terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6"
    }
  }
}

provider "docker" {}

variable "app_version" {
  type    = string
  default = "1.0.0"
}

variable "db_password" {
  type      = string
  sensitive = true
}

resource "docker_network" "lab" {
  name = "tinyapp-net"
}

resource "docker_volume" "db_data" {
  name = "tinyapp-db-data"
}

resource "docker_image" "postgres" {
  name         = "postgres:16-alpine"
  keep_locally = true
}

resource "docker_image" "app" {
  name         = "localhost:5001/tinyapp:1.0.0"
  keep_locally = true
}

resource "docker_container" "db" {
  name  = "tinyapp-db"
  image = docker_image.postgres.image_id
  env = [
    "POSTGRES_USER=tinyapp",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=tinyapp",
  ]

  networks_advanced {
    name = docker_network.lab.name
  }

  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }

  healthcheck {
    test     = ["CMD", "pg_isready", "-U", "tinyapp"]
    interval = "2s"
    retries  = 10
  }
  wait = true
}

resource "docker_container" "app" {
  name  = "tinyapp-web"
  image = docker_image.app.image_id
  env = [
    "APP_VERSION=${var.app_version}",
    "DATABASE_URL=postgresql://tinyapp:${var.db_password}@${docker_container.db.name}:5432/tinyapp",
  ]

  networks_advanced {
    name = docker_network.lab.name
  }

  ports {
    internal = 8000
    external = 8090
  }
  wait = true
}

output "url" {
  value = "http://localhost:8090"
}
