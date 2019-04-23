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
    'diskEventLock': Lock()
}
thread = None

def data_init():
    now = int(time.time())
    for t in range(now - 100, now):
        cpu_load_init.append({
            "time": t,
            "value": round(random.random(), 2)
        })

#def readDiskUseRate(start_timestamp, end_timestamp):
#    use_rate = defaultdict(list)
#    mount_points = conf['disk_mount_point']
#    conn = sqlite3.connect('../database/system.db')
#    c = conn.cursor()
#    for point in mount_points:
#        sql = "select mount_point, use_rate, timestamp, total_space from disk_use_rate where mount_point=\"{}\" order by timestamp desc limit {};".format(point, conf["default_search_count"])
#        cursor = c.execute(sql)
#        for cur in cursor:
#            use_rate[point].append({
#                "mount_point": cur[0],
#                "use_rate": cur[1],
#                "timestamp": cur[2],
#                "total_space": cur[3]
#            })
#    return {"mount_points": mount_points, "use_rate": use_rate}

def readCpuTableMock(start_timestamp, end_timestamp):
    if start_timestamp == 0 or end_timestamp == 0:
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 100
    data = {
        "load": [],
        "top20": []
    }
    cpu_load_init.pop(0)
    cpu_load_init.append({
        "time": int(time.time()),
        "value": round(random.random(), 2)
    })
    data['load'] = cpu_load_init

    for x in xrange(0, 20):
        data['top20'].append({
            "name": "program" + str(x),
            "cpu": round(random.uniform(0, 1), 2),
            "mem": round(random.uniform(0, 1), 2),
            "pid": str(x + 20000),
            "user": "hexueyuan",
            "time": "1:03:02"
        })

    return data

def readMemoryTableMock(start_timestamp, end_timestamp):
    if start_timestamp == 0 or end_timestamp == 0:
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 20
    data = {
        "memory": {
            "currentUseRate": 0,
            "total": 0,#MB
            "rest": 0,
            "selectTimeslotUseRate": []
        },
        "swap": {
            "currentUseRate": 0,
            "total": 0,
            "rest": 0,
            "selectTimeslotUseRate": []
        }
    }
    data['memory']['currentUseRate'] = round(random.random(), 2)
    data['memory']['total'] = 16 * 1024
    data['memory']['rest'] = data['memory']['total'] * data['memory']['currentUseRate']
    data['swap']['currentUseRate'] = round(random.random(), 2)
    data['swap']['total'] = 20 * 1024
    data['swap']['rest'] = data['swap']['total'] * data['swap']['currentUseRate']

    for t in range(start_timestamp, end_timestamp):
        data['memory']['selectTimeslotUseRate'].append({'time': t, 'value': round(random.random(), 2)})
        data['swap']['selectTimeslotUseRate'].append({'time': t, 'value': round(random.random(), 2)})
    return data

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

@socketio.on('cpuDataRequest', namespace='/')
def cpuEvent_connect():
    global thread
    with thread_lock_state['cpuEventLock']:
        socketio.start_background_task(target=sendCPUData)

@socketio.on('diskDataRequest', namespace='/')
def diskEvent_connect():
    global thread
    with thread_lock_state['diskEventLock']:
        socketio.start_background_task(target=sendDiskData)

@app.route('/smwsAPI/cpu_info', methods = ['GET'])
def cpuInfo():
    start_time = request.args.get('start', 0)
    end_time = request.args.get('end', 0)
    responseData = {
        "status": "success",
        "errMsg": None,
        "data": readCpuTableMock(start_time, end_time)
    }
    resp = make_response(json.dumps(responseData))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/smwsAPI/memory_info', methods = ['POST'])
def MemoryInfo():
    start_time = request.form.get('start_time_second', 0)
    end_time = request.form.get('end_time_second', 0)
    responseData = {
        "status": "success",
        "errMsg": None,
        "data": readMemoryTableMock(start_time, end_time)
    }
    resp = make_response(json.dumps(responseData))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No configure in"
        exit(0)
    with open(sys.argv[1]) as f:
        context = f.read()
        conf = json.loads(context)
    data_init()
    socketio.run(app, debug=True, port=5001)
