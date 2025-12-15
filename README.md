# PocketSOC – On-Device AI Fraud & Threat Detection Platform

## 🎯 Project Goal
A production-grade, end-to-end system demonstrating on-device AI fraud detection, secure backend ingestion, and performance benchmarking.

## 🏗️ System Architecture

```ascii
[ SMS / Text ]
      ↓
[ Mobile Agent (Simulated) ]
      ↓
[ Preprocessing & TFLite Inference ] -> (Scam Detected?)
      ↓ Yes
[ AES-256 Encryption ]
      ↓
[ HTTP POST + JWT ]
      ↓
[ FastAPI Backend ]
      ↓
[ Decryption & Verification ]
      ↓
[ SQLite DB & Audit Log ]
```

## 📂 Folder Structure
- **agent/**: Simulated mobile agent (inference, crypto, sender).
- **model/**: AI pipeline (dataset, train, export).
- **backend/**: Secure API (auth, encryption, RBAC).
- **benchmarks/**: Performance testing scripts.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Docker (optional)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python model/dataset_loader.py  # Create dummy dataset
python model/train.py           # Train model
python model/convert_tflite.py  # Convert to TFLite
```

### 3. Run the Backend
```bash
uvicorn backend.main:app --reload
```
or via Docker:
```bash
docker-compose up --build
```

### 4. Run the Agent
In a new terminal:
```bash
python agent/agent_runner.py
```
Type a message like *"Urgent: Update your bank details now"* to see it detected and reported.

## 🔒 Threat Model
- **Data in Transit**: Secured via TLS (HTTPS) and application-layer AES-256 encryption.
- **Authentication**: JWT tokens signed with HS256 (simulated robust auth).
- **Access Control**: RBAC ensures only agents can report, and only analysts/admins can view.
- **Audit**: Immutable hash-chained logs track all actions.

## ⚡ Performance
See `benchmarks/results.md` for latest run data.
Run `python benchmarks/latency_test.py` to measure.

## 🔮 Future Improvements
- Replace SQLite with PostgreSQL.
- Implement real-time model updates (OTA).
- Add specific phishing link detection features.
