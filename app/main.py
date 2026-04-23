# app/main.py

from fastapi import FastAPI
from app.models import ClipRequest
from app.jobs import create_job, get_job
from app.worker import worker_loop
import threading

app = FastAPI()

# Start worker thread (Cloud Run v1 assumption)
threading.Thread(target=worker_loop, daemon=True).start()


@app.post("/clip")
def create_clip(req: ClipRequest):
    job_id = create_job(req.dict())
    return {"job_id": job_id}


@app.get("/clip/{job_id}")
def get_clip(job_id: str):
    job = get_job(job_id)

    if not job:
        return {"error": "not found"}

    return {
        "status": job["status"],
        "video_url": job.get("result"),
        "error": job.get("error")
    }
