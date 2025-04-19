import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
import os

def get_medium_articles(query="AI in radiology", max_articles=5):
    """Scrape Medium articles based on search query"""
    base_url = "https://medium.com/_/api/search/posts"
    params = {
        "query": query,
        "max": max_articles,
        "collection": "latest"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for post in data['payload']['references']['Post'].values():
            if 'title' in post and 'mediumUrl' in post:
                articles.append({
                    'title': post['title'],
                    'url': f"https://medium.com/{post['mediumUrl']}",
                    'source': 'Medium',
                    'published': datetime.fromtimestamp(post['firstPublishedAt']/1000).strftime('%Y-%m-%d')
                })
        return articles
    except Exception as e:
        print(f"Error fetching Medium articles: {e}")
        return []

def get_papers_with_code():
    """Get latest papers from Papers With Code in medical imaging"""
    url = "https://paperswithcode.com/rss"
    try:
        feed = feedparser.parse(url)
        papers = []
        
        for entry in feed.entries:
            # Filter for medical imaging/AI in radiology
            if any(term in entry.title.lower() or term in entry.summary.lower() 
                   for term in ['radiology', 'medical imaging', 'health data', 'x-ray', 'mri', 'ct scan']):
                papers.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': 'Papers With Code',
                    'published': entry.published
                })
        return papers
    except Exception as e:
        print(f"Error fetching Papers With Code: {e}")
        return []

def select_article_to_send(articles):
    """Select the most recent article not sent before"""
    # In a real implementation, you'd check against a database of sent articles
    # For simplicity, we'll just pick the most recent one
    if not articles:
        return None
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x.get('published', ''), reverse=True)
    return articles[0]
