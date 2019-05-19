#!/bin/bash

current=$(pwd)

dependencies=('Flask' 'flask-socketio' 'pathlib2')

for dependency in ${dependencies[@]};
do
    echo "install:" ${dependency}
    pip install ${dependency}
done

cd ${current}/websshBackend
npm install

mkdir ${current}/log/{backendAPI,collector}