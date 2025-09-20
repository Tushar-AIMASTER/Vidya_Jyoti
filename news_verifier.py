
import requests
import feedparser
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
import json
import logging
from urllib.parse import urljoin, urlparse
from config import Config
import time

class NewsVerifier:
    def __init__(self):
        self.config = Config()
        self.newsapi = None
        if self.config.NEWS_API_KEY and self.config.NEWS_API_KEY != 'your-newsapi-key':
            self.newsapi = NewsApiClient(api_key=self.config.NEWS_API_KEY)
        self.logger = logging.getLogger(__name__)
        
    def verify_headline(self, headline):
        """Main verification function"""
        verification_result = {
            'headline': headline,
            'authenticity_score': 0,
            'verification_status': 'Unknown',
            'sources_found': [],
            'similar_headlines': [],
            'summary': {
                'what_happened': '',
                'when_happened': '',
                'where_happened': '',
                'why_happened': ''
            },
            'details': {
                'total_sources_checked': 0,
                'matching_sources': 0,
                'fact_check_results': [],
                'verification_method': []
            }
        }
        
        try:
            # Step 1: Search using NewsAPI (if available)
            if self.newsapi:
                verification_result = self._verify_with_newsapi(headline, verification_result)
            
            # Step 2: Search using RSS feeds and web scraping
            verification_result = self._verify_with_rss_feeds(headline, verification_result)
            
            # Step 3: Check fact-checking websites
            verification_result = self._check_fact_checking_sites(headline, verification_result)
            
            # Step 4: Calculate final authenticity score
            verification_result = self._calculate_authenticity_score(verification_result)
            
            # Step 5: Generate summary
            verification_result = self._generate_summary(verification_result)
            
        except Exception as e:
            self.logger.error(f"Error in headline verification: {str(e)}")
            verification_result['verification_status'] = 'Error'
            verification_result['error'] = str(e)
        
        return verification_result
    
    def _verify_with_newsapi(self, headline, result):
        """Verify headline using NewsAPI"""
        try:
            self.logger.info("Verifying with NewsAPI...")
            result['details']['verification_method'].append('NewsAPI')
            
            # Extract keywords from headline for search
            keywords = self._extract_keywords(headline)
            
            # Ensure we have a valid search query
            if not keywords or len(keywords) < 1:
                # Fallback: use first few words of headline
                words = headline.split()[:3]
                search_query = ' '.join(words)
            else:
                # Use only the most important keywords (max 3) to avoid overly specific searches
                search_query = ' '.join(keywords[:3])
            
            self.logger.info(f"Searching NewsAPI with query: '{search_query}'")
            
            # Search for articles
            articles = self.newsapi.get_everything(
                q=search_query,
                language='en',
                sort_by='relevancy',
                page_size=20
            )
            
            result['details']['total_sources_checked'] += len(articles['articles'])
            
            for article in articles['articles']:
                try:
                    # Use multiple similarity methods for better matching
                    title = article['title'].lower()
                    headline_lower = headline.lower()
                    
                    ratio = fuzz.ratio(headline_lower, title)
                    partial = fuzz.partial_ratio(headline_lower, title)
                    token_sort = fuzz.token_sort_ratio(headline_lower, title)
                    
                    # Use the highest similarity score
                    similarity = max(ratio, partial, token_sort)
                    
                    self.logger.info(f"Article similarity: {similarity}% (ratio:{ratio}, partial:{partial}, token:{token_sort}) - {article['title'][:50]}...")
                    
                    if similarity > 35:  # Much lower threshold for better matching
                        self.logger.info(f"Adding matching source: {article['source']['name']}")
                        result['sources_found'].append({
                            'source': article['source']['name'],
                            'title': article['title'],
                            'url': article['url'],
                            'published_at': article['publishedAt'],
                            'similarity_score': similarity,
                            'description': article['description']
                        })
                        
                        result['similar_headlines'].append({
                            'title': article['title'],
                            'similarity': similarity,
                            'source': article['source']['name']
                        })
                        
                        result['details']['matching_sources'] += 1
                except Exception as e:
                    self.logger.error(f"Error processing article: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"NewsAPI verification failed: {str(e)}")
            result['details']['newsapi_error'] = str(e)
        
        return result
    
    def _verify_with_rss_feeds(self, headline, result):
        """Verify headline using RSS feeds and web scraping"""
        try:
            self.logger.info("Verifying with RSS feeds...")
            result['details']['verification_method'].append('RSS_Feeds')
            
            keywords = self._extract_keywords(headline)
            
            for feed_url in self.config.NEWS_SOURCES:
                try:
                    feed = feedparser.parse(feed_url)
                    result['details']['total_sources_checked'] += len(feed.entries)
                    
                    for entry in feed.entries:
                        # Use multiple similarity methods for better matching
                        entry_title = entry.title.lower()
                        headline_lower = headline.lower()
                        
                        ratio = fuzz.ratio(headline_lower, entry_title)
                        partial = fuzz.partial_ratio(headline_lower, entry_title)
                        token_sort = fuzz.token_sort_ratio(headline_lower, entry_title)
                        
                        # Use the highest similarity score
                        similarity = max(ratio, partial, token_sort)
                        
                        if similarity > 30:  # Lower threshold for RSS feeds
                            result['sources_found'].append({
                                'source': feed.feed.get('title', 'RSS Feed'),
                                'title': entry.title,
                                'url': entry.link,
                                'published_at': entry.get('published', ''),
                                'similarity_score': similarity,
                                'description': entry.get('summary', '')
                            })
                            
                            result['similar_headlines'].append({
                                'title': entry.title,
                                'similarity': similarity,
                                'source': feed.feed.get('title', 'RSS Feed')
                            })
                            
                            result['details']['matching_sources'] += 1
                
                except Exception as e:
                    self.logger.warning(f"Failed to parse RSS feed {feed_url}: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"RSS feed verification failed: {str(e)}")
        
        return result
    
    def _check_fact_checking_sites(self, headline, result):
        """Check fact-checking websites"""
        try:
            self.logger.info("Checking fact-checking sites...")
            result['details']['verification_method'].append('Fact_Check')
            
            keywords = self._extract_keywords(headline)
            search_terms = ' '.join(keywords[:3])
            
            for fact_site in self.config.FACT_CHECK_SOURCES:
                try:
                    # Simple Google search for fact-check results
                    search_url = f"https://www.google.com/search?q=site:{fact_site} {search_terms}"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(search_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        search_results = soup.find_all('h3')
                        
                        if len(search_results) > 0:
                            result['details']['fact_check_results'].append({
                                'site': fact_site,
                                'results_found': len(search_results),
                                'status': 'Found related fact-checks'
                            })
                
                except Exception as e:
                    self.logger.warning(f"Failed to check {fact_site}: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Fact-checking failed: {str(e)}")
        
        return result
    
    def _calculate_authenticity_score(self, result):
        """Calculate overall authenticity score"""
        score = 0
        
        # Base score from number of matching sources
        matching_sources = result['details']['matching_sources']
        if matching_sources >= 3:
            score += 50
        elif matching_sources >= 2:
            score += 35
        elif matching_sources >= 1:
            score += 20
        
        # Score from similarity scores
        if result['similar_headlines']:
            avg_similarity = sum(h['similarity'] for h in result['similar_headlines']) / len(result['similar_headlines'])
            score += int(avg_similarity * 0.4)  # Max 40 points from similarity
        
        # Score from reputable sources
        reputable_sources = ['BBC', 'Reuters', 'AP', 'CNN', 'NPR']
        for source in result['sources_found']:
            if any(rep in source['source'] for rep in reputable_sources):
                score += 10
                break
        
        # Score from fact-checking results
        if result['details']['fact_check_results']:
            score += 10
        
        # Ensure score is within 0-100 range
        score = min(100, max(0, score))
        result['authenticity_score'] = score
        
        # Determine verification status
        if score >= 80:
            result['verification_status'] = 'Highly Likely True'
        elif score >= 60:
            result['verification_status'] = 'Likely True'
        elif score >= 40:
            result['verification_status'] = 'Possibly True'
        elif score >= 20:
            result['verification_status'] = 'Questionable'
        else:
            result['verification_status'] = 'Likely False or Unverified'
        
        return result
    
    def _generate_summary(self, result):
        """Generate What, When, Where, Why summary"""
        if not result['sources_found']:
            return result
        
        # Analyze the most similar source
        best_source = max(result['sources_found'], key=lambda x: x['similarity_score'])
        
        # Extract What happened
        result['summary']['what_happened'] = f"Based on verification, the headline appears to be related to: {best_source['title']}"
        
        # Extract When happened
        if best_source.get('published_at'):
            try:
                pub_date = best_source['published_at']
                if isinstance(pub_date, str):
                    # Try to parse the date
                    result['summary']['when_happened'] = f"Originally reported around: {pub_date}"
                else:
                    result['summary']['when_happened'] = f"Originally reported around: {pub_date}"
            except:
                result['summary']['when_happened'] = "Date information not available"
        
        # Extract Where happened
        description = best_source.get('description', '')
        if description:
            # Simple location extraction (can be improved with NLP)
            locations = re.findall(r'\b(?:in|at)\s+([A-Z][a-zA-Z\s]+?)(?:[,.]|\s+(?:said|reported|according))', description)
            if locations:
                result['summary']['where_happened'] = f"Location mentioned: {locations[0].strip()}"
            else:
                result['summary']['where_happened'] = "Location information not clearly specified"
        
        # Extract Why happened
        if description and len(description) > 50:
            result['summary']['why_happened'] = f"Context: {description[:200]}..."
        else:
            result['summary']['why_happened'] = "Additional context not available from sources"
        
        return result
    
    def _extract_keywords(self, text):
        """Extract keywords from text"""
        # Remove common stop words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'breaking', 'news', 'update', 'report', 'says', 'share', 'warm', 'hugs', 'snubbing', 'after', 'with', 'in', 'after', 'leaves', 'two', 'jawans', 'dead', 'locals', 'protest', 'nambol', 'assam', 'rifles', 'ambush'}
        
        # Clean and split text
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Prioritize important keywords (nouns, locations, events)
        priority_keywords = []
        for word in keywords:
            if len(word) > 4 or word in ['war', 'fire', 'crash', 'storm', 'flood', 'covid', 'virus', 'india', 'manipur', 'assam', 'kashmir', 'pakistan', 'china', 'bengal', 'maharashtra', 'gujarat', 'rajasthan', 'punjab', 'haryana', 'delhi', 'mumbai', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'ahmedabad', 'pune', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'indore', 'bhopal', 'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan', 'vasai', 'varanasi', 'srinagar', 'aurangabad', 'navi', 'solapur', 'vadodara', 'patna', 'meerut', 'rajkot', 'kalyan', 'vasai', 'varanasi', 'srinagar', 'aurangabad', 'navi', 'solapur', 'vadodara', 'patna']:
                priority_keywords.append(word)
        
        # Return priority keywords first, then others
        result = priority_keywords + [w for w in keywords if w not in priority_keywords]
        return result[:10]  # Return top 10 keywords
