FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

COPY uv.lock ./

COPY src/ ./src/

COPY README.md ./

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "crosspost_mcp.server"]
