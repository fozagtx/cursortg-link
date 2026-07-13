FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY agent-playbooks ./agent-playbooks
COPY skills-pack ./skills-pack
COPY skills-catalog ./skills-catalog

RUN pip install --no-cache-dir .

RUN mkdir -p /data

CMD ["python", "-m", "cursor_tg_connector"]
