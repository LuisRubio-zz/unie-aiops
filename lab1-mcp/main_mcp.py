import os
import uuid
import json
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# MCP Server URL
MCP_URL = "http://127.0.0.1:8080/mcp"

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment.")

# Initialize LangChain 0.3.x
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)

def mcp_request(method, params=None):
    """Make MCP request."""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": str(uuid.uuid4())
    }
    try:
        response = requests.post(MCP_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("result") if "result" in data else data
    except Exception as e:
        return f"Error: {e}"

def create_mcp_tool(tool_info):
    """Create LangChain tool from MCP tool info."""
    name = tool_info.get('name')
    description = tool_info.get('description', f'MCP tool: {name}')
    
    def mcp_tool_func(**kwargs) -> str:
        return str(mcp_request("tools/call", {"name": name, "arguments": kwargs}))
    
    # Set docstring and name
    mcp_tool_func.__doc__ = description
    mcp_tool_func.__name__ = name
    
    # Apply tool decorator
    return tool(mcp_tool_func)

def get_mcp_tools():
    """Dynamically fetch and create tools from MCP server."""
    tools_data = mcp_request("tools/list")
    if isinstance(tools_data, str) or not tools_data:
        return []
    
    tools = []
    for tool_info in tools_data.get('tools', []):
        try:
            mcp_tool = create_mcp_tool(tool_info)
            tools.append(mcp_tool)
        except Exception as e:
            print(f"Warning: Could not create tool {tool_info.get('name')}: {e}")
    
    return tools

tools = get_mcp_tools()

# Create agent with tools
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Kubernetes assistant. Use the available tools to answer questions about Kubernetes clusters."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def is_k8s_query(query):
    """Check if query is Kubernetes related."""
    k8s_keywords = ["k8s", "kubernetes", "pod", "namespace", "deploy", "service", "node", "cluster"]
    return any(keyword in query.lower() for keyword in k8s_keywords)

def main():
    print("🤖 LangChain + Kubernetes MCP Chat (type 'exit' to quit)\n")
    
    try:
        tool_names = [tool.name for tool in tools]
        print(f"Available MCP tools ({len(tools)}): {', '.join(tool_names)}\n")
    except Exception as e:
        print(f"⚠️ Could not connect to MCP server: {e}")
        return

    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        try:
            if is_k8s_query(user_input):
                # Use MCP agent for Kubernetes queries
                result = agent_executor.invoke({"input": user_input})
                print(f"🤖 {result['output']}\n")
            else:
                # Direct LLM for general queries
                response = llm.invoke([HumanMessage(content=user_input)])
                print(f"🤖 {response.content}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")

if __name__ == "__main__":
    main()