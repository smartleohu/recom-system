# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt ./entrypoint.sh /app/
COPY ./recom_system /app/recom_system
COPY ./manage.py ./setup.py /app/

# Create a directory for log files
RUN mkdir -p /app/logs

# Remove any existing .pyc files
RUN find . -name "*.pyc" -exec rm -f {} +

# Install any needed dependencies specified in requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Postgres and RabbitMQ, and configure
RUN apt-get update \
    && apt-get install -y postgresql rabbitmq-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && service postgresql start \
    && su - postgres -c "psql -c \"CREATE USER hur WITH PASSWORD 'PASSWORD';\"" \
    && su - postgres -c "createdb -O hur recom_data3" \
    && service postgresql stop \
    && service rabbitmq-server start

# Update Django settings
RUN sed -i 's/localhost/127.0.0.1/g' /app/recom_system/settings.py

# Expose the port the app runs on (not really needed in the Dockerfile)
EXPOSE 8000

# Change permissions for entrypoint.sh to make it executable
RUN chmod +x /app/entrypoint.sh

# Specify the command to start the server using the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
