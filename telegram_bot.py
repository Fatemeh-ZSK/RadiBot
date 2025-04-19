import requests
import os

def send_telegram_message(article, bot_token, chat_id):
    """Send article summary via Telegram bot"""
    if not article:
        return False
    
    message = (
        f"📰 *{article['title']}*\n"
        f"🔗 {article['url']}\n"
        f"📅 {article['published']}\n"
        f"📚 Source: {article['source']}\n\n"
        f"📝 *Summary:*\n"
        f"{article['summary']}"
    )
    
    url = f"https://api.telegram.org/bot7929490695:AAEf81hJYm6ShnZO2eBTgaGOp9LV4G-roZE/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False
