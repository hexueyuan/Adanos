#!/bin/bash

CRNTPWD=$(pwd)
export PYTHONPATH=${CRNTPWD}"/lib"
cd ${CRNTPWD}/collector
python main.py ../conf/collector.release.conf &

cd ${CRNTPWD}/server
python  main.py ../conf/application.conf &

cd ${CRNTPWD}/websshBackend
npm start &