from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional
from config import MONGODB_URI, DATABASE_NAME
from models import Expense, ExpenseSummary, CategorySummary
from decimal import Decimal

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.expenses = self.db.expenses

    async def add_expense(self, user_id: int, amount: float, category: str, note: Optional[str] = None) -> Expense:
        expense = Expense(
            user_id=user_id,
            amount=Decimal(str(amount)),
            category=category.lower(),
            note=note
        )
        
        # Convert Decimal to float for MongoDB storage
        expense_dict = expense.model_dump()
        expense_dict['amount'] = float(expense_dict['amount'])
        
        await self.expenses.insert_one(expense_dict)
        return expense

    async def get_monthly_summary(self, user_id: int) -> Optional[ExpenseSummary]:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now()
        
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'date': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total': {'$sum': '$amount'},
                    'count': {'$sum': 1}
                }
            }
        ]
        
        result = await self.expenses.aggregate(pipeline).to_list(1)
        if result:
            return ExpenseSummary(
                total=Decimal(str(result[0]['total'])),  # Convert float back to Decimal
                count=result[0]['count'],
                start_date=start_date,
                end_date=end_date
            )
        return None

    async def get_category_summary(self, user_id: int) -> list[CategorySummary]:
        start_date = datetime.now().replace(day=1)
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'date': {'$gte': start_date}
                }
            },
            {
                '$group': {
                    '_id': '$category',
                    'total': {'$sum': '$amount'}
                }
            },
            {'$sort': {'total': -1}}
        ]
        
        results = await self.expenses.aggregate(pipeline).to_list(None)
        
        # Calculate total expenses for percentage
        total_expenses = sum(float(result['total']) for result in results) if results else 0
        
        return [
            CategorySummary(
                category=result['_id'],
                total=Decimal(str(result['total'])),  # Convert float back to Decimal
                percentage=float(Decimal(str(result['total'])) / Decimal(str(total_expenses)) * 100) if total_expenses else 0
            )
            for result in results
        ]