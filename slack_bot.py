"""
Slack bot integration
"""
import os
import logging
from slack_bolt import App
from agent import handle_user_input

logger = logging.getLogger(__name__)

# Initialize Slack app
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if BOT_TOKEN and SIGNING_SECRET:
    app = App(token=BOT_TOKEN, signing_secret=SIGNING_SECRET)
    
    @app.message(".*")
    def handle_message(message, say):
        """Handle messages in Slack"""
        try:
            user_message = message['text']
            user_id = message['user']
            
            # Get AI response
            response = handle_user_input(user_message)
            
            # Send to Slack
            say(response)
            
            logger.info(f"Slack message from {user_id}: {user_message}")
        except Exception as e:
            logger.error(f"Slack bot error: {e}")
            say("Sorry, there was an error processing your message.")
    
    @app.event("app_mention")
    def handle_mention(body, say):
        """Handle mentions of the bot"""
        text = body['event']['text']
        # Remove bot mention
        user_message = text.split('>')[1].strip() if '>' in text else text
        response = handle_user_input(user_message)
        say(response)
else:
    app = None
    logger.warning("Slack bot not configured")
