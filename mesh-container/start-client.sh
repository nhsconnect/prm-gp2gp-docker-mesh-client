#!/bin/bash

set -e

if [[ -z "$KEYSTORE_PASSWORD" ]]; then
    echo "Error: KEYSTORE_PASSWORD environment variable is not set, exiting.."
    exit 1
fi

if [[ -z "$MESH_MAILBOX_NAME" ]]; then
    echo "Error: MESH_MAILBOX_NAME environment variable is not set, exiting.."
    exit 1
fi

if [[ -z "$MESH_MAILBOX_PASSWORD" ]]; then
    echo "Error: MESH_MAILBOX_PASSWORD environment variable is not set, exiting.."
    exit 1
fi

java -jar ${MESH_SCRIPTS_HOME}/mesh-6.2.0_20180601-installer-signed.jar << EOF
1
${MESH_APP_HOME}
1
${MESH_DATA_HOME}
O
1
${MESH_MAILBOX_NAME}
0
1
1
1
N
EOF


envsubst < ${MESH_SCRIPTS_HOME}/config-template.cfg > ${MESH_APP_HOME}/meshclient.cfg
cp ${MESH_SCRIPTS_HOME}/log4j.xml ${MESH_APP_HOME}/log4j.xml

cd $MESH_APP_HOME
java -jar -Dlog4j.configuration=file:./log4j.xml meshClient.jar ./meshclient.cfg
