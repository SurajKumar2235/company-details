from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from company_insight_service.config.settings import settings

DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ProductSentiment(Base):
    __tablename__ = "product_sentiments"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    product_name = Column(String)
    sentiment_score = Column(Float) # -1.0 to 1.0
    sentiment_label = Column(String) # Positive, Negative, Neutral
    similarity_score = Column(Float, nullable=True) # 0.0 to 1.0
    summary = Column(Text)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class FinancialReport(Base):
    __tablename__ = "financial_reports"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    period = Column(String) # e.g., "Q1 2024"
    revenue = Column(String, nullable=True)
    net_income = Column(String, nullable=True)
    data = Column(JSON) # Store raw JSON of financials
    created_at = Column(DateTime, default=datetime.utcnow)

class StockAnalysis(Base):
    __tablename__ = "stock_analyses"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    ticker = Column(String)
    analysis_text = Column(Text)
    three_year_trend = Column(JSON) # JSON describing dips and rises
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
