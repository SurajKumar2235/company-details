"""
Company-related API routes
"""
import json
import asyncio
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict

from company_insight_service.services import (
    get_monthly_events,
    find_ticker,
    get_stock_data_analysis
)
from company_insight_service.workflows.company_research import app_flow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/company", tags=["company"])


class CompanyRequest(BaseModel):
    company_name: str


class MonthlyEventRequest(BaseModel):
    company_name: str
    month: str
    year: int


class StockTrendRequest(BaseModel):
    company_name: str
    years: int = 3


@router.post("/monthly_events")
async def company_monthly_events(request: MonthlyEventRequest):
    """
    Get news and events for a company during a specific month and year
    """
    if not request.company_name or not request.month or not request.year:
        raise HTTPException(
            status_code=400,
            detail="All fields (company_name, month, year) are required"
        )
    
    events = get_monthly_events(request.company_name, request.month, request.year)
    
    return {
        "company": request.company_name,
        "period": f"{request.month} {request.year}",
        "events": events
    }


@router.post("/stock_trends")
async def company_stock_trends(request: StockTrendRequest):
    """
    Analyze stock trends (dip/peak months) over a specified number of years
    """
    if not request.company_name:
        raise HTTPException(status_code=400, detail="company_name is required")
        
    ticker = find_ticker(request.company_name)
    if not ticker:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker not found for {request.company_name}"
        )
        
    analysis = get_stock_data_analysis(ticker, years=request.years)
    if not analysis:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve stock data."
        )
        
    return {
        "company": request.company_name,
        "ticker": ticker,
        "analysis": analysis
    }


@router.post("/deep_search")
async def deep_search_company(request: CompanyRequest):
    """
    Trigger the deep analysis workflow (LangGraph) and stream progress
    """
    if not request.company_name:
        raise HTTPException(status_code=400, detail="Company name is required")
    
    async def event_generator():
        initial_state = {
            "company_name": request.company_name,
            "ticker": None,
            "news": [],
            "product_sentiment": [],
            "stock_analysis": None,
            "financials": None,
            "errors": []
        }
        
        try:
            # Stream events from LangGraph
            for event in app_flow.stream(initial_state):
                for node_name, updates in event.items():
                    chunk = {
                        "event": "update",
                        "node": node_name,
                        "data": updates
                    }
                    yield json.dumps(chunk) + "\n"
                    await asyncio.sleep(0.1)
            
            yield json.dumps({
                "event": "complete",
                "message": "Workflow finished. Data queued for saving."
            }) + "\n"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield json.dumps({"event": "error", "message": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
