from fastapi import APIRouter, HTTPException

from app.schemas.marketplace import TaskCreate, TaskRead
from app.schemas.world import VerifyProofRequest

router = APIRouter()

IN_MEMORY_USERS = {
    "user_1": {
        "id": "user_1",
        "name": "Demo Poster",
        "world_id_status": "verified",
        "wallet_connected": True,
    },
    "user_2": {
        "id": "user_2",
        "name": "Demo Worker",
        "world_id_status": "verified",
        "wallet_connected": True,
    },
}

IN_MEMORY_TASKS = [
    {
        "id": "task_1",
        "title": "Record store shelf availability",
        "description": "Visit the assigned location and record current stock visibility.",
        "reward_amount": "5",
        "currency": "USDC",
        "status": "open",
        "created_by": "user_1",
        "category": "field",
        "deadline": None,
        "worker_id": None,
        "proof_text": None,
        "proof_url": None,
        "escrow_status": "unfunded",
    }
]

IN_MEMORY_ESCROWS = {
    "task_1": {
        "task_id": "task_1",
        "status": "unfunded",
    }
}


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
    return IN_MEMORY_TASKS


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    for task in IN_MEMORY_TASKS:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    item = {
        "id": f"task_{len(IN_MEMORY_TASKS) + 1}",
        "title": task.title,
        "description": task.description,
        "reward_amount": task.reward_amount,
        "currency": task.currency,
        "status": "open",
        "created_by": getattr(task, "created_by", "user_1"),
        "category": getattr(task, "category", "general"),
        "deadline": getattr(task, "deadline", None),
        "worker_id": None,
        "proof_text": None,
        "proof_url": None,
        "escrow_status": "unfunded",
    }
    IN_MEMORY_TASKS.append(item)
    IN_MEMORY_ESCROWS[item["id"]] = {
        "task_id": item["id"],
        "status": "unfunded",
    }
    return item


@router.post("/tasks/{task_id}/accept")
def accept_task(task_id: str, payload: dict):
    worker_id = payload.get("worker_id")

    if not worker_id:
        raise HTTPException(status_code=400, detail="worker_id is required")

    if worker_id not in IN_MEMORY_USERS:
        raise HTTPException(status_code=404, detail="Worker not found")

    for task in IN_MEMORY_TASKS:
        if task["id"] == task_id:
            if task["status"] != "open":
                raise HTTPException(status_code=400, detail="Task is not open")
            task["worker_id"] = worker_id
            task["status"] = "accepted"
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks/{task_id}/submit")
def submit_task(task_id: str, payload: dict):
    worker_id = payload.get("worker_id")
    proof_text = payload.get("proof_text")
    proof_url = payload.get("proof_url")

    if not worker_id or not proof_text:
        raise HTTPException(status_code=400, detail="worker_id and proof_text are required")

    for task in IN_MEMORY_TASKS:
        if task["id"] == task_id:
            if task["status"] != "accepted":
                raise HTTPException(status_code=400, detail="Task must be accepted first")
            if task["worker_id"] != worker_id:
                raise HTTPException(status_code=403, detail="Only assigned worker can submit")
            task["proof_text"] = proof_text
            task["proof_url"] = proof_url
            task["status"] = "submitted"
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks/{task_id}/approve")
def approve_task(task_id: str):
    for task in IN_MEMORY_TASKS:
        if task["id"] == task_id:
            escrow = IN_MEMORY_ESCROWS.get(task_id)

            if task["status"] != "submitted":
                raise HTTPException(status_code=400, detail="Task must be submitted first")

            if not escrow or escrow["status"] != "funded":
                raise HTTPException(status_code=400, detail="Escrow must be funded first")

            escrow["status"] = "released"
            task["escrow_status"] = "released"
            task["status"] = "paid"

            return {
                "message": "Task approved and payout released",
                "task": task,
            }

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/escrow/fund")
def fund_escrow(payload: dict):
    task_id = payload.get("task_id")

    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required")

    escrow = IN_MEMORY_ESCROWS.get(task_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")

    escrow["status"] = "funded"

    for task in IN_MEMORY_TASKS:
        if task["id"] == task_id:
            task["escrow_status"] = "funded"
            break

    return {
        "task_id": task_id,
        "escrow_status": "funded",
        "message": "Escrow funded successfully",
    }


@router.get("/reputation/{user_id}")
def get_reputation(user_id: str):
    user = IN_MEMORY_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tasks_completed = 0
    submitted_count = 0
    total_earned = 0.0

    for task in IN_MEMORY_TASKS:
        if task.get("worker_id") == user_id:
            if task["status"] in ["submitted", "paid"]:
                submitted_count += 1
            if task["status"] == "paid":
                tasks_completed += 1
                try:
                    total_earned += float(task["reward_amount"])
                except (TypeError, ValueError):
                    pass

    approval_rate = 100 if submitted_count == 0 else round((tasks_completed / submitted_count) * 100)
    reputation_score = min(100, tasks_completed * 20)

    badges = []
    if user["world_id_status"] == "verified":
        badges.append("Verified Human")
    if tasks_completed >= 1:
        badges.append("Trusted Worker")
    if tasks_completed >= 3:
        badges.append("Fast Climber")

    return {
        "user_id": user_id,
        "verified": user["world_id_status"] == "verified",
        "tasks_completed": tasks_completed,
        "reputation_score": reputation_score,
        "approval_rate": approval_rate,
        "disputes": 0,
        "total_earned": total_earned,
        "badges": badges,
    }


@router.get("/world/status/{user_id}")
def world_status(user_id: str):
    user = IN_MEMORY_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user["id"],
        "world_id_status": user["world_id_status"],
        "wallet_connected": user["wallet_connected"],
        "verification_level": "human",
    }


@router.post("/world/verify")
def verify_world_proof(payload: VerifyProofRequest):
    return {
        "verified": False,
        "app_id": payload.app_id,
        "action": payload.action,
        "message": "Implement live World proof verification here.",
    }
