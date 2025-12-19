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
    
    def _classify_request(self, user_input: str) -> str:
        """Classify user request to determine which agent to use"""
        user_input_lower = user_input.lower()
        
        # Kubernetes keywords
        k8s_keywords = [
            "kubernetes", "k8s", "pod", "deployment", "service", "namespace",
            "cluster", "node", "container", "kubectl", "helm", "ingress"
        ]
        
        # Ticketing keywords
        ticket_keywords = [
            "ticket", "issue", "bug", "problem", "support", "help desk",
            "incident", "request", "complaint", "report"
        ]
       
        # Check for ticketing keywords
        if any(keyword in user_input_lower for keyword in ticket_keywords):
            return "ticketing"
        
        # Check for Kubernetes keywords
        if any(keyword in user_input_lower for keyword in k8s_keywords):
            return "kubernetes"
        

        
        # Default to ticketing for general support requests
        return "ticketing"
    
    def _parse_agent_response(self, response: Any, agent_type: str) -> str:
        """Parse response from A2A agent"""
        try:
            return response.root.result.parts[0].root.text
        except Exception as e:
            return f"Error parsing response from {agent_type} agent: {str(e)}"
    
    async def process_request(self, user_input: str) -> str:
        """Process user request and route to appropriate agent"""
        
        # Classify the request
        agent_type = self._classify_request(user_input)
        
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
