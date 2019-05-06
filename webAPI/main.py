# -*- coding: utf-8 -*-

from app import App

if __name__ == '__main__':
    conf = {
        'debug': True,
        'port': 8081,
        'fileSystem': {}
    }

    myApp = App(conf)
    myApp.run()
