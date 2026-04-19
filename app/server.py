#!/usr/bin/env python3
"""
Trading212 MCP Server
Simple Model Context Protocol server for fetching Trading212 portfolio data
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from .clients.trading212 import Trading212API
from .models import BalanceResponse, PositionsResponse, Position, Instrument, AccountSummaryResponse, RateLimitStatus

# Initialize MCP server
mcp = FastMCP("trading212")

# Initialize Trading212 API client
try:
    trading_api = Trading212API()
except Exception as e:
    trading_api = None

@mcp.tool(
    name="get_balance",
    title="Get Account Balance", 
    description="Get comprehensive Trading212 account summary including cash and investments",
    meta={"readonly": True, "category": "account"}
)
async def get_balance():
    """Get comprehensive Trading212 account summary.
    
    Returns detailed account information including cash balances, investment values,
    and overall portfolio performance. This is a read-only operation that does not
    modify your Trading212 account in any way.
    
    Returns:
        AccountSummaryResponse: Complete account summary with cash, investments, and totals
    """
    if not trading_api:
        raise RuntimeError("Trading212 API not initialized")
    
    try:
        summary_data = trading_api.get_balance()
        return AccountSummaryResponse(**summary_data)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch balance: {str(e)}")

@mcp.tool(
    name="get_positions",
    title="Get Portfolio Positions",
    description="Get all current Trading212 portfolio positions with detailed instrument information", 
    meta={"readonly": True, "category": "portfolio"}
)
async def get_positions():
    """Get all current Trading212 portfolio positions.
    
    Retrieves detailed information about all positions in your Trading212 portfolio,
    including instrument details, quantities, prices, and profit/loss calculations.
    This is a read-only operation that does not modify your Trading212 account.
    
    Returns:
        PositionsResponse: List of all portfolio positions with detailed metadata
    """
    if not trading_api:
        raise RuntimeError("Trading212 API not initialized")
    
    try:
        portfolio_data = trading_api.get_positions()
        
        if not portfolio_data:
            return PositionsResponse(positions=[], count=0)
        
        positions = []
        for pos in portfolio_data:
            instrument = pos.get('instrument', {})
            wallet_impact = pos.get('walletImpact', {})
            
            positions.append(Position(
                instrument=Instrument(
                    ticker=instrument.get('ticker', ''),
                    name=instrument.get('name', ''),
                    currency=instrument.get('currency', 'GBP'),
                    isin=instrument.get('isin', '')
                ),
                quantity=pos.get('quantity', 0),
                quantityAvailableForTrading=pos.get('quantityAvailableForTrading', 0),
                quantityInPies=pos.get('quantityInPies', 0),
                averagePrice=pos.get('averagePricePaid', 0),
                currentPrice=pos.get('currentPrice', 0),
                ppl=wallet_impact.get('unrealizedProfitLoss', 0),
                currentValue=wallet_impact.get('currentValue', 0),
                totalCost=wallet_impact.get('totalCost', 0),
                fxImpact=wallet_impact.get('fxImpact', 0),
                createdAt=pos.get('createdAt', '')
            ))
        
        return PositionsResponse(positions=positions, count=len(positions))
    except Exception as e:
        raise RuntimeError(f"Failed to fetch positions: {str(e)}")


@mcp.tool(
    name="get_rate_limit_status", 
    title="Get Rate Limit Status",
    description="Get current Trading212 API rate limit status and usage statistics",
    meta={"readonly": True, "category": "monitoring"}
)
async def get_rate_limit_status():
    """Get current Trading212 API rate limit status.
    
    Returns information about the current API rate limiting status, including
    remaining requests, reset times, and usage statistics. Useful for monitoring
    API usage and avoiding rate limit violations. This is a read-only operation.
    
    Returns:
        RateLimitStatus: Current rate limit information and timing details
    """
    if not trading_api:
        raise RuntimeError("Trading212 API not initialized")
    
    try:
        return RateLimitStatus(**trading_api.get_rate_limit_status())
    except Exception as e:
        raise RuntimeError(f"Failed to get rate limit status: {str(e)}")

if __name__ == "__main__":
    mcp.run()
    