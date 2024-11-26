# handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from models import Expense, ExpenseSummary, CategorySummary
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ExpenseHandler:
    def __init__(self):
        self.db = Database()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        await update.message.reply_text(
            "👋 Welcome to ExpenseTracker Bot!\n\n"
            "Commands:\n"
            "💰 /add amount category note - Add expense\n"
            "📊 /summary - Get monthly summary\n"
            "📋 /categories - View spending by category\n\n"
            "Example: /add 20.50 food lunch"
        )

    async def add_expense(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /add command"""
        try:
            # Validate input
            if not context.args or len(context.args) < 2:
                await update.message.reply_text(
                    "Please provide amount and category.\n"
                    "Example: /add 20.50 food lunch"
                )
                return

            # Parse amount
            try:
                amount = float(context.args[0])
                if amount <= 0:
                    await update.message.reply_text("Amount must be greater than 0")
                    return
            except ValueError:
                await update.message.reply_text("Invalid amount. Please use numbers only.")
                return

            category = context.args[1].lower()
            note = ' '.join(context.args[2:]) if len(context.args) > 2 else None
            
            await self.db.add_expense(update.effective_user.id, amount, category, note)
            await update.message.reply_text(
                f"✅ Added expense:\n"
                f"Amount: ${amount:.2f}\n"
                f"Category: {category}\n"
                f"Note: {note if note else 'N/A'}"
            )
            
        except Exception as e:
            logger.error(f"Error adding expense: {str(e)}")
            await update.message.reply_text(
                "Sorry, there was an error adding your expense. Please try again."
            )

    async def get_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /summary command"""
        try:
            summary = await self.db.get_monthly_summary(update.effective_user.id)
            if summary:
                await update.message.reply_text(
                    f"📊 Monthly Summary\n\n"
                    f"💰 Total Spent: ${summary.total:.2f}\n"
                    f"🧾 Number of Expenses: {summary.count}"
                )
            else:
                await update.message.reply_text("No expenses recorded this month.")
        except Exception as e:
            logger.error(f"Error getting summary: {str(e)}")
            await update.message.reply_text(
                "Sorry, there was an error getting your summary. Please try again."
            )

    async def get_categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /categories command"""
        try:
            categories = await self.db.get_category_summary(update.effective_user.id)
            if categories:
                response = "📋 Spending by Category:\n\n"
                for cat in categories:
                    response += f"🔹 {cat.category}: ${cat.total:.2f} ({cat.percentage:.1f}%)\n"
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("No expenses recorded this month.")
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            await update.message.reply_text(
                "Sorry, there was an error getting your categories. Please try again."
            )