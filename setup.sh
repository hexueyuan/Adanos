#!/bin/bash

dependencies=['Flask', 'flask-socketio']

for dependency in dependencies;
do
    pip install ${dependency}
done