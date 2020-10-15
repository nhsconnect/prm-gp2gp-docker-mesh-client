FROM openjdk:8

ENV TEST_MESH_MAILBOX_NAME=abc
ENV TEST_MESH_MAILBOX_PASSWORD=abc
ENV PROD_MESH_MAILBOX_NAME=abc
ENV PROD_MESH_MAILBOX_PASSWORD=abc
ENV KEYSTORE_PASSWORD=abc

COPY . .

RUN apt-get update
RUN apt-get install -y gettext-base
RUN ./install-mesh-client-script.sh
