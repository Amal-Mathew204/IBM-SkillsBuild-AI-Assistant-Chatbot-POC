# WIP Project - Running with Docker Compose

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Steps to Run the Project

```sh
# Navigate to the Project Directory
cd /path/to/your/project

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
- Use `sudo` if permission issues arise.

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

