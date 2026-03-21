from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.core.store import escrows, tasks

router = APIRouter(prefix="/escrow", tags=["escrow"])


class EscrowFundRequest(BaseModel):
    task_id: str


class EscrowReleaseRequest(BaseModel):
    task_id: str


@router.post("/fund")
def fund_escrow(payload: EscrowFundRequest):
    task = tasks.get(payload.task_id)
    escrow = escrows.get(payload.task_id)

    if not task or not escrow:
        raise HTTPException(status_code=404, detail="Task escrow not found")

    escrow["status"] = "funded"
    task["escrow_status"] = "funded"

    return {
        "task_id": payload.task_id,
        "escrow_status": escrow["status"],
        "message": "Escrow funded successfully",
    }


@router.post("/release")
def release_escrow(payload: EscrowReleaseRequest):
    task = tasks.get(payload.task_id)
    escrow = escrows.get(payload.task_id)

    if not task or not escrow:
        raise HTTPException(status_code=404, detail="Task escrow not found")

    if task["status"] not in ["approved", "paid", "submitted"]:
        raise HTTPException(status_code=400, detail="Task is not ready for payout release")

    escrow["status"] = "released"
    task["escrow_status"] = "released"
    task["status"] = "paid"

    return {
        "task_id": payload.task_id,
        "escrow_status": escrow["status"],
        "task_status": task["status"],
        "message": "Payout released successfully",
    }
