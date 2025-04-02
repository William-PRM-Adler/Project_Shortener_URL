# Stage 1: Build the React frontend
FROM node:18 as frontend

WORKDIR /frontend

COPY frontend_ui/package*.json ./
RUN npm install

COPY frontend_ui/ ./
RUN npm run build

# Stage 2: Backend with FastAPI and built frontend
FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
