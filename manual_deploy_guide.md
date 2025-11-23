# Manual Deployment Guide

Follow these steps to build and deploy AgentOps components to Google Cloud Run.

**Prerequisites**: Ensure you have completed the [GCP Setup](gcp_setup.md).

## Variables
Set these variables in your terminal for convenience:
```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export REPO="agentops-repo"
```
*(On Windows PowerShell, use `$env:PROJECT_ID = gcloud config get-value project` etc.)*

## 1. Build & Deploy Backend

### Build Image
```bash
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/backend ./backend
```

### Deploy Service
```bash
gcloud run deploy agentops-backend \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID
```

**Note**: Copy the **Service URL** from the output (e.g., `https://agentops-backend-xyz.a.run.app`). You will need it for the next steps.

## 2. Build & Deploy Frontend

### Build Image
```bash
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/frontend ./frontend
```

### Deploy Service
Replace `YOUR_BACKEND_URL` with the URL from Step 1.

```bash
gcloud run deploy agentops-frontend \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/frontend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars NEXT_PUBLIC_API_URL=YOUR_BACKEND_URL
```

**Success**: Open the Frontend Service URL to see the empty dashboard.

## 3. Build & Deploy Agents

We will deploy two agents: `chat-agent` and `summary-agent`.

### Chat Agent

**Build**:
```bash
gcloud builds submit \
    --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/chat-agent \
    --build-arg AGENT_DIR=chat_agent \
    .
```

**Deploy**:
Replace `YOUR_BACKEND_URL` and ensure you have a `GOOGLE_API_KEY` if using real Gemini calls (optional for basic connectivity test).

```bash
gcloud run deploy agent-chat-01 \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/chat-agent \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars BACKEND_URL=YOUR_BACKEND_URL,AGENT_ID=agent-chat-01,SERVICE_NAME=chat-service,APP_MODULE=agent.main:app,GOOGLE_API_KEY=your_key_here
```

### Summary Agent

**Build**:
```bash
gcloud builds submit \
    --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/summary-agent \
    --build-arg AGENT_DIR=summary_agent \
    .
```

**Deploy**:
```bash
gcloud run deploy agent-summary-01 \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/summary-agent \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars BACKEND_URL=YOUR_BACKEND_URL,AGENT_ID=agent-summary-01,SERVICE_NAME=summary-service,APP_MODULE=agent.main:app,GOOGLE_API_KEY=your_key_here
```

## 4. Verification

1.  Refresh the **Frontend Dashboard**.
2.  You should see `chat-service` and `summary-service` listed.
3.  Try injecting a fault to verify the sidecar is communicating with the backend.
