# app/jobs.py

from queue import Queue
import uuid

job_queue = Queue()
job_store = {}

def create_job(data):
    job_id = str(uuid.uuid4())
    job_store[job_id] = {
        "status": "queued",
        "result": None
    }
    job_queue.put((job_id, data))
    return job_id


def update_job(job_id, status, result=None):
    job_store[job_id]["status"] = status
    job_store[job_id]["result"] = result


