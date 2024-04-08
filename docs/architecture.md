# AI Model:

I have mocked the AI model by random choice of the Postgresql for the moment.
It can be replaced by the Open AI for the recommandation calculation.

# Storage of Results:

I have used Elasticsearch to store the results of similarity calculations.
Maintain user information, recommended product, and relevance score in
Elasticsearch documents.
I have used the Elasticsearch API to interact with the Elasticsearch cluster
from
Django.

# PostgreSQL Data Manipulation:

I have used PostgreSQL to store user profile, anomaly, and component data.
Create Django models to map this relational data.
Use data stored in PostgreSQL to train the AI model and enrich the
recommendation information stored in Elasticsearch.

# Testing:

I have written unit tests using libraries like Django TestCase to test each
feature in isolation.
The tests cover edge cases and ensure the application works properly.

# Celery

I have used Celery to call AI model asynchronously.

# Process

## POST

- POST anomaly_id with optional **user_name** to our app that calls AI model
- Our app returns the **task_result_id** immediately not blocking the system
- AI model calculate similarities by celery for our app
- Result will be stocked in ElasticSearch with **task_result_id** and optional
  **user_name**

## GET

- GET the solutions by **task_result_id** and optional **user_name** to our app
- Our app will find the solutions stocked in ElasticSearch
- Our app will return the solutions