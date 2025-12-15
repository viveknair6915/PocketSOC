from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    detected_label = Column(String)
    confidence = Column(Float)
    raw_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    payload_encrypted = Column(String) # Storing original encrypted payload for audit
    decrypted_text = Column(String) # Storing decrypted text (if policy allows)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    previous_hash = Column(String) # For hash chaining
    current_hash = Column(String)
