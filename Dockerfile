# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/
COPY ./recom_system /app/recom_system
COPY ./manage.py /app/
COPY ./setup.py /app/

# Remove the migrations directory
RUN rm -rf /app/recom_system/app/migrations

# Remove any existing .pyc files
RUN find . -name "*.pyc" -exec rm -f {} +

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Postgres and RabbitMQ, and configure
RUN apt-get update \
    && apt-get install -y postgresql rabbitmq-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Start PostgreSQL service and configure it
RUN service postgresql start \
    && su - postgres -c "psql -c \"CREATE USER hur WITH PASSWORD 'PASSWORD';\"" \
    && su - postgres -c "createdb -O hur recom_data3" \
    && service postgresql stop

# Configure RabbitMQ
# RUN rabbitmq-plugins enable rabbitmq_management
# RUN rabbitmqctl add_user myuser mypassword
# RUN rabbitmqctl set_user_tags myuser administrator
# RUN rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"

# Start RabbitMQ service
RUN service rabbitmq-server start

# Update Django settings
RUN sed -i 's/localhost/127.0.0.1/g' /app/recom_system/settings.py

# Expose the port the app runs on (not really needed in the Dockerfile)
EXPOSE 8000

# The command to start the server will be provided in docker-compose.yml
CMD ["python", "manage.py", "runserver_with_celery", "0.0.0.0:8000"]
