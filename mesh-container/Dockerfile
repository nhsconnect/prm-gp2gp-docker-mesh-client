FROM openjdk:8

ENV MESH_APP_HOME=/mesh-app
ENV MESH_DATA_HOME=/mesh-data

COPY . .

RUN apt-get update && apt-get install -y gettext-base unrar-free
RUN ./install-mesh-client.sh
