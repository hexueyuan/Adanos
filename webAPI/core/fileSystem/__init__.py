# -*- coding: utf-8 -*-
import route

def init(name, logger, config):
    route.module_name   = name
    route.module_logger = logger
    route.module_config = config

from route import mod