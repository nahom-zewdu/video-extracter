# app/worker.py

import subprocess
import os

from app.jobs import job_queue, update_job
from app.uploader import upload_to_gcs

from app.downloader import (
    get_download_url,
    download_file,
)

def cut(input_file, start, duration, output):
    cmd = [
        "ffmpeg",
        "-ss", start,
        "-i", input_file,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "veryfast",
        "-movflags", "+faststart",
        output
    ]

    subprocess.run(cmd, check=True)


def worker_loop():
    os.makedirs("outputs", exist_ok=True)

    while True:
        job_id, data = job_queue.get()

        try:
            update_job(job_id, "processing")

            download_url = get_download_url(data["url"])

            input_file = download_file(
                download_url,
                f"outputs/{job_id}.mp4"
            )

            output_file = f"outputs/{job_id}_clip.mp4"

            cut(
                input_file,
                data["start"],
                data["duration"],
                output_file
            )

            # Upload to GCS
            url = upload_to_gcs(
                output_file,
                f"clips/{job_id}.mp4"
            )

            update_job(job_id, "done", result=url)

        except Exception as e:
            update_job(job_id, "failed", error=str(e))