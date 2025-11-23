#!/bin/bash

# Start the Agent Application (FastAPI) in the background
# We use uvicorn to run the app passed in APP_MODULE env var
echo "Starting Agent App: $APP_MODULE"
uvicorn $APP_MODULE --host 0.0.0.0 --port $PORT &
AGENT_PID=$!

# Start the Sidecar in the background
echo "Starting AgentOps Sidecar..."
python3 /app/sidecar/sidecar.py &
SIDECAR_PID=$!

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
