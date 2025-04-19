from telegram_bot import setup_webhook, create_webhook_app
import os

def scheduled_delivery():
    """Original daily delivery functionality"""
    # ... (keep your existing code)

def main():
    bot_token = os.getenv('7929490695:AAEf81hJYm6ShnZO2eBTgaGOp9LV4G-roZE')
    
    # Run scheduled delivery if triggered by cron
    if os.getenv('GITHUB_ACTIONS') == 'true':
        scheduled_delivery()
    # Local development with webhook
    else:
        app = create_webhook_app(bot_token)
        print("Starting webhook server...")
        app.run(port=5000)

if __name__ == "__main__":
    main()
