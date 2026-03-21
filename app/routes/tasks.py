from fastapi import APIRouter, HTTPException, Query

from app.core.store import escrows, next_task_id, tasks, users
from app.schemas.marketplace import (
    TaskAcceptRequest,
    TaskCreate,
    TaskResponse,
    TaskSubmitRequest,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(status: str | None = Query(default=None), category: str | None = Query(default=None)):
    items = list(tasks.values())

    if status:
        items = [task for task in items if task["status"] == status]

    if category:
        items = [task for task in items if task["category"] == category]

    return items


@router.post("", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    if payload.created_by not in users:
        raise HTTPException(status_code=404, detail="Creator not found")

    task_id = next_task_id()

    task = {
        "task_id": task_id,
        "title": payload.title,
        "description": payload.description,
        "reward": payload.reward,
        "currency": payload.currency,
        "created_by": payload.created_by,
        "deadline": payload.deadline,
        "category": payload.category,
        "status": "open",
        "worker_id": None,
        "proof_text": None,
        "proof_url": None,
        "escrow_status": "unfunded",
    }

    tasks[task_id] = task
    escrows[task_id] = {
        "task_id": task_id,
        "amount": payload.reward,
        "currency": payload.currency,
        "status": "unfunded",
    }

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/accept", response_model=TaskResponse)
def accept_task(task_id: str, payload: TaskAcceptRequest):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "open":
        raise HTTPException(status_code=400, detail="Task is not open for acceptance")

    if payload.worker_id not in users:
        raise HTTPException(status_code=404, detail="Worker not found")

    task["worker_id"] = payload.worker_id
    task["status"] = "accepted"
    return task


@router.post("/{task_id}/submit", response_model=TaskResponse)
def submit_task(task_id: str, payload: TaskSubmitRequest):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "accepted":
        raise HTTPException(status_code=400, detail="Task must be accepted before submission")

    if task["worker_id"] != payload.worker_id:
        raise HTTPException(status_code=403, detail="Only assigned worker can submit this task")

    task["proof_text"] = payload.proof_text
    task["proof_url"] = payload.proof_url
    task["status"] = "submitted"
    return task


@router.post("/{task_id}/approve", response_model=TaskResponse)
def approve_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "submitted":
        raise HTTPException(status_code=400, detail="Task must be submitted before approval")

    escrow = escrows.get(task_id)
    if not escrow or escrow["status"] != "funded":
        raise HTTPException(status_code=400, detail="Escrow must be funded before approval")

    task["status"] = "paid"
    task["escrow_status"] = "released"
    escrow["status"] = "released"
    return task
