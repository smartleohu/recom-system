# Anomaly Recommendation System API

## Overview:

The Anomaly Recommendation System API is a Django-based application designed to
provide recommendations for anomalies detected in industrial products. The
system utilizes artificial intelligence to identify similar anomalies based on
past occurrences, enabling operators to quickly find solutions and ensure a
quality production chain.

## Features:

- **AI Model Integration**: The Django application communicates asynchronously
  with an AI model to calculate similar anomalies, ensuring optimal performance
  and responsiveness.
- **Storage of Results**: Calculated similarities are stored in Elasticsearch,
  facilitating rapid retrieval and analysis. Each stored result includes user
  information, recommended product, and relevance score.
- **PostgreSQL Data Management**: User data, anomaly records, and product
  components are stored in a PostgreSQL database. This data serves as the
  primary source for the AI model and enriches recommendation information in
  Elasticsearch.
- **Testing Suite**: A comprehensive suite of unit tests (pytest) covers each
  implemented feature, including edge cases, to ensure the correct operation of
  the application.
- **Detailed Documentation**: The project includes thorough documentation
  outlining the overall architecture, design decisions, and usage instructions,
  providing clarity and guidance for developers and stakeholders.

## Architecture:

- **Django Framework**: The core of the API, handling HTTP requests and
  responses, as well as business logic implementation.
- **AI Model**: An external artificial intelligence model integrated with
  Django asynchronously to perform anomaly similarity calculations.
- **Elasticsearch**: A distributed search and analytics engine used for storing
  recommendation results, allowing for efficient querying and analysis.
- **PostgreSQL Database**: The primary data store for user data, anomaly
  records, and product components, facilitating data management and retrieval.
- **Docker Containerization**: The application can be containerized using
  Docker, ensuring consistent deployment across different environments with all
  dependencies properly configured.

[Click here for details](docs/architecture.md)

## Development Environment:

- MacOS
- Pycharm: Python >= 3.10

## Installation:

1. **Services**
    - elasticsearch-full: for fast look-up of result calculated by AI model
      when send GET result request
    - postgresql@14: to store Anomaly, PowerComponent, UserProfile
    - rabbitmq: for celery to develop the asynchronous POST anomaly request et
      GET result request
    - docker: for docker image

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/smartleohu/recom-system.git
3. Install Dependencies:
   ```bash 
   pip install -r requirements.txt
4. Pass all unit tests:
   ```bash 
   pytest
5. Apply Database Migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

## Configuration:

1. launch all services
   ```bash
   brew services start elasticsearch-full
   brew services start postgresql@14
   brew services start rabbitmq 
   brew services list
   
    Name               Status  User      File
    elasticsearch-full started leo ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch-full.plist
    postgresql@14      started root      ~/Library/LaunchAgents/homebrew.mxcl.postgresql@14.plist
    rabbitmq           started root      ~/Library/LaunchAgents/homebrew.mxcl.rabbitmq.plist

2. **Postgres**:
   ```bash
   psql recom_data2
   recom_data2=# SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE';
              table_name          
    ------------------------------
     django_migrations
     app_userprofile
     app_anomaly_user_names
     app_anomaly
     app_powercomponent
     app_powercomponent_anomalies

3. launch app web service for recom_system
   ```bash
   # create intial anomalies to AI models
   python manage.py runserver_with_celery 0.0.0.0:8000
   # if you want to clear elesticsearsh 
   python manage.py reset_elesticsearsh
   # launch recom_system.app 
   python manage.py runserver_with_celery 0.0.0.0:8000

## Application

### Documentation Browser

http://127.0.0.1:8000/swagger/
![alt text](docs/RecommandationSystem.png)

[Click here for Swagger](docs/RecommandationSystem.pdf)

### Manipulation

1. **POST**:
    - fill out the body of the request by
         ```javascript
         {
           "anomaly_id": "N99",
           "user_name": "DefaultUser" # this is optional
         }
    - you will get back the task result id quickly
      _e.g. 8f3a6c09-0842-4489-b225-3465867941f2_,
      and you will use it in the next step
    - you can post simultaneously many requests without any process blocking,
      and you will get different task result ids to use in the next step.

2. **GET**:
   fill out the parameter values
   *
   *_task_result_id=8f3a6c09-0842-4489-b225-3465867941f2&user_name=DefaultUser_
   **,
   and you will get back the corresponding calculated results for related
   anomalies

### Docker run

1. check out docker-compose.yml and Dockerfile
2. launch
    ```bash
   docker-compose up