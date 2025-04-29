# Semantic Search Module
The Semantic Search Module is an application that uses Textual Embedding Models to determine which top k courses are the most relevent to recommend to the user, based on the semantic textual similary between each SkillsBuild course (stored on the projects database) to a given query (users conversation context).

## Features

### FastAPI Application
The Semantic Search Module is designed to be deployed as a single container via Docker (with the `.DockerFile` defining the Docker Image of the implementation). The implmentation uses a Uvicorn Server to run a FastAPI application, exposing an endpoint to access and use the Semantic Search Module. 

When running the Docker Image of the Semantic Search module, the FastAPI application has a Server StartUp Function. This function creates an embedded dataset of Courses to be stored on the applications Database Server, before the endpoint is available for access to execute a semantic search of courses.

To obtain courses recommendations to the AI Assistant Chatbot a HTTP Request must be sent to the API endpoint, passing a query for semantic search and the number of courses to recommend. Once a request is recieved the Module retrieves the embedded dataset cached on the Applications Database to run a semantic search. Once completed the Module provides an API response, containing in the response body, with a list of JSON objects which are the courses to recommend to the user.

In the console for the semantic search module a logging system is used to record the progress of server startup and the default FASTAPI logger is used to record any requests made to the application.

### Testing
#### Unit Testing
The `./test.py` file contains all the unit tests for the: database connections/methods, embedding and semantic search functions used by the Sementic Search Module.
#### Benchmark Testing
The `./benchmark.py` contains the benchmark testing code of the semantic search module. This measures the exectution time (s) and memory usage (MB) of embedded dataset creation task (the most computationally intentsive task undertaking by the semantic search module).

## API EndPoint CORS Policy
The following restrictions are applied to incomming HTTP requests for the FASTAPI endpoints of the semantic search module:
- Allow Only GET Methods
- Only Accept Requests with the same origin as the Semantic Search Module

## API Reference
All API Endpoints are defined in the `./main.py` file. Please note in the urls listed bellow you must replace the **'http://api.url'** with the URL you are using to deploy the application.
### Course Recommendation API Endpoint
```
http://api.url/{query}/{k}
```
Path Parameters:
- query (str): User Input query to obtain courses
- k (int): Top number of courses to be returned by the semantic search module
### FASTAPI Automated Docs
This url can be used to view and test the API Endpoints of the FASTAPI application
```
http://api.url/docs
```

## Configuration
The `.env` file contains the template enviroment variables to run the semantic search module as an internal container for the AI Assistant Chatbot Application for **LOCAL HOST DEPLOYMENT**

## Dependencies
To run the Semantic Search Module, the application is required to connect to a MongoDB Database Server. The implementation is designed to use the database connections to source the courses available to recommend to the user and to cache an embedded dataset of courses. 


## To Run the Project
The Module is not designed to be run independently, but as an internal component for an AI Assistant Chatbot run via Docker Compose. To see how this component is integrated and executed within the Chatbot application please head to the [AI Assistant Chatbot repository](https://github.com/Amal-Mathew204/IBM-SkillsBuild-AI-Assistant-Chatbot-POC).

