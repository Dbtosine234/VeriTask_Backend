from fastapi import APIRouter, HTTPException

from app.core.store import users
from app.schemas.world import WorldStatusResponse, WorldVerifyRequest

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/status/{user_id}", response_model=WorldStatusResponse)
def get_world_status(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return WorldStatusResponse(
        user_id=user["user_id"],
        world_id_status=user["world_id_status"],
        wallet_connected=user["wallet_connected"],
        verification_level="human",
    )


@router.post("/verify", response_model=WorldStatusResponse)
def verify_world_id(payload: WorldVerifyRequest):
    user = users.get(payload.user_id)
    if not user:
        users[payload.user_id] = {
            "user_id": payload.user_id,
            "name": payload.user_id,
            "world_id_status": "verified",
            "wallet_connected": True,
        }
        user = users[payload.user_id]
    else:
        user["world_id_status"] = "verified"
        user["wallet_connected"] = True

    return WorldStatusResponse(
        user_id=user["user_id"],
        world_id_status=user["world_id_status"],
        wallet_connected=user["wallet_connected"],
        verification_level="human",
    )
