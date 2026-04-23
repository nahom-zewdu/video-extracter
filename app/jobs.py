# app/jobs.py

from queue import Queue
import uuid
import threading

job_queue = Queue()
job_store = {}
lock = threading.Lock()


def create_job(data):
    job_id = str(uuid.uuid4())

    with lock:
        job_store[job_id] = {
            "status": "queued",
            "result": None,
            "error": None
        }

    job_queue.put((job_id, data))
    return job_id


def update_job(job_id, status, result=None, error=None):
    with lock:
        if job_id not in job_store:
            return False

        job_store[job_id]["status"] = status

        if result is not None:
            job_store[job_id]["result"] = result

        if error is not None:
            job_store[job_id]["error"] = error

    return True


def get_job(job_id):
    with lock:
        return job_store.get(job_id)
