#!/usr/bin/env python3
"""
Trading212 MCP Server Entry Point
Run this file to start the Trading212 MCP server
"""

import uvicorn
from app.server import app

if __name__ == "__main__":
    print("Starting Trading212 MCP Server...")
    print("Visit http://localhost:8000/docs for API documentation")
    uvicorn.run(app, host="127.0.0.1", port=8000)