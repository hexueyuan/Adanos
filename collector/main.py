# -*- coding:utf8 -*-

from collector import Collector
from database import SQLiteBase
from dashboard import Logger, Config, Dashboard

import json
import sys
import os
import signal

def main(conf):
    ## 创建日志工厂
    logFactory = Logger(conf['log'])
    ## 创建默认数据库插件
    db = SQLiteBase(conf['database']['path'], logger=logFactory.getLogger('database') ,init_script_file=conf['database'].get('init_script_file'))
    ## 创建默认配置文件插件
    config = conf['config']

    ## dashboard配置
    dashboard_init = {
        'namespace': {
            'collector': {
                'config': config.get('collector'),
                'logger': logFactory.getLogger('collector'),
                'database': None
            },
            'cpuWorker': {
                'config': config.get('cpuWorker'),
                'logger': logFactory.getLogger('cpuWorker'),
                'database': db
            },
            'memoryWorker': {
                'config': config.get('memoryWorker'),
                'logger': logFactory.getLogger('memoryWorker'),
                'database': db
            },
            'diskWorker': {
                'config': config.get('diskWorker'),
                'logger': logFactory.getLogger('diskWorker'),
                'database': db
            }
        }
    }
    ## 创建dashboard
    dashboard = Dashboard(dashboard_init)

    ## 创建collector
    collector = Collector(dashboard)

    ## 注册捕获信号
    def exitHandler(signum, frame):
        collector.exit()
        logFactory.getLogger('root').info('collector exit.')
        exit()
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)
    signal.signal(signal.SIGTSTP, exitHandler)

    logFactory.getLogger('root').info('collector start.')
    ## 启动collector
    collector.work()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "python main <conf_path>"
        exit()
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            conf  = json.load(f)
        main(conf)
    else:
        print "No such file: {}".format(sys.argv[1])