# app/models.py
from pydantic import BaseModel

class ClipRequest(BaseModel):
    url: str
    start: str
    duration: int