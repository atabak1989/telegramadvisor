import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters
from bot_handlers import BotHandlers
from config import BOT_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Initialize bot handlers
    bot_handlers = BotHandlers()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_handlers.start)],
        states={
            bot_handlers.AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.age)],
            bot_handlers.MAJOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.major)],
            bot_handlers.DEGREE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.degree)],
            bot_handlers.BACHELOR_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.bachelor_field)],
            bot_handlers.MASTER_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.master_field)],
            bot_handlers.GPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.gpa)],
            bot_handlers.LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.language)],
            bot_handlers.BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.budget)],
            bot_handlers.COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.country)],
        },
        fallbacks=[CommandHandler('cancel', bot_handlers.cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', bot_handlers.help_command))
    
    # Run the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    main()
