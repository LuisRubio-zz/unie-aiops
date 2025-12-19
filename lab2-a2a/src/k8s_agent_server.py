#!/usr/bin/env python3
"""A2A MCP Kubernetes Agent Server"""

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from k8s_agent_executor import MCPAgentExecutor


def main():
    # Define agent skill for Kubernetes monitoring
    monitor_k8s_skill = AgentSkill(
        id='monitor_kubernetes',
        name='Monitor Kubernetes Resources',
        description='Monitor and query Kubernetes cluster resources including pods, services, deployments, and nodes',
        tags=['kubernetes', 'monitoring', 'cluster', 'resources'],
        examples=['show all pods', 'list running services', 'check deployment status', 'get node information'],
    )

    # Create agent card
    agent_card = AgentCard(
        name='Kubernetes Monitoring Agent',
        description='A Kubernetes cluster monitoring agent that provides real-time insights into cluster resources and status',
        url='http://localhost:8889/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[monitor_k8s_skill],
    )

    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=MCPAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Kubernetes Monitoring A2A Agent on http://localhost:8889")
    print("Agent Card will be available at: http://localhost:8889/.well-known/agent")


    app = server.build()
    uvicorn.run(app, host="0.0.0.0", port=8889) 


if __name__ == "__main__":
    main()
