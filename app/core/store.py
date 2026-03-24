from typing import Any


users: dict[str, dict[str, Any]] = {
    "user_1": {
        "user_id": "user_1",
        "name": "Demo Poster",
        "world_id_status": "verified",
        "wallet_connected": True,
        "role": "poster",
    },
    "user_2": {
        "user_id": "user_2",
        "name": "Demo Worker",
        "world_id_status": "verified",
        "wallet_connected": True,
        "role": "worker",
    },
}

tasks: dict[str, dict[str, Any]] = {
    "task_1": {
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
}

escrows: dict[str, dict[str, Any]] = {
    "task_1": {
        "task_id": "task_1",
        "status": "unfunded",
    }
}

task_counter = 1


def next_task_id() -> str:
    global task_counter
    task_counter += 1
    return f"task_{task_counter}"


def list_tasks() -> list[dict[str, Any]]:
    return list(tasks.values())


def get_task(task_id: str) -> dict[str, Any] | None:
    return tasks.get(task_id)


def get_user(user_id: str) -> dict[str, Any] | None:
    return users.get(user_id)


def create_task(data: dict[str, Any]) -> dict[str, Any]:
    task_id = next_task_id()
    item = {
        "id": task_id,
        "title": data["title"],
        "description": data["description"],
        "reward_amount": data["reward_amount"],
        "currency": data.get("currency", "USDC"),
        "status": "open",
        "created_by": data.get("created_by", "user_1"),
        "category": data.get("category", "general"),
        "deadline": data.get("deadline"),
        "worker_id": None,
        "proof_text": None,
        "proof_url": None,
        "escrow_status": "unfunded",
    }

    tasks[task_id] = item
    escrows[task_id] = {
        "task_id": task_id,
        "status": "unfunded",
    }
    return item


def fund_escrow(task_id: str) -> dict[str, Any] | None:
    escrow = escrows.get(task_id)
    task = tasks.get(task_id)

    if not escrow or not task:
        return None

    escrow["status"] = "funded"
    task["escrow_status"] = "funded"
    return {
        "task_id": task_id,
        "escrow_status": "funded",
        "message": "Escrow funded successfully",
    }


def accept_task(task_id: str, worker_id: str) -> tuple[dict[str, Any] | None, str | None]:
    task = tasks.get(task_id)
    if not task:
        return None, "Task not found"

    user = users.get(worker_id)
    if not user:
        return None, "Worker not found"

    if task["status"] != "open":
        return None, "Task is not open"

    task["worker_id"] = worker_id
    task["status"] = "accepted"
    return task, None


def submit_task(
    task_id: str,
    worker_id: str,
    proof_text: str,
    proof_url: str | None = None,
) -> tuple[dict[str, Any] | None, str | None]:
    task = tasks.get(task_id)
    if not task:
        return None, "Task not found"

    if task["status"] != "accepted":
        return None, "Task must be accepted first"

    if task["worker_id"] != worker_id:
        return None, "Only assigned worker can submit"

    task["proof_text"] = proof_text
    task["proof_url"] = proof_url
    task["status"] = "submitted"
    return task, None


def approve_task(task_id: str) -> tuple[dict[str, Any] | None, str | None]:
    task = tasks.get(task_id)
    escrow = escrows.get(task_id)

    if not task:
        return None, "Task not found"

    if task["status"] != "submitted":
        return None, "Task must be submitted first"

    if not escrow or escrow["status"] != "funded":
        return None, "Escrow must be funded first"

    escrow["status"] = "released"
    task["escrow_status"] = "released"
    task["status"] = "paid"

    return {
        "message": "Task approved and payout released",
        "task": task,
    }, None


def get_reputation(user_id: str) -> dict[str, Any] | None:
    user = users.get(user_id)
    if not user:
        return None

    tasks_completed = 0
    submitted_count = 0
    total_earned = 0.0

    for task in tasks.values():
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

    badges: list[str] = []
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


def get_world_status(user_id: str) -> dict[str, Any] | None:
    user = users.get(user_id)
    if not user:
        return None

    return {
        "user_id": user["user_id"],
        "world_id_status": user["world_id_status"],
        "wallet_connected": user["wallet_connected"],
        "verification_level": "human",
    }
