"""API key service for generating, hashing, and verifying API keys."""

import secrets
import base64
import logging
from typing import Optional, Tuple
from src.repositories.api_keys import ApiKeyRepository

logger = logging.getLogger(__name__)


class ApiKeyService:
    """Service for API key operations."""
    
    # API key prefix
    KEY_PREFIX = "sk-"
    # Token length in bytes (32 bytes = 256 bits)
    TOKEN_BYTES = 32
    # Maximum retry attempts for collision detection
    MAX_RETRIES = 10
    
    def __init__(self, repository: Optional[ApiKeyRepository] = None):
        """
        Initialize API key service.
        
        Args:
            repository: Optional API key repository (creates new if None)
        """
        self.repository = repository or ApiKeyRepository()
    
    def generate_api_key(self, user_id: str) -> Tuple[str, dict]:
        """
        Generate a new API key for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple of (plaintext_key, metadata_dict)
        """
        # Check if user already has an active key
        existing_key = self.repository.find_by_user_id(user_id)
        if existing_key:
            logger.warning(f"User {user_id} already has an active API key")
            # Return existing key metadata (but not the plaintext key for security)
            return None, existing_key.to_dict()
        
        # Generate unique key with collision detection
        for attempt in range(self.MAX_RETRIES):
            # Generate random token
            token_bytes = secrets.token_bytes(self.TOKEN_BYTES)
            # Encode to base64 URL-safe (no padding)
            token_b64 = base64.urlsafe_b64encode(token_bytes).decode('utf-8').rstrip('=')
            # Create full key with prefix
            plaintext_key = f"{self.KEY_PREFIX}{token_b64}"
            
            # Hash the key
            key_hash = self.hash_api_key(plaintext_key)
            
            # Check for collision
            existing = self.repository.find_by_hash(key_hash)
            if not existing:
                # No collision, store the key
                api_key = self.repository.create(user_id, key_hash)
                logger.info(f"Generated new API key for user {user_id}")
                return plaintext_key, api_key.to_dict()
            
            logger.warning(f"API key collision detected (attempt {attempt + 1}/{self.MAX_RETRIES})")
        
        raise RuntimeError(f"Failed to generate unique API key after {self.MAX_RETRIES} attempts")
    
    def hash_api_key(self, api_key: str) -> str:
        """
        Hash an API key using SHA256 for fast indexed lookup.
        
        Args:
            api_key: Plaintext API key
            
        Returns:
            Hashed API key (SHA256 hex digest)
        
        Note:
            Using SHA256 for MVP (fast indexed lookup).
            TODO: Upgrade to two-hash approach: SHA256 (lookup) + bcrypt (verification)
        """
        import hashlib
        return hashlib.sha256(api_key.encode('utf-8')).hexdigest()
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """
        Verify an API key and return user_id if valid.
        
        Args:
            api_key: Plaintext API key to verify
            
        Returns:
            user_id if valid, None otherwise
        """
        if not api_key or not api_key.startswith(self.KEY_PREFIX):
            logger.debug("Invalid API key format")
            return None
        
        # Use SHA256 for fast indexed lookup
        # TODO: Upgrade to two-hash approach (SHA256 for lookup + bcrypt for verification)
        # For MVP, SHA256 is secure enough for long random API keys
        import hashlib
        lookup_hash = hashlib.sha256(api_key.encode('utf-8')).hexdigest()
        
        api_key_record = self.repository.find_by_hash(lookup_hash)
        if not api_key_record:
            logger.debug("API key not found")
            return None
        
        if not api_key_record.is_active():
            logger.debug(f"API key is {api_key_record.status.value}")
            return None
        
        # Update usage metadata
        self.repository.update_last_used(lookup_hash)
        
        return api_key_record.user_id
    
    def get_user_api_key(self, user_id: str) -> Optional[dict]:
        """
        Get user's API key metadata (without plaintext key).
        
        Args:
            user_id: User ID
            
        Returns:
            Key metadata dict or None if not found
        """
        api_key = self.repository.find_by_user_id(user_id)
        if api_key:
            return api_key.to_dict()
        return None
    
    def revoke_api_key(self, api_key: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            api_key: Plaintext API key to revoke
            
        Returns:
            True if revoked, False otherwise
        """
        import hashlib
        lookup_hash = hashlib.sha256(api_key.encode('utf-8')).hexdigest()
        
        result = self.repository.revoke(lookup_hash)
        if result:
            logger.info("Revoked API key")
        return result

