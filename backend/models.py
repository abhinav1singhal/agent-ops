from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"

class FaultType(str, Enum):
    LATENCY = "LATENCY"
    ERROR = "ERROR"
    NONE = "NONE"

class AgentMetrics(BaseModel):
    latency_ms: float
    error_rate: float
    cpu_usage: float = 0.0
    memory_usage: float = 0.0

class AgentConfig(BaseModel):
    region: str
    image: str
    version: str

class Agent(BaseModel):
    agent_id: str
    service_name: str
    status: AgentStatus
    last_heartbeat: datetime
    metrics: AgentMetrics
    active_faults: List[FaultType] = []
    config: AgentConfig

class TelemetryPayload(BaseModel):
    agent_id: str
    service_name: str
    status: AgentStatus
    metrics: AgentMetrics
    config: Optional[AgentConfig] = None

class FaultInjectionRequest(BaseModel):
    fault_type: FaultType
    duration_seconds: int = 60
