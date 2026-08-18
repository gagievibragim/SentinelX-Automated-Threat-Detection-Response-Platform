from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey

from app.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    timestamp = Column(DateTime, nullable=True)
    source = Column(String(50), nullable=False)
    event_type = Column(String(100), nullable=False)
    username = Column(String(255))
    source_ip = Column(String(64))
    hostname = Column(String(255))
    message = Column(Text)
    raw = Column(JSON, default=dict)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    title = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(30), default="open")
    rule_id = Column(String(100), nullable=False)
    mitre_technique = Column(String(100))
    description = Column(Text)
    risk_score = Column(Integer, default=0)
    event_id = Column(Integer, ForeignKey("security_events.id"))
    metadata_json = Column(JSON, default=dict)

class IOC(Base):
    __tablename__ = "iocs"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    ioc_type = Column(String(30), nullable=False)
    value = Column(String(512), nullable=False)
    reputation = Column(String(30), default="unknown")
