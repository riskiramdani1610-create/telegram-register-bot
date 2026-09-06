# Main Bot File
import logging
from telegram.ext import Application, ConversationHandler, MessageHandler, CommandHandler, filters
from config import TELEGRAM_TOKEN
from handlers.user_handler import UserHandler, START, BIND_PHONE, BIND_PASSWORD, REAL_PHONE, OTP_CODE, CONFIRM

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Start the bot"""
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Initialize handlers
    user_handler = UserHandler()
    
    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', user_handler.start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.confirm_start)],
            BIND_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.handle_bind_phone)],
            BIND_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.handle_password)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.confirm_bind)],
            REAL_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.handle_real_phone)],
            OTP_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_handler.handle_otp)],
        },
        fallbacks=[CommandHandler('cancel', user_handler.cancel)],
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    
    # Start bot
    logger.info("🚀 Bot starting...")
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
