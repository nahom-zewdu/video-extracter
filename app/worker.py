# app/worker.py

import subprocess
import os
import random
import time

from app.jobs import job_queue, update_job
from app.uploader import upload_to_gcs
from app.downloader import download_video


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

            # Small random delay
            time.sleep(random.uniform(1, 4))

            input_file = download_video(
                data["url"],
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

            print(url)

            update_job(
                job_id,
                "done",
                result=url
            )

        except Exception as e:
            update_job(
                job_id,
                "failed",
                error=str(e)
            )
