#!/bin/bash

envsubst < config-template.cfg >> temp.cfg

rm /usr/local/MESH-APP-HOME/meshclient.cfg
mv ./temp.cfg /usr/local/MESH-APP-HOME/meshclient.cfg