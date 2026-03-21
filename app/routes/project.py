from fastapi import APIRouter

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/overview")
def project_overview():
    return {
        "name": "Genesis Fresh Scaffold",
        "mode": "fresh-code",
        "goal": "Hackathon-ready scaffold aligned to a sponsor challenge",
        "next_step": "Implement challenge-specific workflow and partner bounty integration",
    }
