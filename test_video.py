import yt_dlp
import subprocess
import os


def download_video(url, output_name="input"):
    """
    Downloads best video+audio merged into a single file.
    """
    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": f"{output_name}.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f"{output_name}.mp4"


def cut_video(input_file, start, duration, output_file):
    """
    Cuts a local video file safely.
    """
    cmd = [
        "ffmpeg",
        "-ss", start,
        "-i", input_file,
        "-t", duration,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "veryfast",
        "-movflags", "+faststart",
        output_file,
    ]

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    URL = "https://www.youtube.com/watch?v=vhdfH4FdGPI"

    print("Downloading video...")
    input_file = download_video(URL)

    print("Cutting clip...")
    cut_video(
        input_file=input_file,
        start="00:00:10",
        duration="15",
        output_file="output.mp4"
    )

    print("Done: output.mp4")