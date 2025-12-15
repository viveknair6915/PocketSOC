from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from pydantic import BaseModel
from datetime import datetime

from backend.database import get_db
from backend.schemas.incident import IncidentCreate, IncidentResponse
from backend.audit.models import Incident
from backend.audit.logger import AuditLogger
from backend.security.encryption import encryption_utils
from backend.auth.dependencies import require_role, Role
from backend.auth.rbac import Role

router = APIRouter(prefix="/incident", tags=["incident"])

@router.post("/report", status_code=201)
async def report_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    # Decrypt payload
    try:
        decrypted_json = encryption_utils.decrypt_payload(incident.encrypted_payload)
        payload_data = json.loads(decrypted_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid encrypted payload")

    # Save to DB
    db_incident = Incident(
        agent_id=incident.agent_id,
        payload_encrypted=incident.encrypted_payload,
        decrypted_text=decrypted_json,
        detected_label=payload_data.get("detected_label"),
        confidence=payload_data.get("confidence"),
        raw_score=payload_data.get("raw_score")
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    # Audit Log
    AuditLogger.log_event(db, db_incident.id, "INCIDENT_REPORTED")

    return {"status": "received", "id": db_incident.id}

# --- DEBUG SIMULATOR ENDPOINT ---
class DebugPayload(BaseModel):
    text: str
    agent_id: str

@router.post("/debug_report", status_code=201)
def debug_report(payload: DebugPayload, db: Session = Depends(get_db)):
    """
    Simulates an agent report for the Frontend Demo.
    This skips the encryption requirement for easy testing via UI.
    In a real scenario, the Frontend would act as a 'read-only' dashboard
    and the Agent (Python) would be the only writer.
    """
    import random
    
    # Mock Detection Logic
    is_scam = "scam" in payload.text.lower() or "urgent" in payload.text.lower() or "verify" in payload.text.lower()
    label = "scam" if is_scam else "legit"
    confidence = random.uniform(0.8, 0.99) if is_scam else random.uniform(0.01, 0.2)
    
    new_incident = Incident(
        detected_label=label,
        confidence=confidence,
        message_content=payload.text,
        timestamp=datetime.utcnow()
    )
    
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    
    # Audit
    AuditLogger.log_event(db, new_incident.id, "SIMULATION_EVENT", f"Simulated incident {new_incident.id} from UI.")
    
    return {
        "id": new_incident.id,
        "detected_label": label,
        "confidence": confidence,
        "status": "Simulated Success"
    }

@router.get("/all", response_model=List[IncidentResponse])
async def read_all_incidents(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(require_role(Role.ADMIN))
):
    incidents = db.query(Incident).all()
    # Audit Log (optional for read, but good for tracking access)
    # AuditLogger.log_event(db, 0, f"ALL_INCIDENTS_ACCESSED_BY_{current_user['username']}")
    return incidents

@router.get("/{incident_id}", response_model=IncidentResponse)
async def read_incident(
    incident_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(Role.ANALYST))
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident
