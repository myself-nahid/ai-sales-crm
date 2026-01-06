from pydantic import BaseModel
from typing import Optional

class Lead(BaseModel):
    name: str
    email: str
    company: str
    job_title: Optional[str] = None
    industry: Optional[str] = None
    persona: Optional[str] = None
    priority: Optional[str] = None
    email_sent: Optional[bool] = False
    response_status: Optional[str] = None