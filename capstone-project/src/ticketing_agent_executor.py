"""A2A Agent Executor for Ticketing System"""

import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool

from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


@tool
def create_ticket(message: str) -> str:
    """Create a new ticket with the given message"""
    try:
        response = requests.post(
            "http://localhost:5000/api/tickets",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return f"Ticket created successfully: {response.json()}"
    except Exception as e:
        return f"Error creating ticket: {str(e)}"


@tool
def get_all_tickets() -> str:
    """Get all tickets from the system"""
    try:
        response = requests.get("http://localhost:5000/api/tickets")
        response.raise_for_status()
        return f"All tickets: {response.json()}"
    except Exception as e:
        return f"Error getting tickets: {str(e)}"


@tool
def query_tickets(query: str) -> str:
    """Query tickets by search term"""
    try:
        response = requests.get(f"http://localhost:5000/api/tickets?q={query}")
        response.raise_for_status()
        return f"Query results: {response.json()}"
    except Exception as e:
        return f"Error querying tickets: {str(e)}"


class TicketingAgentExecutor(AgentExecutor):
    """A2A Agent Executor for Ticketing System"""

    def __init__(self):
        # Initialize model
        self.model = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY")
        )

        # Register tools
        self.tools = [create_ticket, get_all_tickets, query_tickets]

        # Create LangChain agent
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=(
                "You are a ticketing system assistant. "
                "Help users create, view, and query tickets."
            )
        )

    async def execute(self, context, event_queue):
        """Execute agent logic for incoming message"""

        # Access messages from context (latest SDK)
        user_message = context.message.parts[0].root.text
        print(f"User: '{user_message}'")

        try:
            response = await self.agent.ainvoke({"messages": [{"role": "user", "content": user_message}]})
            print(f"Ticketing Agent: {response}")

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
            print(f"Agent invocation failed: {e}")
            await event_queue.enqueue_event(new_agent_text_message(f"Error: {str(e)}"))

    async def cancel(self, context, event_queue):
        """Cancel is not supported"""
        raise Exception("cancel not supported")
