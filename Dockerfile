# --- STAGE 1: Build Frontend ---
FROM node:20-slim AS frontend-build
WORKDIR /frontend

# Copy dependency files and install fresh (Linux-native)
COPY frontend/package*.json ./
RUN npm install

# Copy source
COPY frontend/ ./

# Hardening: Ensure Vite is executable
RUN chmod +x node_modules/.bin/vite

# Build the SPA
RUN npm run build

# --- STAGE 2: Build Backend & Serve Everything ---
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install Python dependencies using UV (100% Efficiency)
COPY backend/requirements.txt ./
RUN uv pip install --no-cache --system -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy the compiled frontend from Stage 1
COPY --from=frontend-build /frontend/dist ./dist

# Set environment variables
ENV PORT=8080
ENV GCP_PROJECT_ID=promptwars-c2
ENV GCP_LOCATION=us-central1
ENV PYTHONPATH=/app

# Start the unified server with production-grade Gunicorn & Uvicorn workers
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "backend.main:app"]
