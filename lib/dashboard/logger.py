# -*- coding: utf-8 -*-

import logging
import logging.config
import logging.handlers

class Logger:
    _default_conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s:%(lineno)d]: %(message)s",
                "datefmt": "%d-%M-%Y %H:%M:%S"
            }
        },
        "handlers": {
            "defaultHandler": {
                "class":"logging.StreamHandler",
                "level":"DEBUG",
                "formatter":"default",
                "stream":"ext://sys.stdout"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ['defaultHandler']
        }
    }
    _current_conf = None
    _logger = None
    _register_loggers = ['root']

    def __init__(self, conf=None):
        if conf is not None and not getattr(conf, 'get'):
            raise TypeError("conf has no get method")
        self._current_conf = self._default_conf
        if conf is not None:
            self._current_conf['formatters'].update(conf.get('formatters', {}))
            self._current_conf['handlers'].update(conf.get('handlers', {}))
            self._current_conf['loggers'] = conf.get('loggers', {})

        #set default propagate = 0
        for logger in self._current_conf['loggers'].values():
            logger['propagate'] = 0

        try:
            logging.config.dictConfig(self._current_conf)
        except ValueError:
            self._current_conf = self._default_conf
            logging.config.dictConfig(self._current_conf)
            logging.getLogger("defaultLogger").exception("logger config error.")
        finally:
            self._logger = logging.getLogger("defaultLogger")

        for key in self._current_conf.get('loggers', {}).keys():
            self._register_loggers.append(key)

    def getLogger(self, name):
        if name == "root":
            return self._logger

        if name in self._register_loggers:
            return logging.getLogger(name)
        else:
            raise NameError("No this logger: {}".format(name))

if __name__ == "__main__":
    conf = {
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
    }
    loggerHome = Logger(conf)
    
    #root = loggerHome.getLogger('root')
    #root.debug('this is a debug message')
    #root.info('this is a info message')
    #root.warn('this is a warning message')
    #root.error('this is a error message')
    #root.fatal('this is a fatal message')

    testLogger1 = loggerHome.getLogger('testLogger1')
    testLogger1.debug('this is a debug message')
    testLogger1.info('this is a info message')
    testLogger1.warn('this is a warning message')
    testLogger1.error('this is a error message')
    testLogger1.fatal('this is a fatal message')
    
    testLogger2 = loggerHome.getLogger('testLogger2')
    testLogger2.debug('this is a debug message')
    testLogger2.info('this is a info message')
    testLogger2.warn('this is a warning message')
    testLogger2.error('this is a error message')
    testLogger2.fatal('this is a fatal message')
