# ─── Build Stage ───────────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

# Install build/tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency spec
COPY requirements.txt .

# Install into an isolated directory
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# ─── Final Stage ───────────────────────────────────────────────────────────────
FROM python:3.10-slim

# Create a non-root user for better security
RUN useradd --create-home appuser

WORKDIR /app

# Copy installed packages and source code
COPY --from=builder /install /usr/local
COPY . .

# Drop privileges
USER appuser

# Expose the port Uvicorn will serve on
EXPOSE 8000

# Default entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
