# -*- coding: utf-8 -*-
#!/usr/bin/env python2

from flask import Flask, request, make_response
from flask_socketio import SocketIO
from threading import Thread, Lock
from collections import defaultdict

import sqlite3
import json
import sys
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)
conf = {}
cpu_load_init = []
thread_lock_state = {
    'cpuEventLock': Lock(),
    'diskEventLock': Lock(),
    'memoryEventLock': Lock()
}

def sendCPUData():
    while True:
        t = int(time.time())
        load = round(random.random(), 2) * 100
        user = round(random.random(), 2) * 100
        system = round(random.random(), 2) * 100
        idle = round(random.random(), 2) * 100
        nice = round(random.random(), 2) * 100
        socketio.emit('onCPUData', {
            'time'  : t,
            'load'  : load,
            'user'  : user,
            'system': system,
            'idle'  : idle,
            'nice'  : nice
        }, namespace='/')
        socketio.sleep(3)

def sendDiskData():
    while True:
        t = int(time.time())
        use_rate = round(random.random(), 2)
        total = 50
        used = total * use_rate
        free = total * (1 - use_rate)
        active = round(random.random(), 2) * total
        inactive = round(random.random(), 2) * total
        socketio.emit('onDiskData', {
            'time'      : t,
            'use_rate'  : use_rate * 100,
            'total'     : total,
            'used'      : used,
            'free'      : free,
            'active'    : active,
            'inactive'  : inactive
        }, namespace='/')
        socketio.sleep(3)

def sendMemorydata():
    while True:
        t = int(time.time())
        use_rate = round(random.random(), 2)
        total = 16
        used = total * use_rate
        free = total * (1 - use_rate)
        socketio.emit('onMemoryData', {
            'time'      : t,
            'use_rate'  : use_rate * 100,
            'total'     : total,
            'used'      : used,
            'free'      : free
        }, namespace='/')
        socketio.sleep(3)

@socketio.on('cpuDataRequest', namespace='/')
def cpuEvent_connect():
    with thread_lock_state['cpuEventLock']:
        socketio.start_background_task(target=sendCPUData)

@socketio.on('diskDataRequest', namespace='/')
def diskEvent_connect():
    with thread_lock_state['diskEventLock']:
        socketio.start_background_task(target=sendDiskData)

@socketio.on('memoryDataRequest', namespace='/')
def memoryEvent_connect():
    with thread_lock_state['memoryEventLock']:
        socketio.start_background_task(target=sendMemorydata)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
