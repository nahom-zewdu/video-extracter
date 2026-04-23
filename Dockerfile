FROM python:3.13-slim

RUN apt-get update && apt-get install -y ffmpeg curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. install dependencies FIRST (cacheable layer)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 2. copy app AFTER dependencies
COPY . .

RUN mkdir -p outputs

ENV PORT=8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
