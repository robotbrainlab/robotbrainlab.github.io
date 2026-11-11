# Docker Cheat Sheet

## Images and Containers

| Command | What it does |
|---|---|
| `docker build -t tinyapp:1.0.0 .` | Build an image from the Dockerfile here, and name it |
| `docker images`, `docker rmi IMAGE` | List images; delete one (or one of its names) |
| `docker tag IMG localhost:5001/IMG` | Add a registry address to an image's name |
| `docker push NAME`, `docker pull NAME` | Upload to, or download from, a registry |
| `docker run --rm IMAGE COMMAND` | Run a one-off container, removed when it exits |
| `docker run -d --name N -p 8080:8000 IMAGE` | Run in the background, forwarding host port 8080 to 8000 |
| `… -e KEY=value`, `--env-file .env` | Pass configuration as environment variables |
| `… -v VOLUME:/path`, `-v "$PWD":/path` | Attach a volume, or a folder from your machine |
| `… --restart unless-stopped` | Restart it whenever it exits, until you stop it |
| `docker ps`, `docker ps -a` | List running containers, or all of them |
| `docker logs N`, `docker exec N COMMAND` | See its output; run a command inside it |
| `docker inspect --format '{{.State.Health.Status}}' N` | Show one field, here the health status |
| `docker rm -f N` | Stop and remove a container |
| `docker volume create V`, `docker network create NET` | Create a volume or a network (`rm` deletes) |

## Compose

| Command | What it does |
|---|---|
| `docker compose up -d` | Build if needed, then start everything in `compose.yaml` |
| `docker compose ps`, `logs SERVICE` | List the project's containers; show a service's output |
| `docker compose down` | Remove containers and networks; keep volumes (`-v` deletes them) |

## Dockerfile Instructions

| Instruction | Purpose |
|---|---|
| `FROM image:tag` | The base image to start from |
| `WORKDIR /app`, `COPY src dest` | Set the working folder; copy files into the image |
| `RUN command` | Run a command while building |
| `ENV KEY=value` | Set an environment variable in the image (never a secret) |
| `USER name` | Run as this user instead of root |
| `EXPOSE 8000` | Document the port the app listens on |
| `HEALTHCHECK … CMD command` | How Docker checks that the app works |
| `CMD ["program", "arg"]` | The command a container runs at start |
