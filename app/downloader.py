# app/downloader.py

import yt_dlp


def download_video(video_url: str, output_path: str):
    """
    Download YouTube video using yt-dlp
    with safer extractor/client settings.
    """

    output_template = output_path.replace(".mp4", ".%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "quiet": True,

        # Important
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "android",
                    "web_safari",
                    "web"
                ]
            }
        },

        # Browser-like headers
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.youtube.com/"
        },

        # Extra reliability
        "retries": 10,
        "fragment_retries": 10,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return output_path
