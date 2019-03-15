# -*- coding:utf8 -*-

import psutil
import sqlite3
import time
import json
import sys

def disk_usage_rate(conf):
    for path in conf["disk_mount_point"]:
        data = psutil.disk_usage(path)
        rate = data.percent
        total = round(data.total / 1024 / 1024 / 1024, 2)
        timestamp = int(time.time())
        sql = "INSERT INTO disk_use_rate(mount_point, use_rate, timestamp, total_space) VALUES(\"{}\", {}, {}, {});".\
            format(path, rate, timestamp, total)
        print sql
        db = sqlite3.connect(conf["database_path"])
        c = db.cursor()
        cursor = c.execute(sql)
        db.commit()
        db.close()

if __name__ == "__main__":
    conf = {}
    if len(sys.argv) < 2:
        print "No configure file in."
        exit()
    with open(sys.argv[1]) as f:
        context = f.read()
        conf = json.loads(context)
    while True:
        disk_usage_rate(conf)
        time.sleep(conf["time_interface_ms"] / 1000)

