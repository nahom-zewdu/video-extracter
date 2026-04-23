# app/main.py

from fastapi import FastAPI
from app.models import ClipRequest
from app.jobs import create_job, job_store
from app.worker import worker_loop
import threading

app = FastAPI()

# start worker thread
threading.Thread(target=worker_loop, daemon=True).start()


@app.post("/clip")
def create_clip(req: ClipRequest):
    job_id = create_job(req.dict())
    return {"job_id": job_id}


@app.get("/clip/{job_id}")
def get_clip(job_id: str):
    return job_store.get(job_id, {"error": "not found"})
