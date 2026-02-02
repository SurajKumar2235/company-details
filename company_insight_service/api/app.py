"""
FastAPI application initialization
"""
import logging
from fastapi import FastAPI

from company_insight_service.api.routes import company, health

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title="Company Intelligence API",
        description="Deep insights into companies using LangGraph, scraping, and sentiment analysis.",
        version="2.0.0"
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(company.router)
    
    # Import signals for DB monitoring (registers event listeners)
    try:
        from company_insight_service.core import signals
        logger.info("Database signals registered")
    except ImportError as e:
        logger.warning(f"Could not import signals: {e}")
    
    return app


# Create app instance
app = create_app()
