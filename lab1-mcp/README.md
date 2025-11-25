## Introduction
Gemini LLM integrated with Kubernetes MCP server for natural language Kubernetes operations

## Pre-requisites

### Clone Repo
git clone https://github.com/LuisRubio-zz/unie-aiops.git
cd unie-aiops/lab1-mcp/

### Environment variables
Get a free gemini api key from https://ai.google.dev/gemini-api/docs/pricing
```bash
# Copy .env template
cp .env.example .env
# Update gemini api key and kubeconfig path in .env.example file
vi .env
```

### UV Package Manager
```bash
# Install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create virtual environment and install dependencies:
uv sync

# Activate environment:
source .venv/bin/activate  # Linux/Mac
# Or on Windows: .venv\Scripts\activate
```

### K8s MCP
```bash
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
```

## Operate your k8s cluster using LLM
User <---> Python Chat Script <---> Gemini API
                              \---> Kubernetes MCP Server <---> K8s cluster

```bash
uv run python main_mcp.py
# Or if environment is activated:
# python main_mcp.py

🤖 Gemini + Kubernetes MCP Chat (type 'exit' to quit)

👤 You: list the namespaces in my kubernetes cluster
🤖 Gemini: Selected tool: namespaces_list
🤖 Gemini: Here are the namespaces in your Kubernetes cluster:
*   my-app
*   keyclock
*   data-lake
*   ...

👤 You: list the pods error in my kubernetes cluster
🤖 Selected tool: pods_list_in_namespace
🤖 Gemini: Here are the pods in the `keyclock` namespace that are not in a healthy `Running` or `Completed` state:

*   **`eric-data-distributed-coordinator-ed-1`**: `0/1 Init:0/1` - This pod is stuck in the initialization phase and has not started all its containers.     
*   ...
```