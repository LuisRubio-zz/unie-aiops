# Ticketing System

A minimal ticketing system with HTML interface and REST API that displays messages on screen.

## Features

- HTML page showing all tickets
- REST API for creating and retrieving tickets
- Auto-refresh every 5 seconds
- Console logging of new tickets

## Setup

1. Create conda environment:
```bash
conda env create -f environment.yml
conda activate ticketing-system
```

2. Run the application:
```bash
python app.py
```

3. Open browser: http://localhost:5000

## REST API

- **POST /api/tickets** - Create ticket
  ```json
  {"message": "Your ticket message"}
  ```

- **GET /api/tickets** - Get all tickets

## Test

Run the test client:
```bash
python test_client.py
```

Or use curl:
```bash
# Create a ticket
curl -X POST http://localhost:5000/api/tickets -H "Content-Type: application/json" -d '{"message": "System error reported"}'

# Get all tickets
curl http://localhost:5000/api/tickets
```