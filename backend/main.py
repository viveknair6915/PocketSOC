from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, incidents, health
from backend.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PocketSOC Backend", version="1.0.0")

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://pocket-soc.vercel.app",
    "https://pocketsoc.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(health.router)

# --- DIRECT DEBUG ENDPOINT TO BYPASS ROUTER ISSUES ---
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_db
from backend.audit.models import Incident
from backend.audit.logger import AuditLogger
from datetime import datetime
import random

class DebugPayload(BaseModel):
    text: str
    agent_id: str

@app.post("/debug/report", status_code=201)
def debug_report_direct(payload: DebugPayload, db: Session = Depends(get_db)):
    is_scam = "scam" in payload.text.lower() or "urgent" in payload.text.lower() or "verify" in payload.text.lower()
    label = "scam" if is_scam else "legit"
    confidence = random.uniform(0.8, 0.99) if is_scam else random.uniform(0.01, 0.2)
    
    new_incident = Incident(
        detected_label=label,
        confidence=confidence,
        decrypted_text=payload.text,
        agent_id=payload.agent_id,
        payload_encrypted="SIMULATION_CLEAR_TEXT",
        timestamp=datetime.utcnow()
    )
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    AuditLogger.log_event(db, new_incident.id, "SIMULATION_EVENT")
    
    return {
        "id": new_incident.id,
        "detected_label": label,
        "confidence": confidence,
        "status": "Simulated Success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
