#!/bin/bash
set -e

INSTALLER_URL=https://digital.nhs.uk/binaries/content/assets/website-assets/services/message-exchange-for-social-care-and-health-mesh/mesh-installation-pack-client-6-2-0.rar 

curl ${INSTALLER_URL} --output mesh-installer.rar

unrar mesh-installer.rar

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

rm mesh-installer.rar
rm mesh-*-installer-signed.jar
