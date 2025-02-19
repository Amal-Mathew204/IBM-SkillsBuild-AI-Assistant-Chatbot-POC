# WIP Project - Running with Docker Compose

## Overview
This project is a chatbot designed for the IBM SkillsBuild platform, providing interactive responses and support for users. It helps users find appropriate courses based on their interests, skills, and career goals within the IBM SkillsBuild platform. By analyzing user queries, the chatbot suggests relevant learning paths and resources to enhance their learning experience.  

The project leverages a full-stack environment with a frontend (Vue), backend (Django), NGINX reverse proxy, and MongoDB, all containerized using Docker Compose.  

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Navigate to Project

```sh
# Navigate to the root path of project
cd /path/to/your/project
```
## Run the Project
```sh
# Stop and Remove Existing Containers and Volumes
docker compose down -v

# Rebuild and Start the Containers
docker compose up --build

# Check logs to ensure all services are running
docker compose logs -f

# Stop the containers when needed
docker compose down
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

