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
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy the compiled frontend from Stage 1
COPY --from=frontend-build /frontend/dist ./dist

# Set environment variables
ENV PORT=8080
ENV GCP_PROJECT_ID=promptwars-c2
ENV GCP_LOCATION=us-central1
ENV PYTHONPATH=/app

# Start the unified server
CMD ["python", "-m", "backend.main"]
