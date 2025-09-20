
import re
import requests
from datetime import datetime
import hashlib
from urllib.parse import urlparse

class NewsUtils:
    @staticmethod
    def clean_headline(headline):
        """Clean and normalize headline text"""
        # Remove extra whitespace
        headline = re.sub(r'\s+', ' ', headline.strip())
        
        # Remove special characters that might interfere with search
        headline = re.sub(r'[^a-zA-Z0-9\s\-.,!?]', '', headline)
        
        return headline
    
    @staticmethod
    def extract_entities(text):
        """Extract named entities from text (simplified version)"""
        # This is a simplified entity extraction
        # In production, you might want to use spaCy or NLTK
        
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': []
        }
        
        # Extract potential person names (capitalized words)
        person_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        entities['persons'] = re.findall(person_pattern, text)
        
        # Extract potential locations
        location_keywords = ['City', 'State', 'Country', 'Street', 'Avenue', 'Road']
        for keyword in location_keywords:
            matches = re.findall(rf'\b\w+\s+{keyword}\b', text, re.IGNORECASE)
            entities['locations'].extend(matches)
        
        # Extract dates
        date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        entities['dates'] = re.findall(date_pattern, text, re.IGNORECASE)
        
        return entities
    
    @staticmethod
    def is_url_safe(url):
        """Check if URL is safe to access"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https'] and parsed.netloc
        except:
            return False
    
    @staticmethod
    def generate_cache_key(text):
        """Generate cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def format_date(date_string):
        """Format date string to readable format"""
        try:
            # Try different date formats
            formats = [
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_string, fmt)
                    return date_obj.strftime('%B %d, %Y at %I:%M %p')
                except ValueError:
                    continue
            
            return date_string
        except:
            return "Date format unknown"
    
    @staticmethod
    def calculate_text_similarity(text1, text2):
        """Calculate similarity between two texts using multiple methods"""
        from fuzzywuzzy import fuzz
        
        # Clean texts
        text1 = NewsUtils.clean_headline(text1.lower())
        text2 = NewsUtils.clean_headline(text2.lower())
        
        # Calculate different similarity scores
        scores = {
            'ratio': fuzz.ratio(text1, text2),
            'partial_ratio': fuzz.partial_ratio(text1, text2),
            'token_sort_ratio': fuzz.token_sort_ratio(text1, text2),
            'token_set_ratio': fuzz.token_set_ratio(text1, text2)
        }
        
        # Return weighted average
        weights = {'ratio': 0.4, 'partial_ratio': 0.2, 'token_sort_ratio': 0.2, 'token_set_ratio': 0.2}
        weighted_score = sum(scores[key] * weights[key] for key in scores)
        
        return {
            'overall_similarity': round(weighted_score, 2),
            'individual_scores': scores
        }



