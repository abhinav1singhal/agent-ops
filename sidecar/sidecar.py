import os
import time
import requests
import random
import logging
from datetime import datetime

# Configuration
AGENT_ID = os.getenv("AGENT_ID", "agent-default-001")
SERVICE_NAME = os.getenv("SERVICE_NAME", "demo-agent-service")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "5"))

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AgentSidecar")

class AgentSidecar:
    def __init__(self):
        self.agent_id = AGENT_ID
        self.service_name = SERVICE_NAME
        self.active_faults = []
        self.status = "HEALTHY"
        
    def check_agent_health(self):
        """Simulates checking the actual AI agent process."""
        # In a real scenario, we'd request localhost:8080/health
        # For MVP, we assume it's healthy unless we are simulating a crash
        if "CRASH" in self.active_faults:
            return "UNHEALTHY"
        return "HEALTHY"

    def collect_metrics(self):
        """Simulates metric collection."""
        base_latency = 100 # ms
        if "LATENCY" in self.active_faults:
            logger.warning("Simulating High Latency...")
            time.sleep(2) # Add 2 seconds delay
            base_latency += 2000
            
        return {
            "latency_ms": base_latency + random.randint(-20, 20),
            "error_rate": 0.0 if self.status == "HEALTHY" else 1.0,
            "cpu_usage": random.uniform(10, 40),
            "memory_usage": random.uniform(200, 500)
        }

    def push_telemetry(self):
        """Pushes telemetry to the backend."""
        self.status = self.check_agent_health()
        metrics = self.collect_metrics()
        
        payload = {
            "agent_id": self.agent_id,
            "service_name": self.service_name,
            "status": self.status,
            "metrics": metrics,
            "config": {
                "region": "us-central1",
                "image": "gcr.io/demo/agent:v1",
                "version": "1.0.0"
            }
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/api/v1/telemetry", json=payload)
            if response.status_code == 200:
                logger.info(f"Telemetry pushed. Status: {self.status}")
            else:
                logger.error(f"Failed to push telemetry: {response.text}")
        except Exception as e:
            logger.error(f"Connection error to backend: {e}")

    def poll_config(self):
        """Polls backend for fault injection commands."""
        # In a real system, this might be a separate thread or use Firestore listeners
        # For MVP, we'll just fetch the agent details occasionally or rely on the response from telemetry (if we designed it that way)
        # But our current API doesn't return config in telemetry response. 
        # Let's add a poll to get agent details to see active faults.
        try:
            response = requests.get(f"{BACKEND_URL}/api/v1/agents/{self.agent_id}")
            if response.status_code == 200:
                data = response.json()
                self.active_faults = data.get("active_faults", [])
                if self.active_faults:
                    logger.info(f"Active Faults Detected: {self.active_faults}")
        except Exception as e:
            pass

    def run(self):
        logger.info(f"Starting Sidecar for {self.agent_id}...")
        while True:
            self.poll_config()
            self.push_telemetry()
            time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    sidecar = AgentSidecar()
    sidecar.run()
