# Use an official Python base image
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Install system build deps needed for some Python packages, then clean apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user and group, and a virtualenv
ENV VENV_PATH=/opt/venv
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Use python -m pip and --no-cache-dir to avoid cache files
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create an unprivileged user and give ownership of the app and venv
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser && \
    chown -R appuser:appgroup /app $VENV_PATH

# Switch to non-root user
USER appuser

EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
