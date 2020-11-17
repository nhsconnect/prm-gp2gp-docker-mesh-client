FROM openjdk:8

ENV MESH_APP_HOME=/mesh/app
ENV MESH_DATA_HOME=/mesh/data
ENV MESH_SCRIPTS_HOME=/mesh/scripts

RUN apt-get update && apt-get install -y gettext-base unrar-free
RUN groupadd -r -g 999 mesh && useradd -r -g mesh -u 1000 mesh

RUN mkdir -p $MESH_APP_HOME && mkdir -p $MESH_DATA_HOME

COPY *.sh $MESH_SCRIPTS_HOME/
COPY *.cfg $MESH_SCRIPTS_HOME/
COPY log4j.xml $MESH_SCRIPTS_HOME/

RUN chown -R mesh:mesh /mesh

USER mesh

RUN ./$MESH_SCRIPTS_HOME/download-installer.sh

CMD ./$MESH_SCRIPTS_HOME/start-client.sh
