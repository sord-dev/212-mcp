"""
Pydantic models for Trading212 MCP Server
Response models and data structures
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class CashInfo(BaseModel):
    availableToTrade: float = 0
    inPies: float = 0  
    reservedForOrders: float = 0


class InvestmentInfo(BaseModel):
    currentValue: float = 0
    realizedProfitLoss: float = 0
    totalCost: float = 0
    unrealizedProfitLoss: float = 0


class AccountSummaryResponse(BaseModel):
    cash: CashInfo
    currency: str
    id: int
    investments: InvestmentInfo
    totalValue: float


class RateLimitStatus(BaseModel):
    limit: Optional[int] = None
    remaining: Optional[int] = None
    reset_timestamp: Optional[int] = None
    reset_in_seconds: Optional[int] = None
    period: Optional[int] = None
    used: Optional[int] = None


class BalanceResponse(BaseModel):
    total: float
    free: float
    invested: float
    ppl: float
    currency: str


class Instrument(BaseModel):
    ticker: str = ""
    name: str = ""
    currency: str = "GBP"
    isin: str = ""


class Position(BaseModel):
    instrument: Instrument
    quantity: float = 0
    quantityAvailableForTrading: float = 0
    quantityInPies: float = 0
    averagePrice: float = 0
    currentPrice: float = 0
    ppl: float = 0
    currentValue: float = 0
    totalCost: float = 0
    fxImpact: Optional[float] = 0
    createdAt: str = ""


class PositionsResponse(BaseModel):
    positions: List[Position]
    count: int