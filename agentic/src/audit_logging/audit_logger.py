"""
Comprehensive audit logging system with immutability guarantees.

Logs every decision, policy check, risk assessment, payment, and API call
with full context for compliance audits and debugging.
"""

import hashlib
import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path


class EventType(Enum):
    """Types of audit events"""
    REQUEST_RECEIVED = "request_received"
    POLICY_CHECK = "policy_check"
    BUDGET_CHECK = "budget_check"
    RISK_ASSESSMENT = "risk_assessment"
    AGENT_DECISION = "agent_decision"
    PAYMENT_RESERVED = "payment_reserved"
    PAYMENT_COMPLETED = "payment_completed"
    API_CALL_SUCCESS = "api_call_success"
    API_CALL_FAILED = "api_call_failed"
    ERROR = "error"


@dataclass
class AuditEvent:
    """Single immutable audit log entry"""
    log_id: str
    timestamp: datetime
    request_id: str
    user_id: str
    project_id: str
    agent_id: Optional[str]
    event_type: EventType
    event_details: Dict[str, Any]
    context_snapshot: Dict[str, Any]
    result: str  # "success" or "failure"
    error: Optional[str] = None
    previous_hash: Optional[str] = None
    current_hash: Optional[str] = None
    
    def __post_init__(self):
        """Calculate hash for immutability chain"""
        if self.current_hash is None:
            self.current_hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate SHA256 hash of this entry + previous hash"""
        content = {
            'log_id': self.log_id,
            'timestamp': self.timestamp.isoformat(),
            'request_id': self.request_id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'agent_id': self.agent_id,
            'event_type': self.event_type.value,
            'event_details': self.event_details,
            'context_snapshot': self.context_snapshot,
            'result': self.result,
            'error': self.error,
            'previous_hash': self.previous_hash
        }
        content_str = json.dumps(content, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()


@dataclass
class AuditTrail:
    """Complete audit trail for a request"""
    request_id: str
    events: List[AuditEvent] = field(default_factory=list)
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_events: int = 0
    
    def add_event(self, event: AuditEvent):
        """Add event to trail"""
        self.events.append(event)
        self.total_events = len(self.events)
        if self.start_time is None:
            self.start_time = event.timestamp
        self.end_time = event.timestamp


@dataclass
class ComplianceReport:
    """Compliance report for a time period"""
    user_id: str
    project_id: Optional[str]
    start_date: datetime
    end_date: datetime
    total_requests: int
    approved_requests: int
    rejected_requests: int
    total_spending: float
    policy_violations: int
    risk_alerts: int
    payment_failures: int
    api_failures: int
    requests: List[Dict[str, Any]] = field(default_factory=list)


class AuditLogger:
    """Comprehensive audit logging with immutability guarantees"""
    
    def __init__(self, log_dir: str = "audit_logs"):
        """Initialize audit logger
        
        Args:
            log_dir: Directory to store audit logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("audit_logger")
        self.logger.setLevel(logging.INFO)
        
        # In-memory trail cache for active requests
        self._trails: Dict[str, AuditTrail] = {}
        
        # Last hash for chain integrity
        self._last_hash: Optional[str] = None
        
        # Setup file handler
        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def _generate_log_id(self) -> str:
        """Generate unique log ID"""
        import uuid
        return f"log_{uuid.uuid4().hex[:12]}"
    
    def _write_event(self, event: AuditEvent) -> None:
        """Write event to log file"""
        event_dict = asdict(event)
        event_dict['timestamp'] = event.timestamp.isoformat()
        event_dict['event_type'] = event.event_type.value
        
        # Write as JSON line
        self.logger.info(json.dumps(event_dict, default=str))
        
        # Update last hash
        self._last_hash = event.current_hash
    
    async def log_request_received(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        agent_id: Optional[str],
        request_details: Dict[str, Any]
    ) -> None:
        """Log incoming API request
        
        Args:
            request_id: Unique request identifier
            user_id: User ID
            project_id: Project ID
            agent_id: Agent ID (if applicable)
            request_details: Full request parameters
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=agent_id,
            event_type=EventType.REQUEST_RECEIVED,
            event_details=request_details,
            context_snapshot={'action': 'request_received'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        
        # Initialize trail for this request
        if request_id not in self._trails:
            self._trails[request_id] = AuditTrail(
                request_id=request_id,
                user_id=user_id,
                project_id=project_id
            )
        self._trails[request_id].add_event(event)
    
    async def log_policy_check(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        policies_checked: List[str],
        results: Dict[str, Any],
        compliant: bool
    ) -> None:
        """Log policy validation results
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            policies_checked: List of policies validated
            results: Policy check results
            compliant: Whether request is compliant
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.POLICY_CHECK,
            event_details={
                'policies_checked': policies_checked,
                'results': results,
                'compliant': compliant
            },
            context_snapshot={'action': 'policy_validation'},
            result="success" if compliant else "failure",
            error=None if compliant else "Policy violations detected",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_budget_check(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        estimated_cost: float,
        available_budget: float,
        budget_approved: bool
    ) -> None:
        """Log budget check results
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            estimated_cost: Estimated cost
            available_budget: Available budget
            budget_approved: Whether budget is sufficient
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.BUDGET_CHECK,
            event_details={
                'estimated_cost': estimated_cost,
                'available_budget': available_budget,
                'budget_approved': budget_approved
            },
            context_snapshot={'action': 'budget_check'},
            result="success" if budget_approved else "failure",
            error=None if budget_approved else "Insufficient budget",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_risk_assessment(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        risk_score: float,
        risk_factors: Dict[str, Any],
        risk_level: str
    ) -> None:
        """Log risk assessment details
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            risk_score: Risk score (0-10)
            risk_factors: Detected risk factors
            risk_level: Risk level (low/medium/high)
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.RISK_ASSESSMENT,
            event_details={
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'risk_level': risk_level
            },
            context_snapshot={'action': 'risk_assessment'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_agent_decision(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        agent_id: str,
        agent_tier: str,
        decision: str,
        reasoning: str,
        decision_details: Dict[str, Any]
    ) -> None:
        """Log agent's decision and reasoning
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            agent_id: Agent ID
            agent_tier: Agent tier (FLASH/PRO)
            decision: Decision (APPROVE/REJECT/ESCALATE)
            reasoning: Agent's reasoning
            decision_details: Full decision details
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=agent_id,
            event_type=EventType.AGENT_DECISION,
            event_details={
                'agent_tier': agent_tier,
                'decision': decision,
                'reasoning': reasoning,
                **decision_details
            },
            context_snapshot={'action': 'agent_decision'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_payment_reserved(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        amount: float,
        tx_hash: str,
        reservation_id: str
    ) -> None:
        """Log payment reservation (blockchain transaction)
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            amount: Payment amount (USDC)
            tx_hash: Blockchain transaction hash
            reservation_id: Payment reservation ID
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.PAYMENT_RESERVED,
            event_details={
                'amount': amount,
                'tx_hash': tx_hash,
                'reservation_id': reservation_id,
                'currency': 'USDC'
            },
            context_snapshot={'action': 'payment_reserved'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_payment_completed(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        estimated_amount: float,
        actual_amount: float,
        variance: float
    ) -> None:
        """Log payment completion with variance
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            estimated_amount: Estimated payment
            actual_amount: Actual cost
            variance: Difference (actual - estimated)
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.PAYMENT_COMPLETED,
            event_details={
                'estimated_amount': estimated_amount,
                'actual_amount': actual_amount,
                'variance': variance,
                'variance_percent': (variance / estimated_amount * 100) if estimated_amount > 0 else 0
            },
            context_snapshot={'action': 'payment_completed'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_api_call_success(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        provider: str,
        model: str,
        actual_cost: float,
        response_details: Dict[str, Any]
    ) -> None:
        """Log successful API call
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            provider: API provider
            model: Model used
            actual_cost: Actual cost
            response_details: Response details
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.API_CALL_SUCCESS,
            event_details={
                'provider': provider,
                'model': model,
                'actual_cost': actual_cost,
                **response_details
            },
            context_snapshot={'action': 'api_call_success'},
            result="success",
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_api_call_failed(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        provider: str,
        model: str,
        error: str
    ) -> None:
        """Log failed API call
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            provider: API provider
            model: Model used
            error: Error message
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.API_CALL_FAILED,
            event_details={
                'provider': provider,
                'model': model,
                'error': error
            },
            context_snapshot={'action': 'api_call_failed'},
            result="failure",
            error=error,
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def log_error(
        self,
        request_id: str,
        user_id: str,
        project_id: str,
        error: str,
        error_details: Dict[str, Any]
    ) -> None:
        """Log system error
        
        Args:
            request_id: Request ID
            user_id: User ID
            project_id: Project ID
            error: Error message
            error_details: Error details
        """
        event = AuditEvent(
            log_id=self._generate_log_id(),
            timestamp=datetime.utcnow(),
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            agent_id=None,
            event_type=EventType.ERROR,
            event_details=error_details,
            context_snapshot={'action': 'error'},
            result="failure",
            error=error,
            previous_hash=self._last_hash
        )
        
        self._write_event(event)
        if request_id in self._trails:
            self._trails[request_id].add_event(event)
    
    async def get_request_audit_trail(self, request_id: str) -> Optional[AuditTrail]:
        """Retrieve complete audit trail for a request
        
        Args:
            request_id: Request ID
            
        Returns:
            AuditTrail with all events for this request
        """
        if request_id in self._trails:
            return self._trails[request_id]
        
        # Load from file if not in cache
        trail = AuditTrail(request_id=request_id)
        
        # Read all log files
        for log_file in sorted(self.log_dir.glob("audit_*.jsonl")):
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        event_dict = json.loads(line)
                        if event_dict['request_id'] == request_id:
                            # Reconstruct AuditEvent
                            event = AuditEvent(
                                log_id=event_dict['log_id'],
                                timestamp=datetime.fromisoformat(event_dict['timestamp']),
                                request_id=event_dict['request_id'],
                                user_id=event_dict['user_id'],
                                project_id=event_dict['project_id'],
                                agent_id=event_dict.get('agent_id'),
                                event_type=EventType(event_dict['event_type']),
                                event_details=event_dict['event_details'],
                                context_snapshot=event_dict['context_snapshot'],
                                result=event_dict['result'],
                                error=event_dict.get('error'),
                                previous_hash=event_dict.get('previous_hash'),
                                current_hash=event_dict.get('current_hash')
                            )
                            trail.add_event(event)
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return trail if trail.total_events > 0 else None
    
    async def generate_compliance_report(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        project_id: Optional[str] = None
    ) -> ComplianceReport:
        """Generate compliance report for time period
        
        Args:
            user_id: User ID
            start_date: Report start date
            end_date: Report end date
            project_id: Optional project filter
            
        Returns:
            ComplianceReport with statistics and request summaries
        """
        report = ComplianceReport(
            user_id=user_id,
            project_id=project_id,
            start_date=start_date,
            end_date=end_date,
            total_requests=0,
            approved_requests=0,
            rejected_requests=0,
            total_spending=0.0,
            policy_violations=0,
            risk_alerts=0,
            payment_failures=0,
            api_failures=0
        )
        
        # Aggregate from all log files
        request_summaries: Dict[str, Dict[str, Any]] = {}
        
        for log_file in sorted(self.log_dir.glob("audit_*.jsonl")):
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        event_dict = json.loads(line)
                        
                        # Filter by user, date range, and project
                        event_time = datetime.fromisoformat(event_dict['timestamp'])
                        if event_dict['user_id'] != user_id:
                            continue
                        if not (start_date <= event_time <= end_date):
                            continue
                        if project_id and event_dict.get('project_id') != project_id:
                            continue
                        
                        req_id = event_dict['request_id']
                        if req_id not in request_summaries:
                            request_summaries[req_id] = {
                                'request_id': req_id,
                                'events': []
                            }
                        
                        request_summaries[req_id]['events'].append(event_dict)
                        
                        # Count metrics
                        event_type = event_dict['event_type']
                        if event_type == EventType.REQUEST_RECEIVED.value:
                            report.total_requests += 1
                        elif event_type == EventType.POLICY_CHECK.value:
                            if event_dict['result'] == 'failure':
                                report.policy_violations += 1
                        elif event_type == EventType.RISK_ASSESSMENT.value:
                            details = event_dict.get('event_details', {})
                            if details.get('risk_level') in ['high', 'critical']:
                                report.risk_alerts += 1
                        elif event_type == EventType.AGENT_DECISION.value:
                            details = event_dict.get('event_details', {})
                            if details.get('decision') == 'APPROVE':
                                report.approved_requests += 1
                            elif details.get('decision') == 'REJECT':
                                report.rejected_requests += 1
                        elif event_type == EventType.PAYMENT_RESERVED.value:
                            details = event_dict.get('event_details', {})
                            report.total_spending += details.get('amount', 0.0)
                        elif event_type == EventType.API_CALL_FAILED.value:
                            report.api_failures += 1
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        report.requests = list(request_summaries.values())
        
        return report
