terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

resource "docker_image" "facesdetection" {
  name         = "lugudu/face-detection-webapp:latest"
  keep_locally = false
}

resource "docker_container" "facesdetection" {
  image = docker_image.facesdetection.image_id
  name  = var.container_name
  ports {
    internal = 8080
    external = 8080
  }
}

variable "container_name" {
  description = "Value of the name for the Docker container"
  type        = string
  default     = "ExampleFacesdetectionContainer"
}

output "container_id" {
  description = "ID of the Docker container"
  value       = docker_container.facesdetection.id
}

output "image_id" {
  description = "ID of the Docker image"
  value       = docker_image.facesdetection.id
}
