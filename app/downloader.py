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

def download_file(url: str, output_path: str):
    response = requests.get(url, stream=True)

    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path
