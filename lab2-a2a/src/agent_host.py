"""Agent Host - Routes user requests to appropriate A2A agents"""

import os
import asyncio
import logging
from typing import Any
from uuid import uuid4

import httpx
from langchain_google_genai import ChatGoogleGenerativeAI

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest


class AgentHost:
    """Host that routes user requests to appropriate A2A agents"""
    
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        
        # Agent endpoints
        self.agents = {
            "ticketing": "http://localhost:5001",  # Ticketing agent port
            "kubernetes": "http://localhost:8889"  # Kubernetes agent port
        }
        
        self.httpx_client = None
        self.clients = {}
        self.agent_cards = {}  # Store agent cards separately
    
    async def __aenter__(self):
        self.httpx_client = httpx.AsyncClient()
        
        # Initialize clients for each agent
        for agent_name, base_url in self.agents.items():
            try:
                resolver = A2ACardResolver(
                    httpx_client=self.httpx_client,
                    base_url=base_url
                )
                agent_card = await resolver.get_agent_card()
                self.agent_cards[agent_name] = agent_card  # Store card separately
                self.clients[agent_name] = A2AClient(
                    httpx_client=self.httpx_client,
                    agent_card=agent_card
                )
                print(f"✓ Connected to {agent_name} agent at {base_url}")
            except Exception as e:
                print(f"✗ Failed to connect to {agent_name} agent: {e}")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.httpx_client:
            await self.httpx_client.aclose()
    
    async def _classify_request(self, user_input: str) -> str:
        """Use LLM to classify user request and select appropriate agent"""
        
        # Build agent information for LLM
        agent_info = []
        for agent_name in self.clients.keys():
            agent_card = self.agent_cards[agent_name]
            skills_info = []
            for skill in agent_card.skills:
                skills_info.append(f"- {skill.name}: {skill.description} (tags: {', '.join(skill.tags)})")
            
            agent_info.append(f"{agent_name}: {agent_card.description}\nSkills:\n" + "\n".join(skills_info))
        
        prompt = f"""Select the most appropriate agent for this user request: "{user_input}"

Available agents:
{chr(10).join(agent_info)}

Respond with only the agent name (ticketing or kubernetes). If unsure, choose ticketing."""
        
        try:
            response = await self.model.ainvoke(prompt)
            selected_agent = response.content.strip().lower()
            return selected_agent if selected_agent in self.clients else "ticketing"
        except Exception:
            return "ticketing"  # Fallback
    
    def _parse_agent_response(self, response: Any, agent_type: str) -> str:
        """Parse response from A2A agent"""
        try:
            return response.root.result.parts[0].root.text
        except Exception as e:
            return f"Error parsing response from {agent_type} agent: {str(e)}"
    
    async def process_request(self, user_input: str) -> str:
        """Process user request and route to appropriate agent"""
        
        # Classify the request
        agent_type = await self._classify_request(user_input)
        
        if agent_type not in self.clients:
            return f"Error: {agent_type} agent is not available"
        
        print(f"Routing request to {agent_type} agent...")
        
        try:
            # Prepare message
            message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': user_input}],
                    'message_id': uuid4().hex,
                },
            }
            
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**message_payload)
            )
            
            # Send to appropriate agent
            response = await self.clients[agent_type].send_message(request)
            
            # Parse response
            return self._parse_agent_response(response, agent_type)
            
        except Exception as e:
            return f"Error communicating with {agent_type} agent: {str(e)}"


async def main():
    """Interactive agent host"""
    logging.basicConfig(level=logging.INFO)
    
    async with AgentHost() as host:
        print("\n🤖 Agent Host Started")
        print("Available agents: ticketing, kubernetes")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                response = await host.process_request(user_input)
                print(f"{response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}\n")
    
    print("Agent Host stopped.")


if __name__ == "__main__":
    import os
    asyncio.run(main())
