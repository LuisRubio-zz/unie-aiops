import google.generativeai as genai
import json
from flask import Flask, request, jsonify
import os

class A2AAgent:
    def __init__(self, agent_id, port, api_key, system_prompt=""):
        self.agent_id = agent_id
        self.port = port
        self.app = Flask(__name__)
        self.system_prompt = system_prompt
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/message', methods=['POST'])
        def receive_message():
            data = request.json
            response = self.process_message(data)
            return jsonify(response)
    
    def process_message(self, message):
        prompt = f"{self.system_prompt}\n\nMessage: {json.dumps(message)}\nRespond with JSON format."
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "agent_id": self.agent_id,
                "response": response.text,
                "status": "success"
            }
        except Exception as e:
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "status": "error"
            }
    
    def send_instruction(self, instruction):
        try:
            response = self.model.generate_content(f"{self.system_prompt}\n\nInstruction: {instruction}")
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_server(self):
        self.app.run(host='localhost', port=self.port, debug=False)