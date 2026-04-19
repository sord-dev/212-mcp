#!/usr/bin/env python3
"""
Trading212 MCP Server
Simple Model Context Protocol server for fetching Trading212 portfolio data
"""

from mcp.server.fastmcp import FastMCP
from .clients.trading212 import Trading212API
from .models import BalanceResponse, PositionsResponse, Position, Instrument, AccountSummaryResponse, RateLimitStatus

# Initialize MCP server
mcp = FastMCP("trading212")

# Initialize Trading212 API client
try:
    trading_api = Trading212API()
except Exception as e:
    trading_api = None

@mcp.tool("get_balance")
async def get_balance():
    """Get Trading212 account summary including cash and investments"""
    if not trading_api:
        raise RuntimeError("Trading212 API not initialized")
    
    try:
        summary_data = trading_api.get_balance()
        return AccountSummaryResponse(**summary_data)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch balance: {str(e)}")

@mcp.tool("get_positions")
async def get_positions():
    """Get Trading212 portfolio positions"""
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


@mcp.tool("get_rate_limit_status")
async def get_rate_limit_status():
    """Get current rate limit status for Trading212 API"""
    if not trading_api:
        raise RuntimeError("Trading212 API not initialized")
    
    try:
        return RateLimitStatus(**trading_api.get_rate_limit_status())
    except Exception as e:
        raise RuntimeError(f"Failed to get rate limit status: {str(e)}")

if __name__ == "__main__":
    mcp.run()
    