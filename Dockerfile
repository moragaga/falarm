# syntax=docker/dockerfile:1.7

FROM python:3.14.2-slim-bookworm AS builder

ARG BUILD_CREATED_AT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /usr/app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        findutils \
        coreutils \
    && pip install --prefix=/install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p src/assets \
    && printf '%s\n' "${BUILD_CREATED_AT:-$(date -u '+%Y-%m-%dT%H:%M:%SZ')}" > src/assets/version.txt \
    && find src/assets/css -name '*.css' ! -name 'ada_bundle.css' -type f -exec cat {} + > src/assets/ada_bundle.css \
    && find src/assets/css -name '*.css' ! -name 'ada_bundle.css' -type f -delete \
    && find src/assets/css -type d -empty -delete \
    && mkdir -p src/assets/css \
    && mv src/assets/ada_bundle.css src/assets/css/ada_bundle.css \
    && find . -name "*.pyc" -delete \
    && find . -name "__pycache__" -type d -prune -exec rm -rf {} +

FROM python:3.14.2-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/app

COPY --from=builder /install /usr/local
COPY --from=builder /usr/app /usr/app

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.config.py", "app:app"]