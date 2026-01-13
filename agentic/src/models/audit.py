"""
Audit Logging Models

Defines audit trail and logging structures for compliance.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid
import requests
import logging

from ..config import config

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of events that can be logged"""
    # Request lifecycle
    REQUEST_RECEIVED = "request_received"
    REQUEST_VALIDATED = "request_validated"
    REQUEST_REJECTED = "request_rejected"
    
    # Policy checks
    POLICY_CHECK = "policy_check"
    POLICY_VIOLATION = "policy_violation"
    PROVIDER_VALIDATION = "provider_validation"
    MODEL_VALIDATION = "model_validation"
    
    # Budget checks
    BUDGET_CHECK = "budget_check"
    BUDGET_EXHAUSTED = "budget_exhausted"
    BUDGET_ALERT = "budget_alert"
    
    # Risk assessment
    RISK_ASSESSMENT = "risk_assessment"
    FRAUD_DETECTED = "fraud_detected"
    ANOMALY_DETECTED = "anomaly_detected"
    
    # Agent decisions
    AGENT_DECISION = "agent_decision"
    AGENT_ESCALATION = "agent_escalation"
    
    # Payment execution
    PAYMENT_APPROVED = "payment_approved"
    PAYMENT_EXECUTED = "payment_executed"
    PAYMENT_FAILED = "payment_failed"
    
    # API execution
    API_CALL_STARTED = "api_call_started"
    API_CALL_COMPLETED = "api_call_completed"
    API_CALL_FAILED = "api_call_failed"
    
    # System events
    SYSTEM_ERROR = "system_error"
    CONFIGURATION_CHANGED = "configuration_changed"


@dataclass
class AuditEntry:
    """
    Single audit log entry for an event.
    
    Example (Provider Validation):
        entry = AuditEntry(
            event_type=AuditEventType.PROVIDER_VALIDATION,
            request_id="req_abc123",
            user_id="medical_store_001",
            event_details={
                "provider_requested": "openai",
                "allowed_providers": ["openai", "google"],
                "validation_result": "PASSED"
            },
            result="success"
        )
    """
    
    # Identifiers
    log_id: str = field(default_factory=lambda: f"log_{uuid.uuid4().hex[:16]}")
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    agent_id: Optional[str] = None
    
    # Event details
    event_type: AuditEventType = AuditEventType.REQUEST_RECEIVED
    event_details: Dict[str, Any] = field(default_factory=dict)
    
    # Context snapshot (state at time of event)
    context_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    # Result
    result: str = "success"  # "success", "failure", "warning"
    error: Optional[str] = None
    
    # Timestamp
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Immutability hash (for audit integrity)
    previous_hash: Optional[str] = None
    entry_hash: Optional[str] = None
    
    def calculate_hash(self) -> str:
        """
        Calculate hash of this entry for immutability.
        Hash includes previous_hash to create chain.
        """
        import hashlib
        import json
        
        # Create deterministic string representation
        data = {
            "log_id": self.log_id,
            "request_id": self.request_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "event_details": json.dumps(self.event_details, sort_keys=True),
            "result": self.result,
            "previous_hash": self.previous_hash or "",
        }
        
        data_str = json.dumps(data, sort_keys=True)
        self.entry_hash = hashlib.sha256(data_str.encode()).hexdigest()
        return self.entry_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "log_id": self.log_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "agent_id": self.agent_id,
            "event_type": self.event_type.value,
            "event_details": self.event_details,
            "context_snapshot": self.context_snapshot,
            "result": self.result,
            "error": self.error,
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }


@dataclass
class AuditLog:
    """
    Collection of audit entries for a request or time period.
    
    Represents the complete audit trail.
    """
    
    # Identifiers
    audit_id: str = field(default_factory=lambda: f"audit_{uuid.uuid4().hex[:16]}")
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    
    # Entries
    entries: List[AuditEntry] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_entry(self, entry: AuditEntry) -> None:
        """Add entry to audit log with hash chaining"""
        if self.entries:
            # Link to previous entry
            entry.previous_hash = self.entries[-1].entry_hash
        
        entry.calculate_hash()
        self.entries.append(entry)
        self.updated_at = datetime.utcnow()
    
    def get_entries_by_type(self, event_type: AuditEventType) -> List[AuditEntry]:
        """Get all entries of specific type"""
        return [e for e in self.entries if e.event_type == event_type]
    
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the audit chain.
        Returns True if all hashes are valid and linked.
        """
        for i, entry in enumerate(self.entries):
            # Verify entry hash
            expected_hash = entry.calculate_hash()
            "updated_at": self.updated_at.isoformat(),
            "integrity_verified": self.verify_integrity(),
        }
    
    @classmethod
    def fetch_from_backend(cls, audit_id: str) -> Optional['AuditLog']:
        """
        Fetch audit log from backend.
        
        Args:
            audit_id: Audit log identifier
            
        Returns:
            AuditLog object or None if not found
        """
        try:
            url = config.get_endpoint('audits', 'get_log', audit_id=audit_id)
            response = requests.get(url, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            entries = []
            for entry_data in data.get('entries', []):
                event_type = AuditEventType(entry_data['event_type'])
                entry = AuditEntry(
                    log_id=entry_data['log_id'],
                    request_id=entry_data.get('request_id'),
                    user_id=entry_data.get('user_id'),
                    project_id=entry_data.get('project_id'),
                    agent_id=entry_data.get('agent_id'),
                    event_type=event_type,
                    event_details=entry_data.get('event_details', {}),
                    context_snapshot=entry_data.get('context_snapshot', {}),
                    result=entry_data.get('result', 'success'),
                    error=entry_data.get('error'),
                    previous_hash=entry_data.get('previous_hash'),
                    entry_hash=entry_data.get('entry_hash'),
                )
                entries.append(entry)
            
            return cls(
                audit_id=data['audit_id'],
                request_id=data.get('request_id'),
                user_id=data.get('user_id'),
                project_id=data.get('project_id'),
                entries=entries,
            )
        except Exception as e:
            logger.error(f"Failed to fetch audit log from backend: {e}")
            return None
   
            # Verify chain link
            if i > 0:
                if entry.previous_hash != self.entries[i-1].entry_hash:
                    return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "audit_id": self.audit_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "entries": [e.to_dict() for e in self.entries],
            "total_entries": len(self.entries),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "integrity_verified": self.verify_integrity(),
        }
