# AgentOps: AI Agent Observability & Self-Healing

**AgentOps** is an operation dashboard designed to monitor the health of AI agents running on Google Cloud Infrastructure. It provides real-time observability, vulnerability reporting, fault injection testing, and automated self-healing capabilities.

![AgentOps Dashboard](https://via.placeholder.com/800x400?text=AgentOps+Dashboard+Preview)

## 🚀 Features

*   **Real-time Monitoring**: Track agent health, latency, and error rates via a centralized dashboard.
*   **Sidecar Pattern**: Lightweight sidecar process runs alongside agents to push telemetry without modifying agent core logic.
*   **Fault Injection**: Simulate production issues (High Latency, Crashes) directly from the UI to test resilience.
*   **Self-Healing**: Automated recovery mechanisms to restart unhealthy agents.
*   **Cloud Native**: Built for Google Cloud Run with Firestore for real-time state management.

## 🏗️ Architecture

The system consists of three main components:
1.  **Dashboard (Frontend)**: Next.js application for visualization and control.
2.  **Platform (Backend)**: FastAPI service handling telemetry and GCP control plane interactions.
3.  **Agents & Sidecars**: AI Agents (e.g., Gemini-powered Chat/Summary bots) paired with a telemetry sidecar.

See [Architecture Design](architecture_design.md) for details.

## 🛠️ Getting Started (Local)

Run the entire stack locally using Docker Compose.

### Prerequisites
*   Docker & Docker Compose
*   Google Cloud Credentials (optional for local mock)

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd agentops

# Start services
docker-compose up --build
```

Access the services:
*   **Dashboard**: [http://localhost:3000](http://localhost:3000)
*   **Backend API**: [http://localhost:8000](http://localhost:8000)

## ☁️ Cloud Deployment (Google Cloud Run)

We provide detailed guides to deploy AgentOps to Google Cloud Platform.

1.  **[GCP Setup Guide](gcp_setup.md)**: Configure your project, enable APIs, and setup your environment.
2.  **[Manual Deployment Guide](manual_deploy_guide.md)**: Step-by-step commands to build and deploy Backend, Frontend, and Agents.

## 🧪 Verification & Usage

### 1. Check Agent Health
Open the Dashboard. You should see cards for `chat-service` and `summary-service` (or `demo-service` locally) with **HEALTHY** status.

### 2. Inject Faults
1.  Click **Inject Latency** on an agent card.
2.  Observe the **Latency** metric spike (>2000ms) after a few seconds.
3.  Click **Inject Error** to simulate a crash. Status will turn **UNHEALTHY**.

### 3. Test Self-Healing
1.  When an agent is **UNHEALTHY**, click **Recover**.
2.  The system will clear the fault state and (in a real cloud env) trigger a service restart.
3.  Status should return to **HEALTHY**.

## 📂 Project Structure

```
├── agents/             # Sample AI Agents (Chat, Summary)
├── backend/            # FastAPI Platform Backend
├── frontend/           # Next.js Dashboard
├── sidecar/            # Telemetry Sidecar Script
├── architecture_design.md
├── gcp_setup.md
├── manual_deploy_guide.md
├── docker-compose.yml
└── diagrams/           # Mermaid.js Diagram Scripts
```

## 📊 Diagrams

### System Architecture
[Source Script](diagrams/architecture.mmd)

```mermaid
graph TD
    %% Styling
    classDef gcp fill:#e8f0fe,stroke:#4285f4,stroke-width:2px;
    classDef user fill:#fff,stroke:#333,stroke-width:2px;
    classDef agent fill:#e6f4ea,stroke:#34a853,stroke-width:2px;
    classDef db fill:#fce8e6,stroke:#ea4335,stroke-width:2px;

    subgraph User_Layer ["User Layer"]
        User[User / Operator]:::user
    end

    subgraph GCP_Infrastructure [Google Cloud Platform]
        direction TB
        
        subgraph Cloud_Run_Services ["Cloud Run Services"]
            Dashboard["AgentOps Dashboard\n(Next.js)"]:::gcp
            Backend["AgentOps Platform\n(FastAPI)"]:::gcp
        end
        
        subgraph Data_Layer ["Data Layer"]
            Firestore[("Google Firestore\nReal-time DB")]:::db
        end
        
        subgraph Managed_Agents ["Managed AI Agents (Cloud Run)"]
            subgraph Agent_Instance ["Agent Pod / Container"]
                Sidecar[AgentOps Sidecar]:::agent
                Agent[AI Agent Core]:::agent
            end
        end
        
        GCP_API["GCP Control Plane\n(Cloud Run Admin API)"]:::gcp
    end

    %% Interactions
    User -->|1. View Health / Inject Fault| Dashboard
    Dashboard -->|2. API Calls| Backend
    Backend <-->|3. Read/Write State| Firestore
    
    %% Telemetry
    Sidecar -->|4. Push Telemetry| Backend
    Sidecar -->|5. Health Check| Agent
    
    %% Fault Injection & Control
    Backend -.->|6. Polls/Stream Config| Sidecar
    Backend -->|7. Restart Service| GCP_API
    GCP_API -->|8. Manage Lifecycle| Agent_Instance

    %% Legend or Notes
    linkStyle 0,1,2,3,4,5,6,7 stroke:#333,stroke-width:1px;
```

### Sequence Diagram (Workflows)
[Source Script](diagrams/sequence.mmd)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Dashboard
    participant API as Backend API
    participant DB as Firestore
    participant Sidecar
    participant Agent as AI Agent
    participant GCP as GCP Control Plane

    %% 1. Telemetry Loop
    rect rgb(240, 248, 255)
        Note over Sidecar, Agent: 1. Telemetry Loop (Every 5s)
        loop Continuous Monitoring
            Sidecar->>Agent: Health Check (HTTP/Process)
            Agent-->>Sidecar: Status OK
            Sidecar->>API: POST /telemetry (Metrics, Status)
            API->>DB: Update Agent State
        end
    end

    %% 2. Fault Injection
    rect rgb(255, 245, 235)
        Note over User, Sidecar: 2. Fault Injection Flow
        User->>UI: Click "Inject Latency"
        UI->>API: POST /inject-fault {type: latency}
        API->>DB: Update Agent Config (active_faults)
        DB-->>API: Acknowledge
        
        par Real-time Update
            DB-->>UI: Stream Update (Fault Pending)
        and Sidecar Polling
            Sidecar->>API: Poll Config / Listen Stream
            API-->>Sidecar: New Config (Fault: Latency)
            Sidecar->>Sidecar: Apply Latency Logic
        end
    end

    %% 3. Self-Healing
    rect rgb(235, 255, 235)
        Note over API, GCP: 3. Self-Healing Flow
        alt Agent Unhealthy
            Sidecar->>API: Report Error / Timeout
            API->>DB: Update Status: UNHEALTHY
            DB-->>UI: Alert User
            
            API->>GCP: Trigger Service Restart
            GCP->>Agent: Restart Container
            Agent-->>Sidecar: Reset
            Sidecar->>API: Report Status: HEALTHY
        end
    end
```
