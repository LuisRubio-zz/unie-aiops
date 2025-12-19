## Introduction

The objective of this lab is to wrap the AI agents from lab1 into Agent2Agent (A2A) protocol and demonstrate inter-agent communication:

1. **Kubernetes A2A Agent**: Wraps the Kubernetes MCP agent with A2A protocol support for monitoring cluster resources
2. **Ticketing A2A Agent**: Wraps the ticketing agent with A2A protocol support for ticket management
3. **Agent Host**: Central coordinator that routes user requests to appropriate A2A agents based on request classification

All agents utilize Gemini LLM and demonstrate A2A protocol integration patterns - enabling seamless inter-agent communication through standardized agent cards and messaging.

## Pre-requisites

### Clone Repository
```bash
git clone https://github.com/LuisRubio-zz/unie-aiops.git
cd unie-aiops/lab2-a2a/
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





## Running the A2A Agents

### 1. Ticketing A2A Agent
First start the ticketing server, then the A2A agent

```bash
# In a first terminal start ticketing server at http://localhost:5000
# Note: Use the ticketing server from lab1-agents
cd cd unie-aiops/lab1-agents/
source .env
uv run python src/ticketing_server.py

# In a second terminal start ticketing A2A agent
cd unie-aiops/lab2-a2a/
source .env
uv run python src/ticketing_a2a_server.py

# Agent will be available at http://localhost:5001
# Agent card at: http://localhost:5001/.well-known/agent
```

### 2. Kubernetes A2A Agent
First start the Kubernetes MCP server, then the A2A agent

```bash
# In a third terminal, download and start k8s MCP server
# Download k8s MCP https://github.com/containers/kubernetes-mcp-server
curl -L -o kubernetes-mcp-server https://github.com/containers/kubernetes-mcp-server/releases/download/v0.0.52/kubernetes-mcp-server-linux-amd64

chmod +x kubernetes-mcp-server

sudo mv kubernetes-mcp-server /usr/bin/

# Load environment variables from .env file:
cd unie-aiops/lab2-a2a/
source .env

kubernetes-mcp-server \
  --port 8080 \
  --kubeconfig ~/.kube/config \
  --sse-base-url http://127.0.0.1:8080 \
  --read-only \
  --log-level 9

# In a fourth terminal start Kubernetes A2A agent
cd unie-aiops/lab2-a2a/
source .env
uv run python src/k8s_agent_server.py

# Agent will be available at http://localhost:8889
# Agent card at: http://localhost:8889/.well-known/agent
```

### 3. Agent Host
Central coordinator that routes requests to appropriate agents

```bash
# In a fifth terminal start agent host
cd unie-aiops/lab2-a2a/
source .env
uv run python src/agent_host.py

# Interact with agent host - it will route requests automatically
You: create a ticket for server maintenance
Agent: Ticket created successfully

You: list the namespaces in my kubernetes cluster
Agent: Here are the namespaces in your Kubernetes cluster:
*   my-app
*   keycloak
*   data-lake
```