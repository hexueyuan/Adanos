# -*- coding: utf-8 -*-
from submodule import create_app, setDashboard, socketio
from dashboard import Logger, Dashboard, convertDashboardConf, convertLoggerConf
from database import SQLiteBase

import json
import sys
import os

def init_dashboard(db, mod_list, loggerFactory, config, datapool, debug=False):
    for mod in mod_list:
        if debug:
            db.setPlugin(mod, 'logger', loggerFactory.getLogger(mod + 'Debug'))
        else:
            db.setPlugin(mod, 'logger', loggerFactory.getLogger(mod))
        db.setPlugin(mod, 'config', config.get(mod, {}))
        db.setPlugin(mod, 'database', datapool)

def create_dashboard(conf):
    dashboardConf = convertDashboardConf(conf)
    #print json.dumps(dashboardConf, indent=2)
    # --> 创建默认配置文件插件
    config = dashboardConf['config']
    mainConf = config.get('main', {})

    # 创建dashboard
    # --> 创建日志工厂
    loggerConf = convertLoggerConf(dashboardConf['logger'])
    #print json.dumps(loggerConf, indent=2)
    logFactory = Logger(loggerConf)
    
    # --> 创建默认数据库插件
    dbConf = config.get('database')
    if mainConf.get('debug'):
        db = SQLiteBase(dbConf['path'], logger=logFactory.getLogger('databaseDebug') ,init_script_file=dbConf.get('init_script_file'))
    else:
        db = SQLiteBase(dbConf['path'], logger=logFactory.getLogger('database') ,init_script_file=dbConf.get('init_script_file'))
    dashboard = Dashboard()

    init_dashboard(dashboard, ['main', 'dataWatcher', 'fileMonitor'], logFactory, config, db, debug=mainConf.get('debug', False))

    return dashboard

def main(conf):
    dashboard = create_dashboard(conf)
    setDashboard(dashboard)

    mainConf = dashboard.getPlugin('main', 'config')
    logger = dashboard.getPlugin('main', 'logger')
    logger.info("set dashboard.")

    # 创建app
    app = create_app()

    logger.info("ready to run app.")
    socketio.run(app, host=mainConf.get('host'), port=mainConf.get('port'), debug=mainConf.get('debug'))

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