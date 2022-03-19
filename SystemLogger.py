from datetime import datetime
import psutil
import threading
from time import sleep

from SQLAdapter import SQLAdapter


class SystemLogger(threading.Thread):
    def __init__(self, sql: SQLAdapter, interval: float, printing=False, saving=True):
        super(SystemLogger, self).__init__()
        self._stop = threading.Event()
        self.sql = sql
        self.interval = interval
        self.printing = printing
        self.saving = saving
        self.timestamp = ""
        self.cpu_percent = "0.0"
        self.mem_percent = "0.0"
        self.mem_total = 0.0

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def toggle_printing(self):
        self.printing = not self.printing

    def toggle_saving(self):
        self.saving = not self.saving

    def run(self) -> None:
        self.tick()
        sleep(1)
        ticks = 0
        while True:
            if self.stopped():
                return
            self.tick()
            if self.printing:
                self.display()
            if self.saving:
                self.save()
            ticks += 1
            sleep(self.interval)

    def tick(self) -> None:
        self.timestamp = datetime.now()
        self.cpu_percent = "%.1f" % psutil.cpu_percent()
        self.mem_percent = "%.1f" % psutil.virtual_memory().percent
        self.mem_total = psutil.virtual_memory().total

    def display(self) -> None:
        # Print to Console
        print(str(datetime.now()))
        print("CPU Workload: " + self.cpu_percent + "%")
        print("Memory Usage: " + self.mem_percent + "% of " + "%.0f" % (self.mem_total / pow(10, 6)) + "MB\n")

    def save(self) -> None:
        # Write cpu_percent & mem_percent to DB
        self.sql.insert("events", ['cpu_usage', 'mem_usage'], [self.cpu_percent, self.mem_percent])
