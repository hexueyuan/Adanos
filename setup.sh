#!/bin/bash

current=$(pwd)

dependencies=('Flask' 'flask-socketio' 'pathlib2', 'psutil')

for dependency in ${dependencies[@]};
do
    echo "install:" ${dependency}
    pip install ${dependency}
done

cd ${current}/websshBackend
npm install

mkdir -p ${current}/log/{backendAPI,collector}