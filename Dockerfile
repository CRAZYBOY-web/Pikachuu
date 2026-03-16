# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for some Python packages (like tgcrypto)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . /app

# Upgrade pip and install Python requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Force unbuffered output to see logs in real-time
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "main.py"]
