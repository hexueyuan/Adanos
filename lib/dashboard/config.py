# -*- coding: utf-8 -*-

class Config:
    _config = {}
    def __init__(self, conf):
        """
        conf is a dict
        """
        if conf is not None:
            self._config = conf
    
    def __getattr__(self, name):
        return self._config.get(name, None)

    def __setattr__(self, name, value):
        self._config[name] = value

if __name__ == "__main__":
    confObj = Config({})

    print confObj.name
    confObj.name = "testConf"
    print confObj.name
