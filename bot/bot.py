import json
import logging
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from rabbitmq import send_feedback_to_rabbitmq
from utils import get_env_variable

# Get the Telegram bot token and bot username from environment variables
TOKEN: Final = get_env_variable('TOKEN')
BOT_USERNAME: Final = get_env_variable('BOT_USERNAME')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command Handlers 
async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text('Hello! I am a bot that will help you to send feedback to the TimelyAI team. Please send your feedback in the text format')


async def help_command(update: Update, context: ContextTypes):
    await update.message.reply_text('How can I assist you? Please let me know if you have any questions or need help with anything.')


async def about_command(update: Update, context: ContextTypes):
    await update.message.reply_text('TimelyAI is an AI-powered platform that provides various services. This feedback bot is designed to collect feedback from users like you. We appreciate your input!')


async def stop_command(update: Update, context: ContextTypes):
    await update.message.reply_text('You have stopped the current interaction. If you have any further questions or feedback, feel free to reach out to us again.')


async def handle_feedback(update: Update, context: ContextTypes):
    feedback = update.message.text
    date_time = update.message.date
    username = update.message.from_user.first_name
    user_id = update.message.from_user.id

    # Create a dictionary to store the feedback data
    feedback_data = {
        "feedback": feedback,
        "date_time": str(date_time),
        "username": username,
        "user_id": user_id
    }
    feedback_json = json.dumps(feedback_data)
    print(feedback_json)
    send_feedback_to_rabbitmq(feedback_json)
    
    await update.message.reply_text('Thank you for your feedback!')

# Error handler
async def error(update: Update, context: ContextTypes):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    # Create a Telegram bot application
    app = Application.builder().token(TOKEN).build() 
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))
    app.add_handler(CommandHandler('stop', stop_command))
    app.add_handler(MessageHandler(filters.ALL, handle_feedback))
    app.add_error_handler(error)
    app.run_polling()

