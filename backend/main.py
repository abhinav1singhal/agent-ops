from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .models import TelemetryPayload, FaultInjectionRequest, FaultType
from . import database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentOps-Backend")

app = FastAPI(title="AgentOps API", version="0.1.0")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/v1/telemetry")
async def receive_telemetry(payload: TelemetryPayload):
    """Endpoint for Sidecars to push telemetry."""
    try:
        await database.update_agent_telemetry(payload)
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error updating telemetry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agents")
async def list_agents():
    """List all monitored agents."""
    return await database.get_all_agents()

@app.get("/api/v1/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    agent = await database.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.post("/api/v1/agents/{agent_id}/fault")
async def inject_fault(agent_id: str, request: FaultInjectionRequest):
    """Inject a fault into an agent."""
    logger.info(f"Injecting fault {request.fault_type} into {agent_id}")
    result = await database.set_agent_fault(agent_id, request.fault_type)
    return result

@app.post("/api/v1/agents/{agent_id}/recover")
async def recover_agent(agent_id: str):
    """Trigger manual recovery (restart/clear faults)."""
    logger.info(f"Recovering agent {agent_id}")
    # 1. Clear faults
    await database.set_agent_fault(agent_id, FaultType.NONE)
    # 2. In a real scenario, we would call Cloud Run API here to restart
    # For MVP, we just clear the fault state
    return {"status": "recovery_initiated", "agent_id": agent_id}

# Mock Cloud Run Interaction (Placeholder)
async def restart_cloud_run_service(service_name: str, region: str):
    logger.info(f"Restarting Cloud Run service: {service_name} in {region}")
    # Use google-cloud-run library here
    pass
