"""
RabbitMQ consumer worker
Processes messages from the queue and saves to database
"""
import pika
import json
import logging
import sys
import os
from company_insight_service.config.settings import settings, BaseSettings
from company_insight_service.config.settings import settings
from company_insight_service.database.models import (
    SessionLocal, Company, ProductSentiment, StockAnalysis, init_db
)

# Import signals to register event listeners
from company_insight_service.core import signals

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def save_data_to_db(data: dict):
    """
    Save company data to database
    
    Args:
        data: Dictionary containing company data
    """
    logger.info("Processing message from queue...")
    
    try:
        db = SessionLocal()
        company_name = data.get('company_name')
        
        if not company_name:
            logger.error("No company_name in message")
            return
            
        # Check if company exists or create
        company = db.query(Company).filter(Company.name == company_name).first()
        if not company:
            company = Company(name=company_name)
            db.add(company)
            db.commit()
            db.refresh(company)
        
        # Save Product Sentiments
        product_sentiments = data.get('product_sentiment', [])
        for prod in product_sentiments:
            sentiment = ProductSentiment(
                company_id=company.id,
                product_name=prod.get('title', 'Unknown'),
                sentiment_score=prod.get('sentiment_score', 0.0),
                sentiment_label=prod.get('sentiment_label', 'Neutral'),
                similarity_score=prod.get('similarity_score', None),
                summary=prod.get('summary', ''),
                source_url=prod.get('link', '')
            )
            db.add(sentiment)
            
        # Save Stock Analysis
        stock_analysis = data.get('stock_analysis')
        ticker = data.get('ticker')
        if stock_analysis:
            analysis = StockAnalysis(
                company_id=company.id,
                ticker=ticker,
                analysis_text=f"Trend: {stock_analysis.get('overall_change_percent', 0)}%",
                three_year_trend=stock_analysis
            )
            db.add(analysis)
            
        db.commit()
        db.close()
        logger.info(f"Successfully saved data for {company_name}")
        
    except Exception as e:
        logger.error(f"Database save failed: {e}")


def main():
    """Main worker function"""
    # Ensure tables exist
    init_db()
    
    params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)
    
    def callback(ch, method, properties, body):
        message = json.loads(body)
        save_data_to_db(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=settings.RABBITMQ_QUEUE_NAME,
        on_message_callback=callback
    )

    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
