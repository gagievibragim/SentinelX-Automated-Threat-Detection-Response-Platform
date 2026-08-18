from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident, SecurityEvent

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    by_severity = {}
    by_rule = {}
    for i in incidents:
        by_severity[i.severity] = by_severity.get(i.severity, 0) + 1
        by_rule[i.rule_id] = by_rule.get(i.rule_id, 0) + 1
    return {
        "events": db.query(func.count(SecurityEvent.id)).scalar() or 0,
        "incidents": len(incidents),
        "open_incidents": sum(i.status == "open" for i in incidents),
        "severity": by_severity,
        "detections": by_rule,
    }
