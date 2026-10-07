# main.py
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram.request import HTTPXRequest
from config import BOT_TOKEN, ADMIN_CHAT_ID
from handlers import (
    start_command, status_command, curriculum_command,
    what_to_study_command, calendar_command, button_callback
)
# Import the new reminder setup function
from reminders import setup_6pm_reminder 

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    # Fix connection timeouts
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()
    
    # Register commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("curriculum", curriculum_command))
    app.add_handler(CommandHandler("whattostudy", what_to_study_command))
    app.add_handler(CommandHandler("calendar", calendar_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Setup the 6 PM reminder (Make sure ADMIN_CHAT_ID is set in config.py!)
    if ADMIN_CHAT_ID:
        setup_6pm_reminder(app, int(ADMIN_CHAT_ID))
        
    print("🤖 Ethiopian Student Speedrun Bot is running publicly... 🚀🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
