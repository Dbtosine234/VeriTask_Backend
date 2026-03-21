from typing import Any

users: dict[str, dict[str, Any]] = {
    "user_1": {
        "user_id": "user_1",
        "name": "Demo Poster",
        "world_id_status": "verified",
        "wallet_connected": True,
    },
    "user_2": {
        "user_id": "user_2",
        "name": "Demo Worker",
        "world_id_status": "verified",
        "wallet_connected": True,
    },
}

tasks: dict[str, dict[str, Any]] = {}

escrows: dict[str, dict[str, Any]] = {}

task_counter = 0


def next_task_id() -> str:
    global task_counter
    task_counter += 1
    return f"task_{task_counter}"
