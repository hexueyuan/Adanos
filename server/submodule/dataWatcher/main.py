# -*- coding: utf-8 -*-
#!/usr/bin/env python2

from flask import Flask, request, make_response
from flask_socketio import SocketIO, emit
from threading import Thread, Lock

import time

app = Flask(__name__)
socketio = SocketIO(app)

dashboard = None
module_name = ''
running = False

timebase = {
    'cpu': 0,
    'memory': 0,
    'disk': 0
}
threadLock = Lock()

def CPUData():
    logger = dashboard.getLogger('dataWatcher')
    database = dashboard.getDatabase('dataWatcher')
    config = dashboard.getConfig('dataWatcher')

    if timebase['cpu'] == 0:
        cnt_time = int(time.time())
        start = cnt_time - 300
        timebase['cpu'] = cnt_time
    else:
        start = timebase['cpu']

    rv = []
    conn = database.connectDB()
    cur = conn.cursor()
    select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('cpu'), start)
    logger.debug("CPU data select sql: {}".format(select_sql))
    conn = database.connectDB()
    cur = conn.cursor()
    cur.execute(select_sql)
    rv = []
    for r in cur.fetchall():
        rv.append({
            'timestamp': r[0],
            'logical_cnt': r[1],
            'phtsics_cnt': r[2],
            'used_rate': r[3],
            'user_time_percent': r[4],
            'system_time_percent': r[5],
            'idle_time_percent': r[6]
        })
    cur.close()
    conn.close()
    logger.debug("cpu new data: {} records.".format(len(rv)))
    if len(rv) > 0:
        timebase['cpu'] = rv[-1]['timestamp']
    return rv

def MemoryData():
    logger = dashboard.getLogger('dataWatcher')
    database = dashboard.getDatabase('dataWatcher')
    config = dashboard.getConfig('dataWatcher')

    if timebase['memory'] == 0:
        cnt_time = int(time.time())
        start = cnt_time - 300
        timebase['memory'] = cnt_time
    else:
        start = timebase['memory']

    rv = []
    conn = database.connectDB()
    cur = conn.cursor()
    select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('memory'), start)
    logger.debug("Memory data select sql: {}".format(select_sql))
    conn = database.connectDB()
    cur = conn.cursor()
    cur.execute(select_sql)
    rv = []
    for r in cur.fetchall():
        rv.append({
            'timestamp': r[0],
            'mem_total': r[1],
            'mem_used_rate': r[2],
            'swap_total': r[3],
            'swap_used_rate': r[4],
            'swap_sin': r[5],
            'swap_sout': r[6]
        })
    cur.close()
    conn.close()
    logger.debug("memory new data: {} records.".format(len(rv)))
    if len(rv) > 0:
        timebase['memory'] = rv[-1]['timestamp']
    return rv

def DiskData():
    logger = dashboard.getLogger('dataWatcher')
    database = dashboard.getDatabase('dataWatcher')
    config = dashboard.getConfig('dataWatcher')

    if timebase['disk'] == 0:
        cnt_time = int(time.time())
        start = cnt_time - 300
        timebase['disk'] = cnt_time
    else:
        start = timebase['disk']

    rv = []
    conn = database.connectDB()
    cur = conn.cursor()
    select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('disk'), start)
    logger.debug("Disk data select sql: {}".format(select_sql))
    conn = database.connectDB()
    cur = conn.cursor()
    cur.execute(select_sql)
    rv = []
    for r in cur.fetchall():
        rv.append({
            'timestamp': r[0],
            'device_name': r[1],
            'mount_point': r[2],
            'fstype': r[3],
            'total': r[4],
            'used_rate': r[5]
        })
    cur.close()
    conn.close()
    logger.debug("disk new data: {} records.".format(len(rv)))
    if len(rv) > 0:
        timebase['disk'] = rv[-1]['timestamp']
    return rv

def collectorData():
    logger = dashboard.getLogger('dataWatcher')
    datas = {
        'cpu': CPUData,
        'memory': MemoryData,
        'disk': DiskData
    }
    rv = {}
    global running
    while running:
        for name, handler in datas.items():
            rv[name] = handler()
        socketio.emit('onNewData', rv, namespace='/')
        logger.debug("{} cpu records emit".format(len(rv)))
        socketio.sleep(5)
    logger.info("running is False")

@socketio.on('connect', namespace='/')
def connect():
    logger = dashboard.getLogger('dataWatcher')
    logger.debug("ready to get lock")
    with threadLock:
        logger.debug("Get lock key")
        global running
        running = True
        socketio.start_background_task(target=collectorData)
    logger.info("new connect")

@socketio.on('disconnect', namespace='/')
def disconnect():
    logger = dashboard.getLogger('dataWatcher')
    global running
    running = False
    logger.info("disconnect")

def run(name, global_dashboard):
    global dashboard, module_name
    dashboard = global_dashboard
    module_name = name
    socketio.run(app, port=8081)