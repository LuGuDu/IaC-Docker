import pulumi
from pulumi_docker import Image, Container

image_name = "lugudu/face-detection-webapp"

container = Container("face-detection-webapp-pulumi",
                      image=image_name,
                      ports=[{
                          "internal": 8080,
                          "external": 8080
                      }])

# Exportar la dirección del contenedor
pulumi.export("container_id", container.id)
pulumi.export("container_name", container.name)