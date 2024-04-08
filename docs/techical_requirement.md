# Technical Discussion Base
## Context:
You work for an industrial company in the quality department. This company
records anomalies detected on products via a dedicated interface. She wishes
implement an intelligence-based anomaly recommendation system
artificial. The objective is to detect similar anomalies in the database by
bringing together the descriptions of each of them. So looking at what has been put into place
works to manage the anomaly, the operator can easily find the solution to the problem
raised and guarantee a quality production chain.
Your recommendation system is an API in Django where as input we give a
anomaly based on its ID and the system lists similar anomalies.
## Requirements:
### AI Model:
- Implement a feature allowing the Django application to communicate
with the AI model to calculate similar anomalies.
- Make sure the AI model is called asynchronously so as not to
block the operation of the main application

### Storage of Results:
- Once the similarities are calculated, store them in Elasticsearch for
rapid recovery.
- Ensure that the data stored in Elasticsearch includes
user information, recommended product and relevance score.
PostgreSQL Data Manipulation:
- Store user data, anomalies and components in one

### Postgresql database.
- Use data stored in PostgreSQL to feed the AI model and
to enrich the recommendation information stored in Elasticsearch.

### Testing:
- Write unit tests for each implemented feature.
- Ensure testing covers all edge cases and ensures correct
operation of the application.
Documentation:
- Document the overall architecture of your application.
- Justify each architectural choice

#### Note 1: 
Make sure the final API can be launched from a Docker image, with all
Necessary dependencies correctly configured.
Docker deployment:
Evaluation criteria
- Correct implementation of the required functionalities, respecting the best
Django development practices.
- Quality and completeness of tests
- Clarity and relevance of the documentation provided.
- Ability to create a working Docker image for the final API, with all the
dependencies correctly managed.

#### Note 2:
- Make sure to create test data for PostgreSQL