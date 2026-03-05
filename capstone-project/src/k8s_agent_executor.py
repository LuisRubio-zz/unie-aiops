"""A2A Agent Executor for MCP Kubernetes Agent"""

import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class MCPAgentExecutor(AgentExecutor):
    """A2A Agent Executor for MCP Kubernetes Agent"""

    def __init__(self):
        # Initialize model
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        
        # MCP server configuration
        self.server_params = {
            "url": "http://127.0.0.1:8080/mcp"
        }
        
        self.agent = None
        self.session = None
        self.client_context = None

    async def _initialize_agent(self):
        """Initialize the agent with MCP tools"""
        if self.agent is None:
            try:
                # Keep the client context and session alive
                self.client_context = streamablehttp_client(**self.server_params)
                read, write, _ = await self.client_context.__aenter__()
                
                self.session = ClientSession(read, write)
                await self.session.__aenter__()
                await self.session.initialize()
                
                # Load MCP tools from Kubernetes server
                tools = await load_mcp_tools(self.session)
                
                # Create agent with Kubernetes MCP tools
                self.agent = create_agent(
                    model=self.model,
                    tools=tools,
                    system_prompt="You are a helpful AI assistant with access to Kubernetes cluster information."
                )
            except Exception as e:
                import traceback
                full_error = traceback.format_exc()
                print(f"Failed to initialize MCP agent: {e}")
                print(f"Full traceback: {full_error}")
                raise

    async def execute(self, context, event_queue):
        """Execute agent logic for incoming message"""
        
        # Access messages from context
        user_message = context.message.parts[0].root.text
        print(f"User message: '{user_message}'")

        try:
            # Initialize agent if not already done
            await self._initialize_agent()
            
            response = await self.agent.ainvoke({"messages": [{"role": "user", "content": user_message}]})
            print(f"Response: {response}")

            # Extract the final AI message content
            if isinstance(response, dict) and "messages" in response:
                # Get the last AI message
                messages = response["messages"]
                for msg in reversed(messages):
                    if hasattr(msg, 'content') and msg.content:
                        result = msg.content
                        break
                else:
                    result = "Task completed successfully"
            else:
                result = str(response)

            await event_queue.enqueue_event(new_agent_text_message(result))
        except Exception as e:
            import traceback
            full_error = traceback.format_exc()
            error_msg = f"MCP connection failed. Please ensure the Kubernetes MCP server is running at {self.server_params['url']}. Error: {str(e)}"
            print(f"Agent invocation failed: {error_msg}")
            print(f"Full traceback: {full_error}")
            await event_queue.enqueue_event(new_agent_text_message(error_msg))

    async def cancel(self, context, event_queue):
        """Cancel is not supported"""
        raise Exception("cancel not supported")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self.client_context:
            await self.client_context.__aexit__(exc_type, exc_val, exc_tb)