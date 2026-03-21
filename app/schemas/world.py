from pydantic import BaseModel


class VerifyProofRequest(BaseModel):
    app_id: str
    action: str
    proof: str | None = None
    signal: str | None = None
