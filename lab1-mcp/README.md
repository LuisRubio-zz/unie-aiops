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

### Conda
```bash
# Install conda in Linux:
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh
conda --version
echo $PATH # check conda is in the path

# To install dependencies and start environment:
conda env create -f environment.yml
conda activate langchain-llm

# If required, to deactivate conda environment
conda deactivate
```

### K8s MCP
```bash
# Download k8s MCP https://github.com/containers/kubernetes-mcp-server
curl -L -o kubernetes-mcp-server https://github.com/containers/kubernetes-mcp-server/releases/download/v0.0.52/kubernetes-mcp-server-linux-amd64

chmod +x kubernetes-mcp-server

sudo mv kubernetes-mcp-server /usr/bin/

export KUBECONFIG=~/.kube/config
kubernetes-mcp-server \
  --port 8080 \
  --kubeconfig $KUBECONFIG \
  --sse-base-url http://127.0.0.1:8080 \
  --read-only \
  --log-level 9
```

## Operate your k8s cluster using LLM
User <---> Python Chat Script <---> Gemini API
                              \---> Kubernetes MCP Server <---> K8s cluster

```bash
python main_mcp.py

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