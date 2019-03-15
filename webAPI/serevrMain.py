from flask import Flask
from flask import make_response
from collections import defaultdict
import sqlite3
import json
import sys
import random
import time

app = Flask(__name__)
conf = {}

def readDiskUseRate(start_timestamp, end_timestamp):
    use_rate = defaultdict(list)
    mount_points = conf['disk_mount_point']
    conn = sqlite3.connect('../database/system.db')
    c = conn.cursor()
    for point in mount_points:
        sql = "select mount_point, use_rate, timestamp, total_space from disk_use_rate where mount_point=\"{}\" order by timestamp desc limit {};".format(point, conf["default_search_count"])
        cursor = c.execute(sql)
        for cur in cursor:
            use_rate[point].append({
                "mount_point": cur[0],
                "use_rate": cur[1],
                "timestamp": cur[2],
                "total_space": cur[3]
            })
    return {"mount_points": mount_points, "use_rate": use_rate}

def readDiskUseRateMock(start_timestamp, end_timestamp):
    use_rate = defaultdict(list)
    mock_mount_points = ['/', '/home/xueyuan', '/bin']
    now = int(time.time())
    for point in mock_mount_points:
        for i in range(0, 50):
            use_rate[point].append({
                "mount_point": point,
                "use_rate": round(random.uniform(0, 100), 2),
                "timestamp": now - (10 * i),
                "total_space": 64
            })
    return {"mount_points": mock_mount_points, "use_rate": use_rate}

def readCpuTableMock(start_timestamp, end_timestamp):
    data = []
    now = int(time.time())
    for i in range(0, 100):
        data.append({
            "time": {
                "user": int(random.randint(1000, 10000)),
                "system": int(random.randint(1000, 10000)),
                "io": int(random.randint(1000, 10000)),
                "irq": int(random.randint(1000, 10000)),
                "sirq": int(random.randint(1000, 10000))
            },
            "count": {
                "physics": int(random.randint(2, 10)),
                "logic": int(random.randint(8, 32))
            },
            "use_rate": round(random.uniform(0, 100), 2),
            "timestamp": now - (10 * i)
        })
    return {"use_rate": data}

def readMemoryUseRateMock(start_timestamp, end_timestamp):
    use_rate = []
    now = int(time.time())
    for i in range(0, 50):
        use_rate.append({
            "use_rate": round(random.uniform(0, 100), 2),
            "timestamp": now - (10 * i),
            "total_space": 16
        })
    return {"use_rate": use_rate}
    
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/smwsAPI/disk_use_rate', methods = ['GET'])
def diskUseRate():
    resp = make_response(json.dumps({
        "status": "OK",
        "errMsg": "",
        "data": readDiskUseRateMock(0, 0)
    }))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/smwsAPI/cpu_use_rate', methods = ['GET'])
def cpuUseRate():
    resp = make_response(json.dumps({
        "status": "OK",
        "errMsg": "",
        "data": readCpuTableMock(0, 0)
    }))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/smwsAPI/memory_use_rate', methods = ['GET'])
def memoryUseRate():
    resp = make_response(json.dumps({
        "status": "OK",
        "errMsg": "",
        "data": readMemoryUseRateMock(0, 0)
    }))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No configure in"
        exit(0)
    with open(sys.argv[1]) as f:
        context = f.read()
        conf = json.loads(context)
    app.run(debug=True, port=5001)
