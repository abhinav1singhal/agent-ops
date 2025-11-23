import os
from google.cloud import firestore
from datetime import datetime
from .models import Agent, AgentStatus, TelemetryPayload, FaultType

# Initialize Firestore Client
# In production, this uses Application Default Credentials
# For local dev, ensure GOOGLE_APPLICATION_CREDENTIALS is set or use emulator
db = firestore.Client()

AGENTS_COLLECTION = "agents"

async def update_agent_telemetry(payload: TelemetryPayload):
    """Updates or creates an agent document with the latest telemetry."""
    doc_ref = db.collection(AGENTS_COLLECTION).document(payload.agent_id)
    
    agent_data = payload.dict()
    agent_data['last_heartbeat'] = datetime.utcnow()
    
    # Merge with existing data to preserve active_faults if not in payload
    # But here we want to update metrics and status primarily
    doc_ref.set(agent_data, merge=True)
    return doc_ref.get().to_dict()

async def get_all_agents():
    """Retrieves all agents."""
    docs = db.collection(AGENTS_COLLECTION).stream()
    agents = []
    for doc in docs:
        agents.append(doc.to_dict())
    return agents

async def get_agent(agent_id: str):
    """Retrieves a single agent."""
    doc = db.collection(AGENTS_COLLECTION).document(agent_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

async def set_agent_fault(agent_id: str, fault_type: FaultType):
    """Sets the active fault for an agent."""
    doc_ref = db.collection(AGENTS_COLLECTION).document(agent_id)
    # For MVP, we just overwrite the list with the single fault
    faults = [fault_type] if fault_type != FaultType.NONE else []
    doc_ref.update({"active_faults": faults})
    return {"agent_id": agent_id, "active_faults": faults}

async def delete_agent(agent_id: str):
    db.collection(AGENTS_COLLECTION).document(agent_id).delete()
