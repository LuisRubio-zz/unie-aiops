from agent import A2AAgent
import requests
import json

class TaskAgent(A2AAgent):
    def __init__(self, api_key, port=5001):
        system_prompt = """You are a TaskAgent specialized in task management and execution.
        Respond to task requests with structured JSON containing task_id, status, and result.
        Keep responses concise and actionable."""
        super().__init__("TaskAgent", port, api_key, system_prompt)

class DataAgent(A2AAgent):
    def __init__(self, api_key, port=5002):
        system_prompt = """You are a DataAgent specialized in data analysis and retrieval.
        Respond to data requests with structured JSON containing data insights and summaries.
        Focus on providing clear, analytical responses."""
        super().__init__("DataAgent", port, api_key, system_prompt)

class CoordinatorAgent(A2AAgent):
    def __init__(self, api_key, port=5003):
        system_prompt = """You are a CoordinatorAgent that orchestrates communication between other agents.
        Break down complex requests into subtasks and coordinate responses.
        Provide clear coordination plans in JSON format."""
        super().__init__("CoordinatorAgent", port, api_key, system_prompt)
        self.agents = {
            "task": "http://localhost:5001",
            "data": "http://localhost:5002"
        }
    
    def coordinate_task(self, instruction):
        plan = self.send_instruction(f"Create a coordination plan for: {instruction}")
        
        # Send to TaskAgent
        task_response = requests.post(f"{self.agents['task']}/message", 
                                    json={"type": "coordination", "plan": plan})
        
        # Send to DataAgent  
        data_response = requests.post(f"{self.agents['data']}/message",
                                    json={"type": "coordination", "plan": plan})
        
        return {
            "plan": plan,
            "task_agent_response": task_response.json() if task_response.ok else "Error",
            "data_agent_response": data_response.json() if data_response.ok else "Error"
        }