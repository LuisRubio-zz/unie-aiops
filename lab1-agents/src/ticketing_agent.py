#!/usr/bin/env python3
"""Ticketing system agent using LangChain and Gemini API"""

import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool

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

def main():
    # Set up Gemini model
    model = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        api_key=os.environ["GEMINI_API_KEY"]
    )
    
    # Create agent with ticketing tools
    tools = [create_ticket, get_all_tickets, query_tickets]
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a ticketing system assistant. Help users create, view, and query tickets."
    )
    
    # Interactive chat loop
    print("Ticketing Assistant (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        print(f"Assistant: {response['messages'][-1].content}")

if __name__ == "__main__":
    main()
