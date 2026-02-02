# Company Intelligence API - Deep Analysis Version

A sophisticated FastAPI application leveraging **LangGraph**, **PostgreSQL**, and **Concurrent Scraping** to provide deep insights into companies.

## Features

*   **Deep Web Scraping**: Goes inside search result links to extract full text content.
*   **Product Sentiment Analysis**: Analyzes what people are talking about using NLP (TextBlob).
*   **Conurrent Processing**: Scrapes and analyzes multiple sources in parallel.
*   **Financial Analysis**:
    *   3-Year Stock Trend Analysis (finding dips and peaks).
    *   Seasonal pattern detection (best/worst months).
*   **Database Integration**: Stores all insights in a local PostgreSQL database.
*   **LangGraph Workflow**: Orchestrates the multi-step research process.

## Prerequisites

*   Docker (for PostgreSQL)
*   Python 3.9+

## Setup

1.  **Start Database**:
    ```bash
    cd company_insight_service
    docker-compose up -d
    ```
    This starts a PostgreSQL instance on port 5432.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Server**:
    Navigate to the parent directory (`test_kube`) and run:
    ```bash
    uvicorn company_insight_service.main:app --reload
    ```

## Usage

**Endpoint**: `POST /deep_search_company`

**Request Body**:
```json
{
  "company_name": "Tesla"
}
```

**Response**:
Returns a detailed JSON report and saves data to the `company_insights` database.

## Architecture

- **`main.py`**: API Entry point.
- **`workflow.py`**: LangGraph state machine definition.
- **`services.py`**: Core logic (Scraping, Sentiment, YFinance).
- **`database/`**: SQLAlchemy models and connection logic.
