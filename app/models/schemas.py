from pydantic import BaseModel
from typing import List

class ReviewRequest(BaseModel):
    texts: List[str]

class AnalysisResponse(BaseModel):
    sentiment: str
    aspects: List[str]
    summary: str
    improvement_tip: str