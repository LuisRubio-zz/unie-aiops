import requests
import json

def test_ticketing_system():
    base_url = "http://localhost:5000"
    
    # Test messages
    messages = [
        "System error in payment module",
        "User login issue reported",
        "Database connection timeout"
    ]
    
    print("Testing Ticketing System REST API")
    print("=" * 40)
    
    for msg in messages:
        response = requests.post(f"{base_url}/api/tickets", 
                               json={"message": msg})
        if response.ok:
            ticket = response.json()
            print(f"Created ticket #{ticket['id']}: {ticket['message']}")
        else:
            print(f"Error creating ticket: {response.status_code}")
    
    # Get all tickets
    response = requests.get(f"{base_url}/api/tickets")
    if response.ok:
        tickets = response.json()
        print(f"\nTotal tickets: {len(tickets)}")

if __name__ == "__main__":
    test_ticketing_system()