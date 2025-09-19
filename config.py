
import os
from datetime import timedelta

class Config:
    """Configuration class for Flask app"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # News API configurations
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'your-newsapi-key'
    
    # Google Fact Check API (optional - free tier available)
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or None
    
    # Rate limiting
    REQUESTS_PER_MINUTE = 60
    
    # Verification settings
    SIMILARITY_THRESHOLD = 0.7  # Threshold for headline similarity
    MIN_SOURCES = 2  # Minimum sources required for verification
    
    # Timeout settings
    REQUEST_TIMEOUT = 30  # seconds
    
    # News sources for scraping (backup when API limits reached)
    NEWS_SOURCES = [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://rss.cnn.com/rss/edition.rss',
        'https://feeds.npr.org/1001/rss.xml',
        'https://feeds.reuters.com/reuters/topNews',
        'https://feeds.ap.org/ap/topnews',
    ]
    
    # Fact-checking sources
    FACT_CHECK_SOURCES = [
        'snopes.com',
        'factcheck.org',
        'politifact.com',
        'fullfact.org'
    ]
