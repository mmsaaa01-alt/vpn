# main.py
import logging
import os
from threading import Thread
from flask import Flask
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

# --- Flask Web Server for UptimeRobot (Keeps Render Free Instance Alive) ---
app = Flask("")

@app.route("/")
def home():
    return "Bot is active and running!"

def run_web():
    # Render binds services to port 10000 by default or uses PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# --------------------------------------------------------------------------

def main():
    # Start the Flask web server in a separate background thread
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    # Fix connection timeouts
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app_bot = ApplicationBuilder().token(BOT_TOKEN).request(request).build()
    
    # Register commands
    app_bot.add_handler(CommandHandler("start", start_command))
    app_bot.add_handler(CommandHandler("status", status_command))
    app_bot.add_handler(CommandHandler("curriculum", curriculum_command))
    app_bot.add_handler(CommandHandler("whattostudy", what_to_study_command))
    app_bot.add_handler(CommandHandler("calendar", calendar_command))
    app_bot.add_handler(CallbackQueryHandler(button_callback))
    
    # Setup the 6 PM reminder (Make sure ADMIN_CHAT_ID is set in config.py!)
    if ADMIN_CHAT_ID:
        setup_6pm_reminder(app_bot, int(ADMIN_CHAT_ID))
        
    print("🤖 Ethiopian Student Speedrun Bot is running publicly... 🚀🔥")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
