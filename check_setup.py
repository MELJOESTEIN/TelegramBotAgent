import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from telegram.ext import Application
from config import MONGODB_URI, BOT_TOKEN, DATABASE_NAME

async def check_setup():
    print("🔍 Running pre-flight checks...")
    
    # 1. Check MongoDB Connection
    try:
        client = AsyncIOMotorClient(MONGODB_URI)
        await client.server_info()
        print("✅ MongoDB Connection: SUCCESS")
        print(f"📊 Using database: {DATABASE_NAME}")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {str(e)}")
        return False

    # 2. Check Telegram Token
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        bot_info = await app.bot.get_me()
        print(f"✅ Telegram Bot Connection: SUCCESS")
        print(f"🤖 Bot Name: {bot_info.first_name}")
        print(f"👤 Bot Username: @{bot_info.username}")
    except Exception as e:
        print(f"❌ Telegram Bot Token Invalid: {str(e)}")
        return False

    print("\n✅ All checks passed! You can run your bot.")
    return True

if __name__ == "__main__":
    asyncio.run(check_setup())