# -*- coding: utf-8 -*-
#!/usr/bin/env python2

from threading import Thread, Lock
import time

from .. import socketio, dashboard
from flask import current_app, g

__all__ = []

name = 'dataWatcher'
running = False
threadLock = Lock()
lasttime = {}
logger = dashboard.getPlugin(name, 'logger')
logger.debug("init data watcher.")

@socketio.on('connect', namespace="/")
def connect():
    global name, running, threadLock, dashboard

    logger = dashboard.getLogger(name)
    logger.debug("A new connect ready to get lock")
    with threadLock:
        logger.debug("Get key!")
        running = True
        socketio.start_background_task(target=collectorData)

@socketio.on('disconnect', namespace="/")
def disconnect():
    global running, dashboard
    logger = dashboard.getLogger(name)

    running = False
    logger.info("disconnect")

def collectorData():
    global name, running, dashboard
    logger = dashboard.getPlugin(name, 'logger')
    config = dashboard.getPlugin(name, 'config')
    logger.debug(str(config))
    
    logger.info("start to collect data")

    rv = {}
    datalist = config.get('datalist', [])
    logger.debug(str(datalist))

    lasttime = config.get('lasttime', {})
    for k in datalist:
        t = lasttime.get(k, 0)
        if t == 'now':
            t = int(time.time())
        lasttime[k] = t
    
    while running:
        for k in datalist:
            handler = HandlerFactory.factory(k)
            lasttime[k], rv[k] = handler(lasttime[k])

        socketio.emit('onNewData', rv, namespace='/')
        logger.debug("{} records emit".format(len(rv)))
        socketio.sleep(5)
    logger.info("exit collect data")

class HandlerFactory:
    @staticmethod
    def factory(name):
        if hasattr(HandlerFactory, name):
            return getattr(HandlerFactory, name)
        else:
            return getattr(HandlerFactory, 'NoneData')

    @staticmethod
    def NoneData():
        return None

    @staticmethod
    def cpu(lasttime):
        global name, dashboard
        logger = dashboard.getPlugin(name, 'logger')
        config = dashboard.getPlugin(name, 'config')
        database = dashboard.getPlugin(name, 'database')

        if lasttime == 0:
            lasttime = int(time.time()) - config.get('data_cnt', 20) * 5
        
        select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('cpu'), lasttime)
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
        logger.debug("CPU new data: {} records.".format(len(rv)))
        if len(rv) > 0:
            return rv[-1]['timestamp'], rv
        else:
            return int(time.time()), rv

    @staticmethod
    def memory(lasttime):
        global name, dashboard
        logger = dashboard.getPlugin(name, 'logger')
        config = dashboard.getPlugin(name, 'config')
        database = dashboard.getPlugin(name, 'database')

        if lasttime == 0:
            lasttime = int(time.time()) - - config.get('data_cnt', 20) * 5

        select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('memory'), lasttime)
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
        logger.debug("Memory new data: {} records.".format(len(rv)))
        if len(rv) > 0:
            return rv[-1]['timestamp'], rv
        else:
            return int(time.time()), rv

    @staticmethod
    def disk(lasttime):
        global name, dashboard
        logger = dashboard.getPlugin(name, 'logger')
        config = dashboard.getPlugin(name, 'config')
        database = dashboard.getPlugin(name, 'database')

        if lasttime == 0:
            lasttime = int(time.time()) - config.get('data_cnt', 20) * 5

        select_sql = "select * from {} where TIMESTAMP > {};".format(config.get('table_name').get('disk'), lasttime)
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
        logger.debug("Disk new data: {} records.".format(len(rv)))
        if len(rv) > 0:
            return rv[-1]['timestamp'], rv
        else:
            return int(time.time()), rv