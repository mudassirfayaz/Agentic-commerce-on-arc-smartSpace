"""API key repository for database operations."""

import logging
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.api_key import ApiKey, ApiKeyStatus
from src.database.base import get_db_session

logger = logging.getLogger(__name__)


class ApiKeyRepository:
    """Repository for API key data access."""
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize repository.
        
        Args:
            db: Optional database session (if None, creates new session)
        """
        self.db = db
    
    def _get_db(self) -> Session:
        """Get database session."""
        if self.db:
            return self.db
        return get_db_session()
    
    def create(self, user_id: str, key_hash: str) -> ApiKey:
        """
        Create a new API key record.
        
        Args:
            user_id: User ID
            key_hash: Hashed API key
            
        Returns:
            Created ApiKey object
        """
        db = self._get_db()
        try:
            api_key = ApiKey(
                user_id=user_id,
                key_hash=key_hash,
                status=ApiKeyStatus.ACTIVE
            )
            db.add(api_key)
            db.commit()
            db.refresh(api_key)
            logger.info(f"Created API key for user {user_id}")
            return api_key
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating API key: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def find_by_hash(self, key_hash: str) -> Optional[ApiKey]:
        """
        Find API key by hash.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            ApiKey object or None if not found
        """
        db = self._get_db()
        try:
            api_key = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
            return api_key
        except Exception as e:
            logger.error(f"Error finding API key by hash: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def find_by_user_id(self, user_id: str) -> Optional[ApiKey]:
        """
        Find active API key for user.
        
        Args:
            user_id: User ID
            
        Returns:
            ApiKey object or None if not found
        """
        db = self._get_db()
        try:
            api_key = db.query(ApiKey).filter(
                and_(
                    ApiKey.user_id == user_id,
                    ApiKey.status == ApiKeyStatus.ACTIVE
                )
            ).first()
            return api_key
        except Exception as e:
            logger.error(f"Error finding API key by user_id: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def update_last_used(self, key_hash: str) -> bool:
        """
        Update last used timestamp and increment usage count.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            True if updated, False otherwise
        """
        db = self._get_db()
        try:
            api_key = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
            if api_key:
                api_key.last_used_at = datetime.utcnow()
                api_key.usage_count += 1
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating last used: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def increment_usage_count(self, key_hash: str) -> bool:
        """
        Increment usage count (alias for update_last_used).
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            True if updated, False otherwise
        """
        return self.update_last_used(key_hash)
    
    def revoke(self, key_hash: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            True if revoked, False otherwise
        """
        db = self._get_db()
        try:
            api_key = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
            if api_key:
                api_key.status = ApiKeyStatus.REVOKED
                db.commit()
                logger.info(f"Revoked API key for user {api_key.user_id}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error revoking API key: {e}")
            raise
        finally:
            if not self.db:
                db.close()

