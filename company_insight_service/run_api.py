#!/usr/bin/env python
"""
API server entry point
"""
import uvicorn
from company_insight_service.config.settings import settings


def main():
    """Start the API server"""
    use_reload = settings.API_WORKERS == 1
    
    uvicorn.run(
        "company_insight_service.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=use_reload,
        workers=settings.API_WORKERS
    )


if __name__ == "__main__":
    main()
