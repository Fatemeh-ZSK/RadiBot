from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import html2text

def extract_text_from_url(url):
    """Extract main text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Medium specific extraction
        if 'medium.com' in url:
            article = soup.find('article')
            if article:
                return article.get_text()
        
        # Papers With Code specific extraction
        elif 'paperswithcode.com' in url:
            content = soup.find('div', {'class': 'paper-abstract'})
            if content:
                return content.get_text()
        
        # Fallback to html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(response.text)
    
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None

def summarize_article(text, max_length=150):
    """Generate a summary of the article text"""
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Could not generate summary for this article."

def process_article(article):
    """Full processing pipeline for an article"""
    if not article:
        return None
    
    text = extract_text_from_url(article['url'])
    if not text:
        return None
    
    summary = summarize_article(text)
    return {
        'title': article['title'],
        'url': article['url'],
        'source': article['source'],
        'published': article.get('published', 'Unknown date'),
        'summary': summary
    }
