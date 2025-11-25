import os
import uuid
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# MCP Server URL
MCP_URL = "http://127.0.0.1:8080/mcp"

# Load environment and configure Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def mcp_request(method, params=None):
    """Generic MCP request handler."""
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

def get_tools_prompt(tools_data):
    """Convert tools data to prompt format."""
    if not isinstance(tools_data, dict) or 'tools' not in tools_data:
        return "No tools available"
    
    tools_text = []
    for tool in tools_data['tools']:
        name = tool.get('name', 'unknown')
        desc = tool.get('description', 'No description')
        tools_text.append(f"- {name}: {desc}")
        
        # Add parameters if available
        schema = tool.get('inputSchema', {}).get('properties', {})
        required = tool.get('inputSchema', {}).get('required', [])
        if schema:
            params = []
            for param, info in schema.items():
                req = "*" if param in required else ""
                params.append(f"{param}{req}: {info.get('description', '')}")
            if params:
                tools_text.append(f"  Parameters: {', '.join(params)}")
    
    return "\n".join(tools_text)

def ask_gemini(prompt):
    """Simple Gemini API call."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🤖 Gemini + Kubernetes MCP Chat (type 'exit' to quit)\n")
    
    # Get available tools
    tools_data = mcp_request("tools/list")
    if isinstance(tools_data, str):
        print(f"⚠️ Could not fetch MCP tools: {tools_data}")
        return
    
    tools_prompt = get_tools_prompt(tools_data)
    print("Available MCP tools loaded successfully\n")
    
    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break
        
        if any(keyword in user_input.lower() for keyword in ["k8s", "kubernetes", "pod", "namespace", "deploy"]):
            # K8s query - use MCP tools
            prompt = f"""You are a Kubernetes assistant. User query: "{user_input}"

Available tools:
{tools_prompt}

Respond with JSON: {{"tool_name": "tool", "arguments": {{"param": "value"}}}}
If no arguments needed: {{"tool_name": "tool", "arguments": {{}}}}"""
            
            response = ask_gemini(prompt)
            
            try:
                # Extract JSON from response
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    json_str = response.split("```")[1].strip()
                else:
                    json_str = response.strip()
                
                tool_call = json.loads(json_str)
                tool_name = tool_call.get("tool_name")
                arguments = tool_call.get("arguments", {})
                
                print(f"🔧 Using tool: {tool_name}")
                
                # Call MCP tool
                result = mcp_request("tools/call", {"name": tool_name, "arguments": arguments})
                
                # Format result with Gemini
                format_prompt = f"""User asked: "{user_input}"
Tool result: {result}
Provide a clear, human-readable summary."""
                
                summary = ask_gemini(format_prompt)
                print(f"🤖 {summary}\n")
                
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse tool selection. Raw response: {response}\n")
            except Exception as e:
                print(f"⚠️ Error: {e}\n")
        else:
            # Regular chat
            response = ask_gemini(user_input)
            print(f"🤖 {response}\n")

if __name__ == "__main__":
    main()