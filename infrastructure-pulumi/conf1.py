import os
import pulumi
import pulumi_docker as docker

# Crear red
network = docker.Network("network")

# Ruta absoluta al directorio de logs
host_logs_path = os.path.abspath("./logs")

# Ruta absoluta al directorio de datos de Portainer
host_portainer_data_path = os.path.abspath("./portainer_data")

# MongoDB
mongo_container = docker.Container("mongo",
    image="mongo:latest",
    ports=[docker.ContainerPortArgs(
        internal=27017,
        external=27017,
    )],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
)

# SonarQube
sonarqube_container = docker.Container("sonarqube",
    image="sonarqube:latest",
    ports=[docker.ContainerPortArgs(
        internal=9000,
        external=9000,
    )],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
)

# Flask App
flask_container = docker.Container("flask-app",
    image="lugudu/borrow-books-app:latest",
    ports=[docker.ContainerPortArgs(
        internal=5000,
        external=5000,
    )],
    volumes=[docker.ContainerVolumeArgs(
        host_path=host_logs_path,
        container_path="/app/borrowbooksapp/logs",
    )],
    envs=[
        "MONGO_URI=mongodb://mongo:27017/borrowbooksdb"
    ],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
    opts=pulumi.ResourceOptions(depends_on=[mongo_container])
)

# Contenedor para visualizar los logs
logs_container = docker.Container("logs-viewer",
    image="httpd:latest",
    ports=[docker.ContainerPortArgs(
        internal=80,
        external=8080,
    )],
    volumes=[docker.ContainerVolumeArgs(
        host_path=host_logs_path,
        container_path="/usr/local/apache2/htdocs/logs",
    )],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
    opts=pulumi.ResourceOptions(depends_on=[flask_container])
)

# Contenedor para Portainer (dashboard de contenedores Docker)
portainer_container = docker.Container("portainer",
    image="portainer/portainer-ce:latest",
    ports=[docker.ContainerPortArgs(
        internal=9000,
        external=9001,  # Puedes cambiar el puerto externo si lo prefieres
    )],
    volumes=[
        docker.ContainerVolumeArgs(
            host_path="/var/run/docker.sock",
            container_path="/var/run/docker.sock",
        ),
        docker.ContainerVolumeArgs(
            host_path=host_portainer_data_path,
            container_path="/data",
        ),
    ],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
)

# Contenedor para Heimdall (dashboard)
heimdall_container = docker.Container("heimdall",
    image="linuxserver/heimdall",
    ports=[docker.ContainerPortArgs(
        internal=80,
        external=8000,  # Puedes cambiar el puerto externo si lo prefieres
    )],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
        name=network.name,
    )],
)