from pydantic import BaseModel


class AcceptTaskRequest(BaseModel):
    worker_id: str


class SubmitTaskRequest(BaseModel):
    worker_id: str
    proof_text: str
    proof_url: str | None = None


class FundEscrowRequest(BaseModel):
    task_id: str
