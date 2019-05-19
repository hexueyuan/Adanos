# -*- coding: utf-8 -*-

import threading
from multiprocessing import Process, Event

import time
import psutil

class WorkerBase(object):
    def __init__(self, mode="threading"):
        if mode not in ['threading', 'proccessing']:
            raise ValueError("Bad mode.")
        self._work_mode = mode

    def work(self):
        if self._work_mode == "threading":
            self._running = True
            self._worker = threading.Thread(target=self.run, args=(self._work_mode, self._running,))
            self._worker.setDaemon(True)
        else:
            self._running = Event()
            self._worker = Process(target=self.run, args=(self._work_mode, self._running,))
            self._worker.daemon = True
            self._running.set()
        self._worker.start()

    def exit(self, force=False):
        if self._work_mode == "threading":
            self._running = False
        else:
            self._running.clear()
        if self.isOK():
            self._worker.join()
        return True

    def beforeWork(self):
        pass

    def afterWork(self):
        pass

    def run(self, mode, status):
        self.beforeWork()
        if mode == "threading":
            while self._running:
                self.main()
        else:
            while status.is_set():
                self.main()
        self.afterWork()

    def main(self):
        print time.strftime("%H:%M:%S", time.localtime(int(time.time()))),  "I'm working..."
        time.sleep(1)

    def isOK(self):
        if self._work_mode == "threading":
            return self._worker.isAlive()
        else:
            return self._worker.is_alive()

class CPUWorker(WorkerBase):
    """采集cpu数据"""
    def __init__(self, dashboard, mode="threading"):
        super(CPUWorker, self).__init__(mode)
        self._name = 'cpuWorker'
        self._dashboard = dashboard
        logger = dashboard.getLogger(self._name)
        logger.info("cpuWorker is created.")
        config = dashboard.getConfig(self._name)
        self._collector_time_interval = config['time_interval']

    def beforeWork(self):
        """
        在进行统计之前先采集一下数据，否则由于psutil基准时为0会导致第一次采集数据为0
        """
        psutil.cpu_count(logical=True)
        psutil.cpu_count(logical=False)
        psutil.cpu_percent()
        psutil.cpu_times_percent()
        psutil.cpu_freq().current
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is working now.".format(self._name))
    
    def afterWork(self):
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is stop working.".format(self._name))

    def main(self):
        # 逻辑核
        logical_cnt = psutil.cpu_count(logical=True)
        # 物理核
        physics_cnt = psutil.cpu_count(logical=False)
        # CPU实时使用率
        cpu_current_use_rate = psutil.cpu_percent()
        # CPU类型时百分比统计
        typeT = psutil.cpu_times_percent()
        cpu_user_time = typeT.user      # 用户时
        cpu_system_time = typeT.system  # 系统时
        cpu_idle_time = typeT.idle      # 空闲时
        # CPU频率统计
        cpu_current_freq = psutil.cpu_freq().current

        # 写入数据
        database = self._dashboard.getDatabase(self._name)
        config = self._dashboard.getConfig(self._name)
        logger = self._dashboard.getLogger(self._name)
        record = {
            'TIMESTAMP': int(time.time()),
            'LOGICALCNT': logical_cnt,
            'PHYSICSCNT': physics_cnt,
            'USERATE': cpu_current_use_rate,
            'USERTIME': cpu_user_time,
            'SYSTEMTIME': cpu_system_time,
            'IDLETIME': cpu_idle_time,
            'FREQUENCY': cpu_current_freq
        }
        if database.insert(config.get('table_name'), record):
            logger.debug('insert success.')
        else:
            logger.warn('insert fail.')
        time.sleep(self._collector_time_interval)

class MemoryWorker(WorkerBase):
    def __init__(self, dashboard, mode='threading'):
        super(MemoryWorker, self).__init__(mode=mode)
        self._name = 'memoryWorker'
        self._dashboard = dashboard
        logger = dashboard.getLogger(self._name)
        logger.info("memoryWorker is created.")
        config = dashboard.getConfig(self._name)
        self._collector_time_interval = config['time_interval']

    def beforeWork(self):
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is start working.".format(self._name))

    def afterWork(self):
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is stop working.".format(self._name))

    def main(self):
        mem = psutil.virtual_memory()
        # 总内存大小 Byte
        mem_total = mem.total
        # 使用率 %
        mem_use_rate = mem.percent

        swap = psutil.swap_memory()
        # 交换区大小 Byte
        swap_total = swap.total
        # 使用率 %
        swap_use_rate = swap.percent
        # 换入字节数 Byte
        swap_sin = swap.sin 
        # 换出字节数 Byte
        swap_sout = swap.sout

        record = {
            'TIMESTAMP': int(time.time()),
            'MEMORYTOTAL': mem_total,
            'MEMORYUSERATE': mem_use_rate,
            'SWAPTOTAL': swap_total,
            'SWAPUSERATE': swap_use_rate,
            'SWAPSIN': swap_sin,
            'SWAPSOUT': swap_sout
        }
        database = self._dashboard.getDatabase(self._name)
        config = self._dashboard.getConfig(self._name)
        logger = self._dashboard.getLogger(self._name)
        if database.insert(config.get('table_name'), record):
            logger.debug('insert success.')
        else:
            logger.warn('insert fail.')
        time.sleep(self._collector_time_interval)

class DiskWorker(WorkerBase):
    def __init__(self, dashboard, mode='threading'):
        super(DiskWorker, self).__init__(mode=mode)
        self._name = 'diskWorker'
        self._dashboard = dashboard
        logger = dashboard.getLogger(self._name)
        logger.info("diskWorker is created.")
        config = dashboard.getConfig(self._name)
        self._collector_time_interval = config['time_interval']

    def beforeWork(self):
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is start working.".format(self._name))

    def afterWork(self):
        logger = self._dashboard.getLogger(self._name)
        logger.info("{} is stop working.".format(self._name))

    def main(self):
        t = int(time.time())
        database = self._dashboard.getDatabase(self._name)
        config = self._dashboard.getConfig(self._name)
        logger = self._dashboard.getLogger(self._name)
        hard_disks = psutil.disk_partitions(all=False)
        for disk in hard_disks:
            disk_device_name = disk.device
            disk_mount_point = disk.mountpoint
            disk_fstype = disk.fstype

            point_info = psutil.disk_usage(disk_mount_point)
            disk_total = point_info.total
            disk_userate = point_info.percent

            record = {
                'TIMESTAMP': t,
                'DEVICENAME': disk_device_name,
                'MOUNTPOINT': disk_mount_point,
                'FSTYPE': disk_fstype,
                'TOTAL': disk_total,
                'USERATE': disk_userate
            }
            if database.insert(config.get('table_name'), record):
                logger.debug('insert success.')
            else:
                logger.warn('insert fail.')
        time.sleep(self._collector_time_interval)


if __name__ == "__main__":
    worker = WorkerBase(mode="proccessing")
    worker.work()
    def exitHandler(signum, frame):
        worker.exit()
        print "Worker is stop working now!"
        exit()
    import signal
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)
    signal.signal(signal.SIGTSTP, exitHandler)

    cnt = 10
    while cnt != 0:
        time.sleep(1)
        if worker.isOK():
            print "worker is working hard!"
        else:
            print "worker is not work now!"
        if cnt == 5:
            if worker.exit():
                print "Make work stop."
        cnt = cnt - 1