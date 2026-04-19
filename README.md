# Trading212 MCP Server

A Model Context Protocol (MCP) server that provides Claude Desktop with access to Trading212 portfolio data including positions, account balance, and rate limiting status.

## Features

- **Account Summary**: Get comprehensive account information including cash balances and investment performance
- **Portfolio Positions**: Fetch all current positions with detailed instrument information
- **Rate Limiting**: Built-in rate limiting with Trading212 API headers and configurable backoff
- **Real-time Monitoring**: Rate limit status endpoint for monitoring API usage
- **Read-only Operations**: All tools are read-only and do not modify your Trading212 account

## Project Structure

```
/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── server.py                # FastMCP server with tool definitions
│   ├── models.py                # Pydantic response models  
│   └── clients/                 # API clients
│       ├── __init__.py         
│       └── trading212.py        # Trading212 API client with rate limiting
├── config/                      # Configuration files
│   └── trading212_config.json   # API credentials and settings
├── requirements.txt             # Python dependencies
├── run.py                      # Server entry point
├── README.md                   # This file
└── venv/                       # Virtual environment
```

## Setup

1. **Configure API Credentials**
   
   Edit `config/trading212_config.json` with your Trading212 API credentials:
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

## Development and Testing

### MCP Inspector
For development and testing of the MCP tools, you can use the official MCP inspector:

```bash
npx @modelcontextprotocol/inspector python run.py
```

This provides a web interface to test and debug your MCP server tools interactively.

### Manual Testing
You can also test the server directly:
```bash
python run.py
```

## Claude Desktop Integration

To connect this MCP server to Claude Desktop, add the following to your Claude Desktop MCP configuration file:

**Location**: 
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration**:
```json
{
  "mcpServers": {
    "trading212": {
      "command": "python",
      "args": ["/absolute/path/to/your/project/run.py"],
      "cwd": "/absolute/path/to/your/project"
    }
  }
}
```

Replace the paths with your actual project location.

## Available MCP Tools

All tools are **read-only** and **safe** - they only fetch data and never modify your Trading212 account.

### `get_balance`
**Description**: Get comprehensive Trading212 account summary  
**Parameters**: None  
**Returns**: Account balance including:
- `cash`: Available cash, amount in pies, reserved for orders
- `investments`: Current value, realized/unrealized P&L, total cost
- `totalValue`: Overall account value
- `currency`: Account currency (e.g., "GBP")
- `id`: Account ID

### `get_positions` 
**Description**: Get all current portfolio positions  
**Parameters**: None  
**Returns**: List of positions including:
- `instrument`: Ticker, company name, currency, ISIN
- `quantity`: Shares owned, available for trading, in pies
- `averagePrice`: Average purchase price per share
- `currentPrice`: Current market price per share
- `ppl`: Profit/loss for this position
- `currentValue`: Total current value of position
- `totalCost`: Total amount paid for position

### `get_rate_limit_status`
**Description**: Get current Trading212 API rate limit status  
**Parameters**: None  
**Returns**: Rate limiting information including:
- `limit`: Total requests allowed per period
- `remaining`: Remaining requests in current period  
- `reset_timestamp`: When the limit resets (Unix timestamp)
- `reset_in_seconds`: Seconds until limit resets
- `period`: Rate limit period duration
- `used`: Requests used in current period

## Rate Limiting

The server implements intelligent rate limiting based on Trading212's response headers:
- **Proactive Management**: Tracks remaining requests and reset times
- **Exponential Backoff**: Implements backoff when approaching limits
- **Configurable**: Safety margins and delay parameters via config
- **Thread-safe**: Safe for concurrent requests from Claude Desktop

### Rate Limiting Configuration

In `config/trading212_config.json`:
```json
{
  "rate_limiting": {
    "safety_margin": 0.1,      // Start backoff at 10% remaining requests
    "min_delay": 1.0,          // Minimum delay in seconds  
    "backoff_factor": 2.0      // Exponential backoff multiplier
  }
}
```

## Security

- **Local Only**: Server runs locally on your machine
- **Direct API**: Only communicates with Trading212 API using your credentials
- **No Data Storage**: No persistent data storage or caching
- **No Third Parties**: No data transmitted to external services
- **Read-only**: All operations are read-only, cannot modify your account

## Technical Details

The project uses:
- **FastMCP**: Model Context Protocol server framework
- **Pydantic**: Data validation and serialization
- **Requests**: HTTP API calls to Trading212
- **Threading**: Thread-safe rate limiting
- **JSON Config**: Simple configuration management

## Troubleshooting

### Common Issues

1. **"Trading212 API not initialized"**
   - Check your API credentials in `config/trading212_config.json`
   - Ensure the config file exists and has valid JSON syntax

2. **Rate limit warnings**
   - The server will automatically handle rate limiting
   - Consider increasing `safety_margin` in config if warnings are frequent

3. **MCP connection issues**
   - Verify the absolute paths in Claude Desktop config
   - Check that Python and dependencies are available
   - Test with MCP inspector first: `npx @modelcontextprotocol/inspector python run.py`