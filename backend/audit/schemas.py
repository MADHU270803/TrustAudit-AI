from pydantic import BaseModel, Field
from typing import List

class AuditRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="The AI-generated text to audit"
    )
    source_model: str = Field(
        default="unknown",
        description="Which AI produced this text, if known"
    )

class Flag(BaseModel):
    category: str
    detail: str
    severity: str

class AuditResponse(BaseModel):
    trust_score: int
    label: str
    flags: List[Flag]
    explanation: str