from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from datetime import datetime
import time


class Monitor:
    def __init__(self, refresh_rate=3):
        super(Monitor, self).__init__()

        self.refresh_rate = refresh_rate
        self.get_system()
        self.in_use = list()

    def get_system(self):
        #self.in_use.append("sys")
        #if "cpu" not in self.in_use and "sys" == self.in_use[0]:
        time.sleep(self.refresh_rate)
        timestamp = boot_time()
        boot_date_time = datetime.fromtimestamp(timestamp)
        system = {
            "boot_date_time": str(boot_date_time)
        }
        return system

    def get_cpu(self):
        return cpu_percent(self.refresh_rate)

    def get_mem(self):
        return virtual_memory().percent

    def get_hdd(self):
        total, used, free, percent = disk_usage("/")
        dictionary = str({"total": total, "used": used, "free": free, "percent": percent})

        return dictionary

    def clear(self):
        self.in_use = list()
