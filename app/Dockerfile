FROM python:3.11-slim

# Basic hardening + predictable Python behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

# Install deps first (better layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /srv/app
USER appuser

# Expose the API port
EXPOSE 8000

# NOTE:
# Use ONE of the two CMD lines below depending on how your imports are structured.
# Start with CMD A. If it fails (import errors), switch to CMD B.

# CMD A: If you run locally as: uvicorn main:app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# CMD B: If you run locally as: uvicorn app.main:app  (package-style)
# CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
