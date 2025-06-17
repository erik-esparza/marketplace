# Use official Python base image (slim variant)
#This image template is Based on py running on Debian
FROM python:3.11-slim as base

# Set env vars
#PYTHONDONTWRITE... prevents .pyc files from being written — cleaner, especially in containers.
#PYTHONUNBUFFERED ensures logs are streamed immediately to STDOUT/STDERR (needed for logging in Docker).
# STDOUT = literally "standard output", meaning, a normal log.
# STDERR = Similar logic to above's example, but for error logs specifically.
# Access these logs with `docker logs <container_name_or_id>` or use the --details flag to
# differentiate between STDOUT and STDERR messages.
# Interesting tools to manage logs or use them: ELK, Fluentd, or Datadog can collect these logs for analysis.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
# Quite simple, apt is a package manager. apt-get update grabs the loads the latest updates (versions, think of it as refreshing the catalogue of depends.), and install executes the installation. Apt is used by ubuntu/debian/other linux distributions.
# the -y flag means answering "yes" to prompts when installing the dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
#Note the order is of big importance here. We first copy the requirements BEFORE running installations. 
#This is related to how docker uses cache — it caches layer per layer. This layer can then be skipped if the reqs haven't changed
#In other words, this will only install new dependencies, not reinstall everything if it's already cached in these layers
#
# For the flag --no-cache-dir, Prevents pip from caching downloaded .whl (wheel) files in /root/.cache/pip → reduces image size.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

#We copy and run the entrypoint. Note i'm running running this file BEFORE switching users, otherwise Docker won't take it unless we change permissions for the other user, which is why we're switching users in the first place... because they' don't have root privileges.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

## Create a non-root user for running the app
# THEN create the user (this switches context)
RUN adduser --disabled-password --gecos '' flaskuser
USER flaskuser

ENTRYPOINT ["/entrypoint.sh"]
