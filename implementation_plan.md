# AgentOps Cloud Deployment Plan

## Goal Description
Deploy the **AgentOps** system and two sample AI agents to **Google Cloud Run**. The system will be fully cloud-native, with no local components.

## User Review Required
> [!IMPORTANT]
> **Prerequisites**:
> - Active Google Cloud Project.
> - `gcloud` CLI installed and authenticated.
> - APIs Enabled: `run.googleapis.com`, `firestore.googleapis.com`, `artifactregistry.googleapis.com`, `aiplatform.googleapis.com`.

## Proposed Changes

### 1. Sample AI Agents
We will create two distinct AI agents using the **Google Generative AI SDK** (Gemini).

#### [NEW] [agents/chat_agent/main.py](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/agents/chat_agent/main.py)
- Simple FastAPI wrapper around `google.generativeai`.
- Exposes `/chat` endpoint.

#### [NEW] [agents/summary_agent/main.py](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/agents/summary_agent/main.py)
- FastAPI wrapper for text summarization.
- Exposes `/summarize` endpoint.

#### [NEW] [agents/common/entrypoint.sh](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/agents/common/entrypoint.sh)
- Script to start **both** the Agent application and the **Sidecar** process in the same container.

### 2. Containerization for Cloud
Update/Create Dockerfiles to be Cloud Run ready.

#### [MODIFY] [backend/Dockerfile](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/backend/Dockerfile)
- Ensure it listens on `$PORT` (Cloud Run requirement).

#### [MODIFY] [frontend/Dockerfile](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/frontend/Dockerfile)
- Production build for Next.js.

#### [NEW] [agents/Dockerfile](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/agents/Dockerfile)
- Shared Dockerfile for agents (uses build args to select agent code).
- Installs `sidecar` dependencies.

### 3. GCP Project Setup & Prerequisites
Explicit commands to prepare the environment.

#### [NEW] [gcp_setup.md](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/gcp_setup.md)
- Guide containing:
    1. `gcloud auth login` & `application-default login`.
    2. `gcloud config set project`.
    3. `gcloud services enable ...` (Run, Artifact Registry, Firestore, AI Platform).
    4. Python Virtual Environment setup (`python -m venv venv`).
    5. `pip install` requirements.

### 4. Manual Deployment Workflow
Instead of a single script, we will document the exact commands to build and deploy each component.

#### [NEW] [manual_deploy_guide.md](file:///C:/Users/15516/.gemini/antigravity/brain/efc8e9e7-f34d-4f02-999b-8afdd51d2847/manual_deploy_guide.md)
- Step-by-step commands to:
    1. **Create Repo**: `gcloud artifacts repositories create...`
    2. **Build Backend**: `gcloud builds submit ... backend`
    3. **Deploy Backend**: `gcloud run deploy ...`
    4. **Build & Deploy Frontend**: Similar steps, passing `NEXT_PUBLIC_API_URL`.
    5. **Build & Deploy Agents**: Steps for `chat-agent` and `summary-agent` with build args.

## Verification Plan

### Manual Verification
1.  **Setup**: Follow `gcp_setup.md` to configure CLI and environment.
2.  **Deploy**: Execute commands from `manual_deploy_guide.md` one by one.
3.  **Verify**: Access the deployed Frontend URL and check Agent health.
