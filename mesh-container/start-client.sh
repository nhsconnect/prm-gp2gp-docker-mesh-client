#!/bin/bash

envsubst < ${MESH_SCRIPTS_HOME}/config-template.cfg > $MESH_APP_HOME/meshclient.cfg

cd $MESH_APP_HOME
java -jar meshClient.jar ./meshclient.cfg
