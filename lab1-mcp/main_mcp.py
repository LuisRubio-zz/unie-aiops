import os
import uuid
import json
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# MCP Server URL
MCP_URL = "http://127.0.0.1:8080/mcp"

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment.")

# Initialize LangChain client with Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

def get_mcp_tools():
    """Fetch list of available MCP tools with their schemas."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": str(uuid.uuid4())
    }
    try:
        response = requests.post(MCP_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return f"Error from MCP: {data['error']}"
        return data.get("result", {})
    except Exception as e:
        return f"Error querying MCP: {e}"

def call_mcp_tool(tool_name, arguments):
    """Call a specific MCP tool with arguments."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": str(uuid.uuid4())
    }
    try:
        response = requests.post(MCP_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return f"Error from MCP: {data['error']}"
        return data.get("result", str(data))
    except Exception as e:
        return f"Error querying MCP: {e}"

def format_tool_info(tools_data):
    """Format tools data for Gemini prompt."""
    if isinstance(tools_data, dict) and 'tools' in tools_data:
        tools_list = tools_data['tools']
    elif isinstance(tools_data, dict):
        # Convert dict to list format
        tools_list = []
        for name, info in tools_data.items():
            if isinstance(info, dict):
                tool_info = {"name": name, **info}
            else:
                tool_info = {"name": name, "description": str(info)}
            tools_list.append(tool_info)
    else:
        tools_list = tools_data if isinstance(tools_data, list) else []
    
    formatted_tools = []
    for tool in tools_list:
        if isinstance(tool, dict):
            name = tool.get('name', 'unknown')
            description = tool.get('description', 'No description')
            
            tool_str = f"- {name}: {description}"
            
            # Add input schema info if available
            input_schema = tool.get('inputSchema', {})
            if input_schema and 'properties' in input_schema:
                properties = input_schema['properties']
                required = input_schema.get('required', [])
                
                params = []
                for param_name, param_info in properties.items():
                    param_type = param_info.get('type', 'string')
                    param_desc = param_info.get('description', '')
                    is_required = param_name in required
                    req_marker = "*" if is_required else ""
                    params.append(f"{param_name}{req_marker}({param_type}): {param_desc}")
                
                if params:
                    tool_str += f"\n  Parameters: {'; '.join(params)}"
            
            formatted_tools.append(tool_str)
    
    return "\n".join(formatted_tools)

def choose_tool_and_args(query, tools_data):
    """Ask LLM to select tool and generate arguments."""
    tools_info = format_tool_info(tools_data)
    
    prompt = f"""You are a Kubernetes assistant. For the user query: "{query}"

Available tools:
{tools_info}

Select the most appropriate tool and generate the required arguments.
Parameters marked with * are required.

Respond in this exact JSON format:
{{"tool_name": "selected_tool", "arguments": {{"param1": "value1", "param2": "value2"}}}}

If no arguments are needed, use: {{"tool_name": "selected_tool", "arguments": {{}}}}
"""
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        
        if not response or not response.content:
            return None, None
        
        # Clean up response text
        response_text = response.content.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        # Parse JSON
        tool_call = json.loads(response_text)
        return tool_call.get("tool_name"), tool_call.get("arguments", {})
        
    except json.JSONDecodeError as e:
        print(f"⚠️ Failed to parse response: {e}")
        print(f"Raw response: {response.content}")
        return None, None
    except Exception as e:
        print(f"⚠️ Error calling LLM: {e}")
        return None, None

def main():
    print("🤖 LangChain + Kubernetes MCP Chat (type 'exit' to quit)\n")

    # Fetch MCP tools once at startup
    tools_data = get_mcp_tools()
    if isinstance(tools_data, str):
        print("⚠️ Could not fetch MCP tools:", tools_data)
        return
    
    print("Available MCP tools loaded successfully\n")

    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        if "k8s" in user_input.lower() or "kubernetes" in user_input.lower():
            query = user_input.strip()
            
            tool_name, arguments = choose_tool_and_args(query, tools_data)
            
            if not tool_name:
                print("⚠️ Could not determine appropriate tool. Please try again.\n")
                continue
            
            print(f"Selected tool: {tool_name}")
            print(f"Arguments: {arguments}")
            
            result = call_mcp_tool(tool_name, arguments)
            
            # Format result with LLM
            format_prompt = f"""User asked: "{query}"
            
Kubernetes tool result:
{result}

Please provide a clear, readable summary of this result for the user."""
            
            try:
                format_response = llm.invoke([HumanMessage(content=format_prompt)])
                print(f"🤖 LangChain: {format_response.content}\n")
            except Exception as e:
                print(f"K8s MCP Result:\n{result}\n")
        else:
            # Normal LangChain conversation
            try:
                response = llm.invoke([HumanMessage(content=user_input)])
                print(f"LangChain: {response.content}\n")
            except Exception as e:
                print(f"⚠️ Error: {e}\n")

if __name__ == "__main__":
    main()