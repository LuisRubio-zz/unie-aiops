from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)
tickets = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ticketing System</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .ticket { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
        .message { background: #f0f0f0; padding: 5px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Ticketing System</h1>
    <div id="tickets">
        {% for ticket in tickets %}
        <div class="ticket">
            <strong>Ticket #{{ ticket.id }}</strong> - {{ ticket.timestamp }}<br>
            <div class="message">{{ ticket.message }}</div>
        </div>
        {% endfor %}
    </div>
    <script>
        setInterval(() => location.reload(), 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tickets=tickets)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    ticket = {
        'id': len(tickets) + 1,
        'message': data.get('message', 'No message'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tickets.append(ticket)
    print(f"New ticket: {ticket['message']}")
    return jsonify(ticket)

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)