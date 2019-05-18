#!/bin/bash

CRNTPWD=$(pwd)

cd ${CRNTPWD}/collector
python main.py ../conf/collector.release.conf &

cd ${CRNTPWD}/server
python  main.py &

cd ${CRNTPWD}/frontend
npm run dev &

cd ${CRNTPWD}/websshBackend
npm start &