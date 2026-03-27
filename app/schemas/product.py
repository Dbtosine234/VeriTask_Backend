from pydantic import BaseModel


class WalletTransaction(BaseModel):
    id: str
    task_id: str
    title: str
    amount: float
    currency: str
    status: str


class WalletRead(BaseModel):
    user_id: str
    currency: str
    pending_balance: float
    released_balance: float
    total_earned: float
    transactions: list[WalletTransaction]


class ActivityItem(BaseModel):
    id: str
    type: str
    task_id: str
    message: str


class ActivityRead(BaseModel):
    user_id: str
    items: list[ActivityItem]
