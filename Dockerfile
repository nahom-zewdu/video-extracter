FROM python:3.13-slim

# system deps (ffmpeg is critical)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install uv
RUN pip install uv

# copy project
COPY . .

# install python deps via uv
RUN uv pip install fastapi uvicorn yt-dlp google-cloud-storage

# create output dir
RUN mkdir -p outputs

# Cloud Run listens on 8080
ENV PORT=8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]