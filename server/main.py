# -*- coding: utf-8 -*-
from submodule import dataWatcherRun, fileSystemRun
from multiprocessing import Process
from database import SQLiteBase
from dashboard import Logger, Config, Dashboard

def main(conf):
    ## 创建日志工厂
    logFactory = Logger(conf['log'])
    ## 创建默认数据库插件
    db = SQLiteBase(conf['database']['path'], logger=logFactory.getLogger('database') ,init_script_file=conf['database'].get('init_script_file'))
    ## 创建默认配置文件插件
    config = conf['config']

    dashboard_init = {
        "namespace": {
            "dataWatcher": {
                "logger": logFactory.getLogger("dataWatcher"),
                "database": db,
                "config": config.get("dataWatcher")
            },
            "fileSystem": {
                "logger": logFactory.getLogger("fileSystem"),
                "database": None,
                "config": config.get("fileSystem")
            }
        }
    }
    dashboard = Dashboard(dashboard_init)
    # dataWatcher进程
    proc1 = Process(target=dataWatcherRun, args=('dataWatcher', dashboard,))
    proc1.daemon = True
    proc1.start()
    # fileSystem进程
    proc2 = Process(target=fileSystemRun, args=('fileSystem', dashboard,))
    proc2.daemon = True
    proc2.start()
    proc1.join()
    proc2.join()

if __name__ == "__main__":
    conf = {
        'log': {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s:%(lineno)d]: %(message)s",
                    "datefmt": "%d-%M-%Y %H:%M:%S"
                }
            },
            "handlers": {
                "database": {
                    "class":"logging.FileHandler",
                    "level":"DEBUG",
                    "formatter":"default",
                    "filename": "../log/backendAPI/database.log"
                },
                "dataWatcher": {
                    "class":"logging.FileHandler",
                    "level":"DEBUG",
                    "formatter":"default",
                    "filename": "../log/backendAPI/dataWatcher.log"
                },
                "fileSystem": {
                    "class":"logging.FileHandler",
                    "level":"DEBUG",
                    "formatter":"default",
                    "filename": "../log/backendAPI/fileSystem.log"
                },
                "defaultHandler": {
                    "class":"logging.FileHandler",
                    "level":"DEBUG",
                    "formatter":"default",
                    "filename": "../log/backendAPI/main.log"
                }
            },
            "loggers": {
                "database": {
                    "handlers": ["database"],
                    "level": "DEBUG",
                    "propogate": "no"
                },
                "dataWatcher": {
                    "handlers": ["dataWatcher"],
                    "level": "DEBUG",
                    "propogate": "no"
                },
                "fileSystem": {
                    "handlers": ["fileSystem"],
                    "level": "DEBUG",
                    "propogate": "no"
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": ['defaultHandler'],
                "propogate": "no"
            }
        },
        'config': {
            "dataWatcher": {
                "table_name": {
                    "cpu": "cpuTable",
                    "memory": "memoryTable",
                    "disk": "diskTable"
                }
            },
            "fileSystem": {

            }
        },
        'database': {
            "path": "../database/smws.db",
            "init_script_file": "../conf/init_script.sql"
        }
    }

    main(conf)