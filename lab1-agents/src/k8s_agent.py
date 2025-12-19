#!/usr/bin/env python3
"""Minimal AI agent using LangChain with Kubernetes MCP and Gemini API"""

import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def main():
    # Set up Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key=os.environ["GEMINI_API_KEY"]
    )
    
    # Connect to Kubernetes MCP server
    server_params = {
        "url": "http://127.0.0.1:8080/mcp"
    }
    
    async with streamablehttp_client(**server_params) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Load MCP tools from Kubernetes server
            tools = await load_mcp_tools(session)
            
            # Create agent with Kubernetes MCP tools
            agent = create_agent(
                model=model,
                tools=tools,
                system_prompt="You are a helpful AI assistant with access to Kubernetes cluster information."
            )
            
            # Interactive chat loop
            print("Kubernetes AI Assistant (type 'quit' to exit)")
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
                print(f"Assistant: {response['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())
