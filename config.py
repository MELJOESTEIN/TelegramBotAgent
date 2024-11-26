import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_NAME = "expense_tracker"

# Validate environment variables
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")