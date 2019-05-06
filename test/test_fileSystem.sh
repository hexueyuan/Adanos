#!/bin/bash

SERVER='http://localhost'
PORT='8081'

URI='fileSystem'
METHOD='GET'
ARGS=''
curl -X ${METHOD} ${SERVER}:${PORT}/${URI}?${ARGS};echo ""
