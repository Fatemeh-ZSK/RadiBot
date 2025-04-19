from scraper import get_medium_articles, get_papers_with_code, select_article_to_send
from summarizer import process_article
from telegram_bot import send_telegram_message
import os

def main():
    # Get articles from all sources
    medium_articles = get_medium_articles("AI in radiology medical imaging health data")
    papers = get_papers_with_code()
    
    all_articles = medium_articles + papers
    
    # Select one article to send
    article_to_send = select_article_to_send(all_articles)
    if not article_to_send:
        print("No relevant articles found today.")
        return
    
    # Process the article (get summary)
    processed_article = process_article(article_to_send)
    if not processed_article:
        print("Failed to process article.")
        return
    
    # Send via Telegram
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram credentials not set.")
        return
    
    success = send_telegram_message(processed_article, bot_token, chat_id)
    if success:
        print("Article sent successfully!")
    else:
        print("Failed to send article.")

if __name__ == "__main__":
    main()
