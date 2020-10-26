#!/bin/bash

envsubst < ${MESH_SCRIPTS_HOME}/config-template.cfg > $MESH_APP_HOME/meshclient.cfg

cd $MESH_APP_HOME
java -jar -Dlog4j.configuration=file:./log4j.xml meshClient.jar ./meshclient.cfg
