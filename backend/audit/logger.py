import hashlib
from sqlalchemy.orm import Session
from backend.audit.models import AuditLog

class AuditLogger:
    @staticmethod
    def log_event(db: Session, incident_id: int, action: str):
        # Get last log to form chain
        last_log = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
        prev_hash = last_log.current_hash if last_log else "0" * 64
        
        # Create current hash
        # Minimal implementation of hash chain: sha256(prev_hash + action + incident_id)
        data_to_hash = f"{prev_hash}{action}{incident_id}"
        current_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        new_log = AuditLog(
            incident_id=incident_id,
            action=action,
            previous_hash=prev_hash,
            current_hash=current_hash
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log
