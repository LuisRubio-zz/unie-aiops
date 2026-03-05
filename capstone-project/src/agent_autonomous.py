"""Agent Host - Orchestrates multi-agent workflows with autonomous decision-making"""

import os
import asyncio
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json

import httpx
from langchain_google_genai import ChatGoogleGenerativeAI

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest


class AgentHost:
    """Host that orchestrates multi-agent workflows with autonomous decision-making"""
    
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=os.environ.get("GEMINI_API_KEY"),
            temperature=0.1,  # Lower temperature for more deterministic, concise responses
            max_output_tokens=256  # Limit output tokens for efficiency
        )
        
        # Agent endpoints
        self.agents = {
            "ticketing": "http://localhost:5001",  # Ticketing agent port
            "kubernetes": "http://localhost:8889"  # Kubernetes agent port
        }
        
        self.httpx_client = None
        self.clients = {}
        self.agent_cards = {}  # Store agent cards separately
        self.conversation_history = []  # Track workflow steps
        self.agent_info_cache = None  # Cache agent info to avoid rebuilding
    
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
        
        # Build cached agent information
        if not self.agent_info_cache:
            agent_info = []
            for agent_name in self.clients.keys():
                agent_card = self.agent_cards[agent_name]
                # Only include agent name and primary description
                agent_info.append(f"{agent_name}: {agent_card.description}")
            self.agent_info_cache = "\n".join(agent_info)
        
        prompt = f"""Request: "{user_input}"
Agents: {self.agent_info_cache}
Reply: agent name only (ticketing/kubernetes)"""
        
        try:
            response = await self.model.ainvoke(prompt)
            selected_agent = response.content.strip().lower()
            return selected_agent if selected_agent in self.clients else "ticketing"
        except Exception:
            return "ticketing"  # Fallback
    
    async def _plan_workflow(self, user_input: str) -> List[Dict[str, Any]]:
        """Use LLM to create a multi-step workflow plan"""
        
        # Build minimal agent information
        if not self.agent_info_cache:
            agent_info = []
            for agent_name in self.clients.keys():
                agent_card = self.agent_cards[agent_name]
                agent_info.append(f"{agent_name}: {agent_card.description}")
            self.agent_info_cache = "\n".join(agent_info)
        
        prompt = f"""Request: "{user_input}"
Agents: {self.agent_info_cache}

Create JSON workflow. Rules:
1. Multi-step if request has multiple actions
2. kubernetes first (gather data), ticketing second (create ticket)
3. Use condition "if errors found" for ticketing step

Format: [{{"agent":"name","action":"text","condition":null}}]
Reply: JSON only"""
        
        try:
            response = await self.model.ainvoke(prompt)
            content = response.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            workflow = json.loads(content)
            
            # Validate workflow has multiple steps if request mentions multiple actions
            if isinstance(workflow, list) and len(workflow) > 0:
                return workflow
            
            raise ValueError("Invalid workflow")
            
        except Exception as e:
            print(f"⚠️  Error planning workflow: {e}, using fallback")
            
            # Intelligent fallback using agent skills and capabilities
            return await self._create_fallback_workflow(user_input)
    
    async def _create_fallback_workflow(self, user_input: str) -> List[Dict[str, Any]]:
        """Create fallback workflow using agent skills and cards"""
        
        # Analyze which agents are relevant based on their skills
        relevant_agents = []
        
        for agent_name in self.clients.keys():
            agent_card = self.agent_cards[agent_name]
            
            # Check if any skill tags or descriptions match the request
            for skill in agent_card.skills:
                skill_text = f"{skill.name} {skill.description} {' '.join(skill.tags)}".lower()
                
                # Simple relevance check
                if any(word in user_input.lower() for word in skill_text.split()):
                    relevant_agents.append({
                        'name': agent_name,
                        'card': agent_card,
                        'matching_skills': [skill for skill in agent_card.skills]
                    })
                    break
        
        # If multiple agents are relevant, create multi-step workflow
        if len(relevant_agents) >= 2:
            # Prioritize kubernetes first (data gathering), then ticketing (action)
            workflow = []
            
            for agent_info in relevant_agents:
                if agent_info['name'] == 'kubernetes':
                    workflow.insert(0, {
                        "agent": "kubernetes",
                        "action": f"Execute this request: {user_input}",
                        "condition": None
                    })
                elif agent_info['name'] == 'ticketing':
                    workflow.append({
                        "agent": "ticketing",
                        "action": "Create a ticket with the information from the previous step",
                        "condition": "if issues or errors found"
                    })
            
            return workflow if workflow else await self._single_agent_fallback(user_input)
        
        # Single agent fallback
        return await self._single_agent_fallback(user_input)
    
    async def _single_agent_fallback(self, user_input: str) -> List[Dict[str, Any]]:
        """Fallback to single agent using classification"""
        agent = await self._classify_request(user_input)
        return [{"agent": agent, "action": user_input, "condition": None}]
    
    async def _should_execute_step(self, step: Dict[str, Any], previous_results: List[str]) -> bool:
        """Determine if a step should be executed based on conditions and previous results"""
        
        condition = step.get("condition")
        if not condition:
            return True
        
        if not previous_results:
            return True
        
        # Simple keyword-based condition evaluation to avoid LLM call
        last_result = previous_results[-1].lower()
        condition_lower = condition.lower()
        
        # Check for common condition patterns
        if "error" in condition_lower or "fail" in condition_lower:
            return "error" in last_result or "fail" in last_result
        
        if "issue" in condition_lower or "problem" in condition_lower:
            return "error" in last_result or "fail" in last_result or "issue" in last_result
        
        # Default to executing the step
        return True
    
    async def _call_agent(self, agent_type: str, action: str, context: str = "") -> str:
        """Call a specific agent with an action and optional context from previous steps"""
        
        if agent_type not in self.clients:
            return f"Error: {agent_type} agent is not available"
        
        # Inject context from previous results if available
        full_action = action
        if context and "[PREVIOUS_RESULT]" in action:
            full_action = action.replace("[PREVIOUS_RESULT]", context)
        elif context:
            full_action = f"{action}\n\nContext from previous step:\n{context}"
        
        try:
            message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': full_action}],
                    'message_id': uuid4().hex,
                },
            }
            
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**message_payload)
            )
            
            response = await self.clients[agent_type].send_message(request)
            return self._parse_agent_response(response, agent_type)
            
        except Exception as e:
            return f"Error communicating with {agent_type} agent: {str(e)}"
    
    def _parse_agent_response(self, response: Any, agent_type: str) -> str:
        """Parse response from A2A agent"""
        try:
            return response.root.result.parts[0].root.text
        except Exception as e:
            return f"Error parsing response from {agent_type} agent: {str(e)}"
    
    async def process_request(self, user_input: str) -> str:
        """Process user request with autonomous multi-agent orchestration"""
        
        print(f"\n🤔 Planning workflow for: {user_input}")
        
        # Create workflow plan
        workflow = await self._plan_workflow(user_input)
        
        if not workflow:
            return "Error: Could not create workflow plan"
        
        print(f"📋 Workflow plan: {len(workflow)} step(s)")
        for i, step in enumerate(workflow, 1):
            print(f"  {i}. [{step['agent']}] {step['action'][:80]}{'...' if len(step['action']) > 80 else ''}")
            if step.get('condition'):
                print(f"     ⚡ Condition: {step['condition']}")
        
        # Execute workflow
        results = []
        self.conversation_history = []
        context = ""  # Accumulate context for next steps
        
        for i, step in enumerate(workflow, 1):
            # Check if step should be executed
            should_execute = await self._should_execute_step(step, results)
            
            if not should_execute:
                print(f"\n⏭️  Step {i}: Skipped (condition not met)")
                continue
            
            print(f"\n🔄 Step {i}: Calling {step['agent']} agent...")
            
            # Execute step with context from previous results
            result = await self._call_agent(step['agent'], step['action'], context)
            results.append(result)
            
            # Update context for next step
            context = result
            
            self.conversation_history.append({
                'step': i,
                'agent': step['agent'],
                'action': step['action'],
                'result': result
            })
            
            # Show truncated result
            result_preview = result[:300] + '...' if len(result) > 300 else result
            print(f"✓ Result: {result_preview}")
        
        # Synthesize final response
        if len(results) == 1:
            return results[0]
        
        # Simple concatenation instead of LLM summarization to save tokens
        summary_parts = []
        for i, result in enumerate(results):
            agent_name = self.conversation_history[i]['agent']
            summary_parts.append(f"[{agent_name}] {result[:200]}")
        
        return "\n\n".join(summary_parts)


async def main():
    """Interactive agent host with multi-agent orchestration"""
    logging.basicConfig(level=logging.INFO)
    
    async with AgentHost() as host:
        print("\n🤖 Multi-Agent Orchestrator Started")
        print("Available agents: ticketing, kubernetes")
        print("\nExample requests:")
        print("  - List namespaces and create ticket if pods in error")
        print("  - Check kubernetes cluster health and report issues")
        print("  - Get all pods and create ticket for any failures")
        print("\nType 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                response = await host.process_request(user_input)
                print(f"\n🤖 Final Response:\n{response}\n")
                print("-" * 80)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}\n")
    
    print("Agent Host stopped.")


if __name__ == "__main__":
    import os
    asyncio.run(main())
