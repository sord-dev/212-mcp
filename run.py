#!/usr/bin/env python3
"""
Trading212 MCP Server Entry Point
Run this file to start the Trading212 MCP server
"""

from app.server import mcp

if __name__ == "__main__":
    print("Starting Trading212 MCP Server...")
    mcp.run()