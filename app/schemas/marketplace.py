from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=10, max_length=2000)
    reward_amount: str
    currency: str = "USDC"
    created_by: Optional[str] = "user_1"
    category: Optional[str] = "general"
    deadline: Optional[str] = None


class TaskRead(BaseModel):
    id: str
    title: str
    description: str
    reward_amount: str
    currency: str
    status: str
    created_by: Optional[str] = None
    category: Optional[str] = None
    deadline: Optional[str] = None
    worker_id: Optional[str] = None
    proof_text: Optional[str] = None
    proof_url: Optional[str] = None
    escrow_status: Optional[str] = "unfunded"
