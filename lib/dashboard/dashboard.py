# -*- coding: utf-8 -*-

from config import Config
from datapool import Datapool
from logger import Logger

class Dashboard:
    _namespace = {
        'default': {
            'config'  : None,
            'database': None,
            'logger'  : None
        }
    }

    def __init__(self, conf=None):
        """
        replace default namespace module:
            {
                "config": Object,
                "database": Object,
                "logger": Object
            }
        It is same as:
            {
                "namespace": {
                    "default": {
                        "config": Object,
                        "database": Object,
                        "logger": Object
                    }
                }
            }
        If you define deafult namespace in root level and 'namespace' path, use 'namespace' path as current.
        
        And you can define different namespace module as followd:
            {
                "namespace": {
                    "application1": {
                        "config": Object,
                        "database": Object,
                        "logger": Object
                    },
                    "application2": {
                        "config": Object,
                        "database": Object,
                        "logger": Object
                    }
                },
                "config": Object,
                "database": Object,
                "logger": Object
            }
        """
        self._default_logger_factory = Logger()
        self._default_logger = self._default_logger_factory.getLogger('root')
        self._default_config = Config({})
        self._default_datapool = Datapool()

        if conf is None:
            self._namespace['default']['config'] = self._default_config
            self._namespace['default']['database'] = self._default_datapool
            self._namespace['default']['logger'] = self._default_logger
        else:
            self._namespace['default']['config'] = conf.get('config', self._default_config)
            self._namespace['default']['database'] = conf.get('database', self._default_datapool)
            self._namespace['default']['logger'] = conf.get('logger', self._default_logger)
            for namespace, conf in conf.get('namespace', {}).items():
                if not self._namespace.has_key(namespace):
                    self._namespace[namespace] = {}
                self._namespace[namespace].update(conf)
        
        self._default_logger.info("Dashboard is created.")

    def setPlugin(self, namespace, pluginName, plugin):
        if not self._namespace.has_key(namespace):
            self._namespace[namespace] = {}

        if plugin is not None:
            self._namespace[namespace][pluginName] = plugin

    def getPlugin(self, namespace, pluginName):
        if not self._namespace.has_key(namespace):
            return self.getPlugin('default', pluginName)

        return self._namespace[namespace].get(pluginName)

    def getLogger(self, namespace):
        return self.getPlugin(namespace, 'logger')

    def getConfig(self, namespace):
        return self.getPlugin(namespace, 'config')

    def getDatabase(self, namespace):
        return self.getPlugin(namespace, 'database')

if __name__ == "__main__":
    """To create custom dashboard"""
    from database import SQLiteBase
    conf = {
        "log": {
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s:%(lineno)d]: %(message)s",
                    "datefmt": "%d-%M-%Y %H:%M:%S"
                }
            },
            "handlers": {
                "consoleHandler": {
                    "class":"logging.StreamHandler",
                    "level":"NOTSET",
                    "formatter":"default",
                    "stream":"ext://sys.stdout"
                },
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "level": "NOTSET",
                    "formatter": "default",
                    "filename": "testHandler2.log"
                }
            },
            "loggers": {
                "testLogger1": {
                    "handlers": ["consoleHandler"],
                    "level": "INFO"
                },
                "testLogger2": {
                    "handlers": ["fileHandler"],
                    "level": "DEBUG"
                }
            }
        },
        "conf": {
            "globalname": "test",
            "author": "xueyuan",
            "date": "2019-05-13"
        },
        "database": {
            "path": "./test.db"
        }
    }

    loggerFactory = Logger(conf['log'])
    database = SQLiteBase(conf['database']['path'])
    config = Config(conf['conf'])

    global_conf = {
        'namespace': {
            'module1': {
                'config': config,
                'database': database,
                'logger': loggerFactory.getLogger('testLogger1')
            },
            'module2': {
                'config': config,
                'database': database,
                'logger': loggerFactory.getLogger('testLogger2')
            }
        }
    }

    dashboard = Dashboard(global_conf)
