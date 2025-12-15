# PocketSOC Deployment Guide

This guide explains how to push your code to GitHub and deploy the PocketSOC platform to the cloud.

## 1. Git Setup (Version Control)

Before deploying, you need to save your code to a Git repository.

### Initialize Git
Open your terminal in `C:\Users\HP\Desktop\PocketSOC` and run:

```bash
git init
git add .
git commit -m "Initial commit of PocketSOC v1.0"
```

### Push to GitHub
1.  Create a new repository on [GitHub](https://github.com/new).
2.  Follow the instructions to push an existing repository:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/PocketSOC.git
git push -u origin main
```

---

## 2. Deployment

Since PocketSOC has three parts (Frontend, Backend, Agent), you will deploy them separately.

### A. Backend (FastAPI)
**Recommended Host:** [Render](https://render.com) (Free Tier) or [Railway](https://railway.app).

1.  **Sign up** for Render/Railway and connect your GitHub account.
2.  **New Web Service**: Select your `PocketSOC` repository.
3.  **Root Directory**: Set this to `.` (current directory).
4.  **Build Command**: `pip install -r requirements.txt` (Render usually detects this automatically).
5.  **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6.  **Environment Variables**: Add these in the dashboard:
    *   `SECRET_KEY`: (Generate a random string)
    *   `DATABASE_URL`: (If using PostgreSQL, otherwise it will use ephemeral SQLite)

### B. Frontend (React)
**Recommended Host:** [Vercel](https://vercel.com) or [Netlify](https://netlify.com).

1.  **Sign up** and "Add New Project".
2.  **Select Repo**: Choose `PocketSOC`.
3.  **Framework Preset**: Select **Vite**.
4.  **Root Directory**: Click "Edit" and change it to `frontend`.
5.  **Environment Variables**:
    *   `VITE_API_URL`: The URL of your deployed Backend (e.g., `https://pocketsoc-backend.onrender.com`).
    *   *Note: You will need to update `vite.config.js` or `api.js` to use this ENV variable instead of the local proxy for production builds.*

### C. Run the Agent (Client)
The Agent is designed to run on the *client's device*.

1.  **On User's Machine**:
    ```bash
    pip install -r requirements.txt
    python agent/agent_runner.py
    ```
2.  **Update Config**: Change `agent/agent_config.py` to point to your deployed backend URL.

---

## 3. Production Readiness Checklist

- [ ] **Change Secrets**: Replace default keys in `.env` and `agent/agent_config.py` with strong environment variables.
- [ ] **Database**: Switch from SQLite to PostgreSQL for persistent production data.
- [ ] **HTTPS**: Ensure Backend and Frontend are served over HTTPS (automatic on Render/Vercel).
