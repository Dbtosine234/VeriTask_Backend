from fastapi import APIRouter, HTTPException

from app.core.store import (
    accept_task as store_accept_task,
    approve_task as store_approve_task,
    create_task as store_create_task,
    fund_escrow as store_fund_escrow,
    get_reputation as store_get_reputation,
    get_task as store_get_task,
    get_world_status as store_get_world_status,
    list_tasks as store_list_tasks,
    submit_task as store_submit_task,
)
from app.schemas.actions import AcceptTaskRequest, FundEscrowRequest, SubmitTaskRequest
from app.schemas.marketplace import TaskCreate, TaskRead
from app.schemas.world import VerifyProofRequest
from app.core.store import get_activity as store_get_activity
from app.core.store import get_wallet as store_get_wallet
from app.schemas.product import ActivityRead, WalletRead

router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/ready")
def ready():
    return {"ready": True, "services": ["api"]}


@router.get("/project/overview")
def project_overview():
    return {
        "name": "VeriTask",
        "track": "World Mini Apps",
        "category": ["Human-Only Marketplace", "Proof of Contribution"],
        "core_value": "bot-resistant work and rewards for verified humans",
    }


@router.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return store_list_tasks()


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = store_get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    data = task.model_dump() if hasattr(task, "model_dump") else task.dict()
    return store_create_task(data)


@router.post("/tasks/{task_id}/accept")
def accept_task(task_id: str, payload: AcceptTaskRequest):
    task, error = store_accept_task(task_id, payload.worker_id)
    if error == "Worker not found":
        raise HTTPException(status_code=404, detail=error)
    if error == "Task not found":
        raise HTTPException(status_code=404, detail=error)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return task


@router.post("/tasks/{task_id}/submit")
def submit_task(task_id: str, payload: SubmitTaskRequest):
    task, error = store_submit_task(
        task_id,
        payload.worker_id,
        payload.proof_text,
        payload.proof_url,
    )
    if error == "Task not found":
        raise HTTPException(status_code=404, detail=error)
    if error == "Only assigned worker can submit":
        raise HTTPException(status_code=403, detail=error)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return task


@router.post("/tasks/{task_id}/approve")
def approve_task(task_id: str):
    result, error = store_approve_task(task_id)
    if error == "Task not found":
        raise HTTPException(status_code=404, detail=error)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


@router.post("/escrow/fund")
def fund_escrow(payload: FundEscrowRequest):
    result = store_fund_escrow(payload.task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Escrow not found")
    return result


@router.get("/reputation/{user_id}")
def get_reputation(user_id: str):
    result = store_get_reputation(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/world/status/{user_id}")
def world_status(user_id: str):
    result = store_get_world_status(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/world/verify")
def verify_world_proof(payload: VerifyProofRequest):
    return {
        "verified": False,
        "app_id": payload.app_id,
        "action": payload.action,
        "message": "Implement live World proof verification here.",
    }
@router.get("/wallet/{user_id}", response_model=WalletRead)
def get_wallet(user_id: str):
    result = store_get_wallet(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/activity/{user_id}", response_model=ActivityRead)
def get_activity(user_id: str):
    result = store_get_activity(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
