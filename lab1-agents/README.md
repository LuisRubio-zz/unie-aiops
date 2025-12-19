## Introduction

The objective of this lab is to implement 2 AI agents using LangGraph:

1. **Kubernetes Agent**: Integrated with a Model Context Protocol (MCP) server to monitor and query Kubernetes cluster resources including pods, services, deployments, and nodes
2. **Ticketing Agent**: Equipped with tools to manage a ticketing system for creating, listing, and querying support tickets

Both agents utilize Gemini LLM and demonstrate different integration patterns - MCP for external system connectivity and custom tools for internal operations.

## Pre-requisites

### Clone Repository
```bash
git clone https://github.com/LuisRubio-zz/unie-aiops.git
cd unie-aiops/lab1-agents/
```

### Environment variables
Get a free gemini api key from https://ai.google.dev/gemini-api/docs/pricing
```bash
# Copy .env template
cp .env.example .env
# Update gemini api key in .env file
vi .env
```

### Setup
```bash
# Install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies and create virtual environment:
uv sync
```

### Ticketing Server
```bash
# In a terminal start ticketing server in http://localhost:5000
uv run python src/ticketing_server.py

# In a new termnal start ticketing agent
source .env
uv run python src/ticketing_agent.py

# Interact with ticketing agent and see the results in ticketing server
You: create a ticket for server maintenance
Assistant: Ticket created successfully

You: show all tickets
Assistant: All tickets: ...
```

### Kubernetes Agent

```bash
# Start k8s MCP in a termina
# Download k8s MCP https://github.com/containers/kubernetes-mcp-server
curl -L -o kubernetes-mcp-server https://github.com/containers/kubernetes-mcp-server/releases/download/v0.0.52/kubernetes-mcp-server-linux-amd64

chmod +x kubernetes-mcp-server

sudo mv kubernetes-mcp-server /usr/bin/

# Load environment variables from .env file:
source .env

kubernetes-mcp-server \
  --port 8080 \
  --kubeconfig ~/.kube/config \
  --sse-base-url http://127.0.0.1:8080 \
  --read-only \
  --log-level 9

# In a new terminal atart Kubernetes agent
source .env
uv run python src/k8s_agent.py

# Interact with kubernetes agent agent and see the results in ticketing server
You: list the namespaces in my kubernetes cluster
Assistant: Here are the namespaces in your Kubernetes cluster:
*   my-app
*   keyclock
*   data-lake
```