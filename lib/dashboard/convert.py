def convertLoggerConf( conf):
    """
    {
        "formatter": {
            "datefmt": "xxx",
            "format": "xxx"
        },
        "modules": {
            "module1": {
                "class": "xxx",
                "level": "xxx"
                xxx
            }
        }
    }
    """
    rv = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": conf.get("formatter")
        },
        "handlers": {
            "defaultHandler": {
                "class":"logging.FileHandler",
                "level":"NOTSET",
                "formatter":"default",
                "filename": "../log/collector/default.log"
            },
            "consoleHandler": {
                "formatter": "default", 
                "class": "logging.StreamHandler", 
                "level": "NOTSET"
            }
        },
        "loggers": {},
        "root": {
            "level": "DEBUG",
            "handlers": ["defaultHandler"],
            "propogate": "no"
        }
    }
    for name, option in conf['modules'].items():
        # handlers
        rv["handlers"][name + "Handler"] = {
            "class": option["class"],
            "level": "NOTSET",
            "formatter": "default"
        }
        if option["class"] == "logging.FileHandler":
            rv["handlers"][name + "Handler"]["filename"] = option['filename']

        # common
        rv["loggers"][name] = {
            "level": option["level"],
            "handlers": [name + "Handler"],
            "propogate": "no"
        }
        # debug
        rv["loggers"][name + "Debug"] = {
            "level": "DEBUG",
            "handlers": [name + "Handler", "consoleHandler"],
            "propogate": "no"
        }
        
    return rv

def convertDashboardConf(conf):
    rv = {
        "config": {},
        "logger": {
            "formatter": {
                "format": "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s:%(lineno)d]: %(message)s",
                "datefmt": "%d-%M-%Y %H:%M:%S"
            },
            "modules": {}
        }
    }

    for name, option in conf.items():
        rv["config"][name] = option.get("config", {})
        rv["logger"]["modules"][name] = option["logger"]

    return rv