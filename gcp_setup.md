# GCP Project Setup & Prerequisites

Follow these steps to prepare your environment for deploying AgentOps.

## 1. Google Cloud CLI Setup

Ensure you have the Google Cloud SDK installed.

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Authenticate for API access (required for local tools/Terraform)
gcloud auth application-default login
```

## 2. Enable Required APIs

Enable the services required for Cloud Run, Firestore, and Artifact Registry.

```bash
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    firestore.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com
```

## 3. Python Environment Setup

It is recommended to use a virtual environment for local development and running scripts.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install -r agents/requirements.txt
```

## 4. Firestore Setup

1.  Go to the [Firestore Console](https://console.cloud.google.com/firestore).
2.  Click **Create Database**.
3.  Select **Native Mode**.
4.  Choose a location (e.g., `us-central1`).
5.  Click **Create**.

## 5. Artifact Registry Setup

Create a repository to store your Docker images.

```bash
# Create a Docker repository named 'agentops-repo' in us-central1
gcloud artifacts repositories create agentops-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="AgentOps Docker Repository"
```

You are now ready to proceed to the [Manual Deployment Guide](manual_deploy_guide.md).
