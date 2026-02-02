"""
Health check and status routes
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Company Intelligence API v2",
        "docs": "/docs",
        "endpoints": {
            "deep_search": "POST /company/deep_search",
            "stock_trends": "POST /company/stock_trends",
            "monthly_events": "POST /company/monthly_events"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Company Intelligence API"
    }
