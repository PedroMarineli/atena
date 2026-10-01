# =============================================================================
# Stage 1: Build stage (compilers, build headers and wheel compilation)
# =============================================================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install compiler & development headers required only for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# =============================================================================
# Stage 2: Final hardened runtime stage (Non-root, Minimal attack surface)
# =============================================================================
FROM python:3.11-slim AS runtime

LABEL maintainer="Pedro Marineli <pedromarineli@users.noreply.github.com>" \
      org.opencontainers.image.title="Atena ERP" \
      org.opencontainers.image.description="Hardened, production-ready enterprise ERP container" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only essential shared runtime libraries (without compilers) + tini for PID 1 & curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    curl \
    libpq5 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root user and group with explicit UID/GID (10001)
RUN groupadd -g 10001 -r appgroup && \
    useradd -u 10001 -r -g appgroup -s /sbin/nologin -d /app appuser

# Copy wheels from builder and install into Python environment
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels requirements.txt

# Create required operational directories with proper permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appgroup /app

# Copy application source code with non-root ownership
COPY --chown=appuser:appgroup . /app/

# Switch to non-root user (Principle of Least Privilege / PodSecurity Standard Restricted)
USER 10001:10001

# Collect static assets at build time (using dummy fallback for build-time compilation)
RUN SECRET_KEY=build-dummy-key-for-collectstatic python manage.py collectstatic --noinput

# Expose internal WSGI port
EXPOSE 8000

# Container-level native Healthcheck for Docker engine / Docker compose
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Use Tini as PID 1 init process to forward UNIX signals and reap zombie child processes
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-", "core.wsgi:application"]
