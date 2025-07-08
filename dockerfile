# Use a lightweight official Python image as the base
FROM python:3.13-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files to disc
# and ensure output is sent directly to terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for PostgreSQL client libraries (psycopg2)
# and other common Django dependencies.
# UPDATED: Add 'netcat-traditional' for the wait_for_db.sh script
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    netcat-traditional \
    # Clean up apt caches to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file first to leverage Docker's build cache
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait_for_db.sh script and make it executable
COPY wait_for_db.sh /usr/local/bin/wait_for_db.sh
RUN chmod +x /usr/local/bin/wait_for_db.sh

# Copy the rest of your Django project code into the container
COPY . /app

# Expose the port your Django application will run on
EXPOSE 8000

# Define the command to run your Django application (now handled by docker-compose)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] # This will be overridden by docker-compose
