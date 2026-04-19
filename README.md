# Trading212 MCP Server

A Model Context Protocol (MCP) server that provides Claude Desktop with access to Trading212 portfolio data including positions, account balance, and rate limiting status.

## Features

- **Account Summary**: Get comprehensive account information including cash balances and investment performance
- **Portfolio Positions**: Fetch all current positions with detailed instrument information
- **Rate Limiting**: Built-in rate limiting with Trading212 API headers and configurable backoff
- **Real-time Monitoring**: Rate limit status endpoint for monitoring API usage

## Project Structure

```
/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── server.py                # FastAPI MCP server
│   ├── models.py                # Pydantic response models  
│   └── clients/                 # API clients
│       ├── __init__.py         
│       └── trading212.py        # Trading212 API client
├── config/                      # Configuration files
│   └── trading212_config.json   # API credentials and settings
├── requirements.txt             # Python dependencies
├── run.py                      # Server entry point
├── README.md                   # This file
└── venv/                       # Virtual environment
```

## Setup

1. **Configure API Credentials**
   
   Create `config/trading212_config.json` with your Trading212 API credentials:
   ```json
   {
     "api_key": "your_api_key_here",
     "api_secret": "your_api_secret_here",
     "rate_limiting": {
       "safety_margin": 0.1,
       "min_delay": 1.0,
       "backoff_factor": 2.0
     }
   }
   ```

2. **Install Dependencies**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start the Server**
   ```bash
   python run.py
   ```
   
   The server will start at `http://127.0.0.1:8000`

## Claude Desktop Integration

To connect this MCP server to Claude Desktop, add the following to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "trading212": {
      "command": "python",
      "args": ["/path/to/your/project/run.py"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## Available Endpoints

### Tools (for Claude Desktop)

- **`/tools/get_balance`** - Get comprehensive account summary
- **`/tools/get_positions`** - Get all portfolio positions  
- **`/tools/get_rate_limit_status`** - Get current API rate limit status

### API Documentation

Visit `http://localhost:8000/docs` when the server is running to view the interactive API documentation.

## Rate Limiting

The server implements intelligent rate limiting based on Trading212's response headers:
- Tracks remaining requests and reset times
- Implements exponential backoff when approaching limits
- Configurable safety margins and delay parameters
- Thread-safe for concurrent requests

## Development

The project uses:
- **FastAPI** for the web server and automatic API documentation
- **Pydantic** for data validation and serialization
- **Requests** for HTTP API calls to Trading212
- **Threading** for thread-safe rate limiting

2. Configure your Trading212 API credentials in `trading212_config.json`:
```json
{
  "api_key": "your_trading212_api_key",
  "api_secret": "your_trading212_api_secret"
}
```

## Running the Server

Start the MCP server:
```bash
python server.py
```

The server will start on `http://localhost:8000`

You can view the API documentation at `http://localhost:8000/docs`

## Available Tools

### get_balance
Fetches your Trading212 account balance including:
- Total account value
- Available cash
- Total invested amount  
- Profit/Loss

### get_positions
Fetches your current portfolio positions with details for each holding:
- Ticker symbol
- Quantity held
- Average purchase price
- Current market price
- Position profit/loss
- Current market value

## Claude Desktop Integration

To use with Claude Desktop, add this server to your MCP configuration. The server exposes two tools that Claude can use to fetch your Trading212 data on demand.

## Security

This server runs locally on your machine and only communicates with the Trading212 API using your configured credentials. No data is stored or transmitted to third parties.