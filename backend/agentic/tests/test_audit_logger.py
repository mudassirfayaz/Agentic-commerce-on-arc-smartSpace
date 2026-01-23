"""
Tests for AuditLogger module
"""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

from audit_logging.audit_logger import (
    AuditLogger,
    AuditEvent,
    AuditTrail,
    EventType,
    ComplianceReport
)


@pytest.fixture
def temp_audit_dir():
    """Create temporary directory for audit logs"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def audit_logger(temp_audit_dir):
    """Create AuditLogger instance"""
    return AuditLogger(log_dir=temp_audit_dir)


class TestAuditEvent:
    """Test AuditEvent dataclass"""
    
    def test_event_creation(self):
        """Test creating an audit event"""
        event = AuditEvent(
            log_id="log_123",
            timestamp=datetime.utcnow(),
            request_id="req_001",
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            event_type=EventType.REQUEST_RECEIVED,
            event_details={"test": "data"},
            context_snapshot={"action": "test"},
            result="success",
            previous_hash=None
        )
        
        assert event.log_id == "log_123"
        assert event.request_id == "req_001"
        assert event.event_type == EventType.REQUEST_RECEIVED
        assert event.current_hash is not None


class TestAuditLogger:
    """Test AuditLogger logging methods"""
    
    @pytest.mark.asyncio
    async def test_log_request_received(self, audit_logger):
        """Test logging request received event"""
        await audit_logger.log_request_received(
            request_id="req_001",
            user_id="user_001",
            project_id="proj_001",
            agent_id="agent_001",
            request_details={"provider": "openai", "model": "gpt-4"}
        )
        
        trail = await audit_logger.get_request_audit_trail("req_001")
        assert trail is not None
        assert len(trail.events) == 1
        assert trail.events[0].event_type == EventType.REQUEST_RECEIVED
    
    @pytest.mark.asyncio
    async def test_log_policy_check(self, audit_logger):
        """Test logging policy check event"""
        # First log request received
        await audit_logger.log_request_received(
            request_id="req_002",
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={}
        )
        
        # Then log policy check
        await audit_logger.log_policy_check(
            request_id="req_002",
            user_id="user_001",
            project_id="proj_001",
            policies_checked=["provider_whitelist", "model_whitelist"],
            results={"provider_whitelist": True, "model_whitelist": True},
            compliant=True
        )
        
        trail = await audit_logger.get_request_audit_trail("req_002")
        assert trail is not None
        assert len(trail.events) == 2
        assert trail.events[1].event_type == EventType.POLICY_CHECK
        assert trail.events[1].result == "success"
    
    @pytest.mark.asyncio
    async def test_log_budget_check(self, audit_logger):
        """Test logging budget check event"""
        await audit_logger.log_request_received(
            request_id="req_003",
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={}
        )
        
        await audit_logger.log_budget_check(
            request_id="req_003",
            user_id="user_001",
            project_id="proj_001",
            estimated_cost=0.05,
            available_budget=10.0,
            budget_approved=True
        )
        
        trail = await audit_logger.get_request_audit_trail("req_003")
        assert trail is not None
        assert any(e.event_type == EventType.BUDGET_CHECK for e in trail.events)
    
    @pytest.mark.asyncio
    async def test_log_risk_assessment(self, audit_logger):
        """Test logging risk assessment event"""
        await audit_logger.log_request_received(
            request_id="req_004",
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={}
        )
        
        await audit_logger.log_risk_assessment(
            request_id="req_004",
            user_id="user_001",
            project_id="proj_001",
            risk_score=3.5,
            risk_level="LOW",
            risk_factors={"cost_spike": False, "unusual_provider": False}
        )
        
        trail = await audit_logger.get_request_audit_trail("req_004")
        assert trail is not None
        assert any(e.event_type == EventType.RISK_ASSESSMENT for e in trail.events)
    
    @pytest.mark.asyncio
    async def test_log_agent_decision(self, audit_logger):
        """Test logging agent decision event"""
        await audit_logger.log_request_received(
            request_id="req_005",
            user_id="user_001",
            project_id="proj_001",
            agent_id="agent_flash",
            request_details={}
        )
        
        await audit_logger.log_agent_decision(
            request_id="req_005",
            user_id="user_001",
            project_id="proj_001",
            agent_id="agent_flash",
            agent_tier="flash",
            decision="APPROVED",
            reasoning="Low cost and risk",
            decision_details={"confidence": 0.95}
        )
        
        trail = await audit_logger.get_request_audit_trail("req_005")
        assert trail is not None
        assert any(e.event_type == EventType.AGENT_DECISION for e in trail.events)


class TestAuditTrail:
    """Test AuditTrail functionality"""
    
    @pytest.mark.asyncio
    async def test_complete_audit_trail(self, audit_logger):
        """Test building complete audit trail"""
        request_id = "req_complete"
        
        # Simulate complete request flow
        await audit_logger.log_request_received(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={"provider": "openai"}
        )
        
        await audit_logger.log_policy_check(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            policies_checked=["whitelist"],
            results={"whitelist": True},
            compliant=True
        )
        
        await audit_logger.log_budget_check(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            estimated_cost=0.05,
            available_budget=10.0,
            budget_approved=True
        )
        
        trail = await audit_logger.get_request_audit_trail(request_id)
        assert trail is not None
        assert len(trail.events) == 3
        assert trail.request_id == request_id
    
    @pytest.mark.asyncio
    async def test_audit_trail_ordering(self, audit_logger):
        """Test events are ordered chronologically"""
        request_id = "req_order"
        
        await audit_logger.log_request_received(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={}
        )
        
        await audit_logger.log_policy_check(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            policies_checked=["test"],
            results={},
            compliant=True
        )
        
        trail = await audit_logger.get_request_audit_trail(request_id)
        assert trail is not None
        assert len(trail.events) >= 2
        # Verify chronological ordering
        for i in range(len(trail.events) - 1):
            assert trail.events[i].timestamp <= trail.events[i + 1].timestamp


class TestComplianceReporting:
    """Test compliance reporting functionality"""
    
    @pytest.mark.asyncio
    async def test_generate_compliance_report(self, audit_logger):
        """Test generating compliance report"""
        # Create some audit events
        for i in range(3):
            await audit_logger.log_request_received(
                request_id=f"req_{i}",
                user_id="user_001",
                project_id="proj_001",
                agent_id=None,
                request_details={}
            )
        
        report = await audit_logger.generate_compliance_report(
            user_id="user_001",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2030, 12, 31)
        )
        
        assert report is not None
        assert isinstance(report, ComplianceReport)
        assert report.total_requests >= 3


class TestHashChainIntegrity:
    """Test audit log hash chain integrity"""
    
    @pytest.mark.asyncio
    async def test_hash_chain(self, audit_logger):
        """Test hash chain is maintained across events"""
        request_id = "req_hash"
        
        await audit_logger.log_request_received(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            agent_id=None,
            request_details={}
        )
        
        await audit_logger.log_policy_check(
            request_id=request_id,
            user_id="user_001",
            project_id="proj_001",
            policies_checked=["test"],
            results={},
            compliant=True
        )
        
        trail = await audit_logger.get_request_audit_trail(request_id)
        assert trail is not None
        assert len(trail.events) >= 2
        
        # Second event should reference first event's hash
        assert trail.events[1].previous_hash == trail.events[0].current_hash
