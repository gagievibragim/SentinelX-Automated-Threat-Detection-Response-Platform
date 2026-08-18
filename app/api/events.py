from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SecurityEvent, Incident, IOC
from app.schemas import EventCreate, EventResponse
from app.detection.engine import DetectionEngine
from app.config import settings
from app.enrichment.ioc import extract_iocs, reputation
from app.response.manager import recommended_action

router = APIRouter(prefix="/api/events", tags=["events"])
engine = DetectionEngine(settings.rules_path)

SEVERITY_SCORE = {"LOW": 20, "MEDIUM": 45, "HIGH": 70, "CRITICAL": 95}

@router.post("", response_model=EventResponse)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = SecurityEvent(**payload.model_dump())
    db.add(event)
    db.flush()

    event_dict = payload.model_dump()
    matches = engine.evaluate(event_dict)

    for rule in matches:
        severity = rule["severity"]
        score = SEVERITY_SCORE.get(severity, 20)
        action = recommended_action(severity, rule["id"])
        incident = Incident(
            title=rule["name"],
            severity=severity,
            status="open",
            rule_id=rule["id"],
            mitre_technique=rule.get("mitre_technique"),
            description=rule.get("description"),
            risk_score=score,
            event_id=event.id,
            metadata_json={"action": action},
        )
        db.add(incident)
        db.flush()

        text = f"{payload.message or ''} {payload.source_ip or ''}"
        for ioc_type, value in extract_iocs(text):
            db.add(IOC(
                incident_id=incident.id,
                ioc_type=ioc_type,
                value=value,
                reputation=reputation(value) if ioc_type == "ip" else "unknown",
            ))

    db.commit()
    db.refresh(event)
    return event
