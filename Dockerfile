# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy

# Expose port FastAPI will run on
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

