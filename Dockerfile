FROM python:3.10-slim

WORKDIR /app

# Copy dependency definition and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./backend/

EXPOSE 8000

# Start command for FastAPI backend
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]