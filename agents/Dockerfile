FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY agents/requirements.txt /app/requirements.txt
COPY sidecar/requirements.txt /app/sidecar_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r sidecar_requirements.txt

# Copy Sidecar Code
COPY sidecar /app/sidecar

# Copy Entrypoint
COPY agents/common/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Build Argument to select agent code
ARG AGENT_DIR
COPY agents/${AGENT_DIR} /app/agent

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default Env Vars
ENV PORT=8080
ENV APP_MODULE=agent.main:app

CMD ["/app/entrypoint.sh"]
