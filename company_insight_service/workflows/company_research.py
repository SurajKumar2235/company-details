"""
LangGraph workflow for company research
"""
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, END

from company_insight_service.services import (
    analyze_products,
    find_ticker,
    get_stock_data_analysis,
    get_latest_news
)
from company_insight_service.workers.queue_utils import publish_to_queue


class AgentState(TypedDict):
    company_name: str
    ticker: Optional[str]
    news: List[Dict]
    product_sentiment: List[Dict]
    stock_analysis: Optional[Dict]
    financials: Optional[Dict]
    errors: List[str]


def research_company_node(state: AgentState):
    """Research company news and products"""
    print(f"Researching: {state['company_name']}")
    company = state['company_name']
    news = get_latest_news(company)
    products = analyze_products(company)
    return {
        "news": news,
        "product_sentiment": products
    }


def financial_node(state: AgentState):
    """Analyze company financials and stock"""
    print(f"Analyzing Financials: {state['company_name']}")
    company = state['company_name']
    ticker = find_ticker(company)
    stock_data = None
    if ticker:
        stock_data = get_stock_data_analysis(ticker)
    
    return {
        "ticker": ticker,
        "stock_analysis": stock_data
    }


def save_node(state: AgentState):
    """Queue data for saving to database"""
    print("Queueing save operation...")
    try:
        payload = {
            "company_name": state['company_name'],
            "product_sentiment": state['product_sentiment'],
            "stock_analysis": state['stock_analysis'],
            "ticker": state['ticker']
        }
        publish_to_queue(payload)
        
    except Exception as e:
        print(f"Queueing failed: {e}")
        return {"errors": [str(e)]}
        
    return {}


def build_workflow():
    """Build and compile the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("research", research_company_node)
    workflow.add_node("financials", financial_node)
    workflow.add_node("save", save_node)
    
    workflow.set_entry_point("research")
    
    workflow.add_edge("research", "financials")
    workflow.add_edge("financials", "save")
    workflow.add_edge("save", END)
    
    return workflow.compile()


app_flow = build_workflow()
