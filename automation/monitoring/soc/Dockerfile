FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY scripts/runtime_config.py /app/runtime_config.py
COPY scripts/auto_response.py /app/auto_response.py
COPY scripts/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "/app/auto_response.py"]
