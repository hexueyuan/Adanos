from .workerFactory import factory

import time

class Collector:
    _dashboard = None
    _workers = []
    _check_time_interval = 10
    def __init__(self, dashboard):
        self._name = 'collector'
        logger = dashboard.getLogger(self._name)
        
        self._dashboard = dashboard
        logger.info("collector is created.")

    def dispatch(self):
        config = self._dashboard.getConfig(self._name)
        logger = self._dashboard.getLogger(self._name)
        workers = config.get('workers', [])
        for workerConf in workers:
            worker = factory(workerConf['name'], self._dashboard, workerConf.get('mode', 'threading'))
            logger.info("dispatch {}.".format(workerConf['name']))
            self._workers.append(worker)
        
        for worker in self._workers:
            worker.work()
        logger.info("All worker is running.")

    def work(self):
        logger = self._dashboard.getLogger(self._name)
        self.dispatch()

        self._running = True
        while self._running:
            for index in xrange(len(self._workers)):
                worker = self._workers[index]
                if not worker.isOK():
                    newWorker = factory(worker._name, self._dashboard, worker._work_mode)
                    worker.exit()
                    newWorker.work()
                    self._workers[index] = newWorker
                    logger.info("{} is restart.".format(newWorker._name))
            time.sleep(self._check_time_interval)

    def exit(self, force=False):
        logger = self._dashboard.getLogger(self._name)
        self._running = False
        for worker in self._workers:
            worker.exit()
        logger.info("All workers is stop working.")
        return True