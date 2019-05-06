# -*- coding: utf-8 -*-

import logging

from core import fileSystem, fileSystemInit
from flask import Flask

conf = {}

class App:
    mod_list = []
    app = None
    conf = None
    def __init__(self, conf):
        self.app = Flask(__name__)
        self.conf = conf
        
        fileSystemInit('fileSystem', logging, conf['fileSystem'])
        self.mod_list.append(fileSystem)
        self.app.register_blueprint(fileSystem)

    def run(self):
        self.app.run(debug=self.conf.get('debug', False), port=self.conf.get('port', 8080))