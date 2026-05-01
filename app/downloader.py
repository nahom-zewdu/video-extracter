# app/downloader.py

import requests


def get_download_url(video_url: str) -> str:
    """
    Call external downloader API
    and return direct downloadable MP4 URL.
    """

    response = requests.post(
        "https://example-api.com/download",
        json={"url": video_url},
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["download_url"]
