import requests
import os
from scraper import get_medium_articles, get_papers_with_code, select_article_to_send
from summarizer import process_article

def handle_message(update, bot_token):
    """Handle incoming Telegram messages"""
    chat_id = update['message']['chat']['id']
    text = update['message'].get('text', '').lower()
    
    if text == 'study':
        # Get and send article
        medium_articles = get_medium_articles("AI in radiology medical imaging health data")
        papers = get_papers_with_code()
        article = select_article_to_send(medium_articles + papers)
        
        if article:
            processed = process_article(article)
            if processed:
                send_telegram_message(processed, bot_token, chat_id)
                return "📚 Article sent! Happy studying!"
        
        return "⚠️ No new articles found at the moment."
    return "Send 'study' to get a new article."

def setup_webhook(bot_token, ngrok_url=None):
    """Set up webhook for real-time updates"""
    if ngrok_url:  # For testing locally
        url = f"{ngrok_url}/webhook"
    else:  # For production (requires HTTPS)
        url = f"https://your-server.com/webhook"
    
    requests.post(
        f"https://api.telegram.org/bot{7929490695:AAEf81hJYm6ShnZO2eBTgaGOp9LV4G-roZE}/setWebhook",
        json={"url": url}
    )

def create_webhook_app(bot_token):
    """Create Flask app for webhook (for local testing)"""
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    
    @app.route('/webhook', methods=['POST'])
    def webhook():
        update = request.json
        response = handle_message(update, bot_token)
        return jsonify({"method": "sendMessage", "chat_id": update['message']['chat']['id'], "text": response})
    
    return app
