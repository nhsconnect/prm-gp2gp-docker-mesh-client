#!/bin/bash

java -jar mesh-6.2.0_20180601-installer-signed.jar << EOF
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

envsubst < ${MESH_SCRIPTS_HOME}/config-template.cfg > $MESH_APP_HOME/meshclient.cfg

cd $MESH_APP_HOME
java -jar -Dlog4j.configuration=file:./log4j.xml meshClient.jar ./meshclient.cfg
