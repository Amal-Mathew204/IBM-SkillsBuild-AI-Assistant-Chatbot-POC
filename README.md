# WIP Final-Year Project 2024/25 (Group 2): AI Assistant for IBM SkillsBuild – for Data Science 

## Overview
This project is a AI Assistant Chatbot designed for the IBM SkillsBuild platform, providing interactive responses and support for users. It helps users find appropriate data science courses based on their interests, skills, and career goals within the IBM SkillsBuild platform. By analyzing user queries, the chatbot suggests relevant learning paths and resources to enhance their learning experience.  


The project is a multi container application, with the following components:
- Frontend (Vue.js): Responsbile for running the User interface
- Backend (Django.js): Responsbile for handling API requests from the frontend and communication between the LLM container
- Caddy: Reverse Proxy with HTTPS Connections
- LLM (FastAPI): Runs trained Llama 3.2 model for chatbot and user conversations
- Semantic Search (FastAPI): Runs jinaai/jina-embeddings-v3 embedding model for semantic search to get course recommendation
- Reverse Search (FastAPI/ ElasticSearch Engine): Uses ElasticSearch engine to find similar courses using reverse search
- MongoDB: Database for the application

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)


## Run the Project
To run the project run the following commands ensuring terminal is pointing at the projects root directory:
```sh

# Start the Containers and run applications
docker compose up

# Rebuild and Start the Containers
docker compose up --build
```

The logs for each container can be viewed through Docker Desktop or using the following command
```sh

# Check logs to ensure all services are running
docker compose logs -f
```
To shutdown the containers and close the application use the following commands:
```sh

# Stop the containers when needed
docker compose down
# Stop and Remove Existing Containers and Volumes
docker compose down -v

```


## Notes

- The `-v` flag removes all volumes for a clean start.
- The `--build` flag forces rebuilding images.

## Troubleshooting

```sh
# Check running containers
docker ps -a

# Verify volumes
docker volume ls

# Free up space
docker system prune -a
```



For more details, refer to the [Docker Compose documentation](https://docs.docker.com/compose/).

## View the Database

- Use MongoDB Compass to view the Database
- MongoDB Compass is a GUI tool for viewing the MongoDB databases, allowing visualization, querying, and data manipulation.
- For more details see [MongoDB Compass](https://www.mongodb.com/products/tools/compass)

## Contributors
* [Mohamed Zahidur Rahman](https://github.com/Zahid2104)
* [Amal Mathew](https://github.com/Amal-Mathew204)
* [Aamir Naje](https://github.com/aamirnaje)
* [Aylin Turan](https://github.com/Aylinx13)




