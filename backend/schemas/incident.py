from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentBase(BaseModel):
    agent_id: str
    encrypted_payload: str
    timestamp: datetime
    model_version: str

    model_config = {'protected_namespaces': ()}

class IncidentCreate(IncidentBase):
    pass

class IncidentResponse(BaseModel):
    id: int
    detected_label: str
    confidence: float
    timestamp: datetime
    
    class Config:
        from_attributes = True
