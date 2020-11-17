#!/bin/bash
set -e

INSTALLER_URL=https://digital.nhs.uk/binaries/content/assets/website-assets/services/message-exchange-for-social-care-and-health-mesh/mesh-installation-pack-client-6-2-0.rar 

cd ${MESH_SCRIPTS_HOME}

curl ${INSTALLER_URL} --output mesh-installer.rar

unrar mesh-installer.rar

rm mesh-installer.rar
