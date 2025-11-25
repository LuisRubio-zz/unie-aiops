# A2A Protocol with Gemini AI

Agent-to-Agent communication protocol implementation using Google's Gemini API for intelligent agent interactions.

## Setup

### Clone Repo
git clone https://github.com/LuisRubio-zz/unie-aiops.git
cd unie-aiops/lab1-mcp/

1. Create conda environment:
```bash
conda env create -f environment.yml
conda activate a2a-agents
```

2. Set your Gemini API key:
```bash
set GEMINI_API_KEY=<GEMINI_API_KEY>
```

3. Run the demo:
```bash
python demo.py
```

## Agents

- **TaskAgent** (port 5001): Task management and execution
- **DataAgent** (port 5002): Data analysis and insights  
- **CoordinatorAgent** (port 5003): Orchestrates multi-agent workflows

## Usage

The coordinator receives instructions and coordinates responses between specialized agents using Gemini AI for intelligent processing.