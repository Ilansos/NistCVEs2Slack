# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/nist2slack-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/nist2slack-cron

# Apply cron job
RUN crontab /etc/cron.d/nist2slack-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Command to run the script immediately and then start cron
CMD cron && tail -f /var/log/cron.log

