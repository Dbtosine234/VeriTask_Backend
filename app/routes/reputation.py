from fastapi import APIRouter, HTTPException

from app.core.store import tasks, users

router = APIRouter(prefix="/reputation", tags=["reputation"])


@router.get("/{user_id}")
def get_reputation(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    completed = 0
    submitted = 0
    total_earned = 0.0

    for task in tasks.values():
        if task.get("worker_id") == user_id:
            if task["status"] in ["submitted", "approved", "paid"]:
                submitted += 1
            if task["status"] == "paid":
                completed += 1
                total_earned += float(task["reward"])

    approval_rate = 100 if submitted == 0 else round((completed / submitted) * 100)
    reputation_score = min(100, completed * 20)

    badges = []
    if user["world_id_status"] == "verified":
        badges.append("Verified Human")
    if completed >= 1:
        badges.append("Trusted Worker")
    if completed >= 3:
        badges.append("Fast Climber")

    return {
        "user_id": user_id,
        "verified": user["world_id_status"] == "verified",
        "tasks_completed": completed,
        "reputation_score": reputation_score,
        "approval_rate": approval_rate,
        "disputes": 0,
        "total_earned": total_earned,
        "badges": badges,
    }
