# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Expense(BaseModel):
    user_id: int
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    note: Optional[str] = None
    date: datetime = Field(default_factory=datetime.now)

class ExpenseSummary(BaseModel):
    total: Decimal
    count: int
    start_date: datetime
    end_date: datetime

class CategorySummary(BaseModel):
    category: str
    total: Decimal
    percentage: float