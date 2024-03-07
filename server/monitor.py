from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from datetime import datetime
import time


class Monitor:
    """Prepare client requested monitoring data to be sent."""
    def __init__(self, refresh_rate: int = 3) -> None:
        """Initialise the monitoring.

        Args:
            refresh_rate (int): Rate of refresh in seconds.
        """
        super(Monitor, self).__init__()

        self.refresh_rate = refresh_rate
        self.get_system()
        self.in_use = list()

    def get_system(self) -> dict:
        """Returns the startup timestamp of the server.

        Returns:
            dict: A dictionary of the system informations.
        """

        time.sleep(self.refresh_rate)
        timestamp = boot_time()
        boot_date_time = datetime.fromtimestamp(timestamp)
        system = {
            "boot_date_time": str(boot_date_time)
        }
        return system

    def get_cpu(self) -> str:
        """Returns the current cpu status.

        Returns:
            str: Current cpu datas.
        """

        return cpu_percent(self.refresh_rate)

    def get_mem(self) -> str:
        """Returns the current memory status.

        Returns:
            str: Current memory datas.
        """

        return virtual_memory().percent

    def get_hdd(self) -> str:
        """Returns the hard drive informations.

        Returns:
            str: A dictionnary as a string so it can be send to the client via socket.
        """

        total, used, free, percent = disk_usage("/")
        dictionary = str({"total": total, "used": used, "free": free, "percent": percent})

        return dictionary

    def clear(self) -> None:
        """Clears the monitoring system list."""

        self.in_use = list()
