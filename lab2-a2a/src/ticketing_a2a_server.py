#!/usr/bin/env python3
"""A2A Ticketing Agent Server"""

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from ticketing_agent_executor import TicketingAgentExecutor


def main():
    # Define agent skills
    create_ticket_skill = AgentSkill(
        id='create_ticket',
        name='Create Ticket',
        description='Create a new support ticket with a message',
        tags=['ticket', 'create', 'support'],
        examples=['create a ticket for server maintenance', 'new ticket about login issues'],
    )

    list_tickets_skill = AgentSkill(
        id='list_tickets',
        name='List Tickets',
        description='Get all tickets from the system',
        tags=['ticket', 'list', 'view'],
        examples=['show all tickets', 'list tickets', 'get tickets'],
    )

    query_tickets_skill = AgentSkill(
        id='query_tickets',
        name='Query Tickets',
        description='Search and query tickets by keywords',
        tags=['ticket', 'search', 'query'],
        examples=['find tickets about login', 'search for server tickets'],
    )

    # Create agent card
    agent_card = AgentCard(
        name='Ticketing System Agent',
        description='A support ticketing system agent that can create, list, and query tickets',
        url='http://localhost:5001/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[create_ticket_skill, list_tickets_skill, query_tickets_skill],
    )

    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=TicketingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Ticketing A2A Agent on http://localhost:5001")
    print("Agent Card will be available at: http://localhost:5001/.well-known/agent")


    app = server.build()
    uvicorn.run(app, host="0.0.0.0", port=5001) 


if __name__ == "__main__":
    main()
