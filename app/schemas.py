from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    timestamp: Optional[datetime] = None
    source: str = Field(min_length=1, max_length=50)
    event_type: str = Field(min_length=1, max_length=100)
    username: Optional[str] = None
    source_ip: Optional[str] = None
    hostname: Optional[str] = None
    message: Optional[str] = None
    raw: dict[str, Any] = {}

class EventResponse(EventCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class IncidentResponse(BaseModel):
    id: int
    created_at: datetime
    title: str
    severity: str
    status: str
    rule_id: str
    mitre_technique: Optional[str]
    description: Optional[str]
    risk_score: int
    event_id: Optional[int]
    metadata_json: dict = {}
    model_config = {"from_attributes": True}
