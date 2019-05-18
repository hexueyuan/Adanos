# -*- coding: utf-8 -*-

from . import worker

def factory(name, dashboard, mode="threading"):
    if name == "cpuWorker":
        return worker.CPUWorker(dashboard, mode)
    elif name == "memoryWorker":
        return worker.MemoryWorker(dashboard, mode)
    elif name == "diskWorker":
        return worker.DiskWorker(dashboard, mode)
    else:
        return None