from specialized_agents import TaskAgent, DataAgent, CoordinatorAgent
import threading
import time
import os

def start_agent(agent):
    agent.start_server()

def main():
    # Get API key from environment or prompt
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    # Create agents
    task_agent = TaskAgent(api_key)
    data_agent = DataAgent(api_key)
    coordinator = CoordinatorAgent(api_key)
    
    # Start agents in threads
    agents = [task_agent, data_agent, coordinator]
    threads = []
    
    for agent in agents:
        thread = threading.Thread(target=start_agent, args=(agent,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    time.sleep(3)  # Wait for servers to start
    
    print("A2A Protocol with Gemini AI Started")
    print("=" * 40)
    
    # Demo instructions
    instructions = [
        "Analyze customer data and create a task plan",
        "Process user feedback and generate insights",
        "Coordinate a data backup and validation task"
    ]
    
    for i, instruction in enumerate(instructions, 1):
        print(f"\n{i}. Instruction: {instruction}")
        print("-" * 30)
        
        # Send to coordinator
        result = coordinator.coordinate_task(instruction)
        print(f"Coordination Result: {result}")
        
        time.sleep(2)
    
    print("\nAgents running. Press Ctrl+C to exit")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()