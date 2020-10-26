FROM openjdk:8

ENV MESH_APP_HOME=/mesh-app
ENV MESH_DATA_HOME=/mesh-data
ENV MESH_SCRIPTS_HOME=/mesh-scripts

COPY *.sh $MESH_SCRIPTS_HOME/
COPY *.cfg $MESH_SCRIPTS_HOME/

RUN apt-get update && apt-get install -y gettext-base unrar-free
RUN ./$MESH_SCRIPTS_HOME/install-mesh-client.sh

CMD ./$MESH_SCRIPTS_HOME/start-client.sh
