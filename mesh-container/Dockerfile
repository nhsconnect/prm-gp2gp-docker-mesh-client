FROM openjdk:8

ENV MESH_APP_HOME=/mesh/app
ENV MESH_DATA_HOME=/mesh/data
ENV MESH_SCRIPTS_HOME=/mesh/scripts

RUN mkdir /mesh

COPY *.sh $MESH_SCRIPTS_HOME/
COPY *.cfg $MESH_SCRIPTS_HOME/
COPY log4j.xml $MESH_SCRIPTS_HOME/

RUN apt-get update && apt-get install -y gettext-base unrar-free
RUN ./$MESH_SCRIPTS_HOME/download-installer.sh
RUN groupadd -r -g 999 mesh && useradd -r -g mesh -u 1000 mesh
RUN chown mesh:mesh /mesh

USER mesh

CMD ./$MESH_SCRIPTS_HOME/start-client.sh
