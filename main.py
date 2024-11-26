# main.py
import asyncio
import nest_asyncio  # Add this import
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import ExpenseHandler
from telegram import Update  # Add this import

async def main():
    try:
        handler = ExpenseHandler()
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", handler.start))
        application.add_handler(CommandHandler("add", handler.add_expense))
        application.add_handler(CommandHandler("summary", handler.get_summary))
        application.add_handler(CommandHandler("categories", handler.get_categories))
        
        print("Bot is starting...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == '__main__':
    # Install nest_asyncio to allow nested event loops
    nest_asyncio.apply()
    
    try:
        # Get or create event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Run the main function
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        loop.close()