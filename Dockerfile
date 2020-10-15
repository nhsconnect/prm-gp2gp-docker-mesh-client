FROM openjdk:8

COPY . .

RUN apt-get update && apt-get install -y gettext-base unrar-free
RUN ./install-mesh-client-script.sh
