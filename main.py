import sys
import threading

from EventReader import EventReader
from SQLAdapter import SQLAdapter
from SystemLogger import SystemLogger

from env import log_interval


class App:
    def __init__(self):
        self.sql = SQLAdapter()
        self.logger = SystemLogger(self.sql, log_interval)
        self.reader = EventReader(self.sql)

    def main_loop(self) -> None:
        # Define available commands
        commands = {
            0: self.quit,
            1: self.start_logger,
            2: self.stop_logger,
            3: self.logger.toggle_printing,
            4: self.logger.toggle_saving,
            5: self.reader.display,
            6: self.reader.csv_dump,
            7: self.test_connection
        }
        print("1 - Start logger")
        print("2 - Stop logger")
        print("3 - Toggle logger printing (current setting: %s)" % self.logger.printing)
        print("4 - Toggle logger saving to database (current setting: %s)" % self.logger.saving)
        print("5 - Display database contents")
        print("6 - Dump database contents as CSV")
        print("7 - Test database connection")
        print("0 - Quit")
        try:
            choice = int(input("Enter command: "))
            commands.get(choice)()
        except (TypeError, ValueError, RuntimeError) as e:
            print("Invalid command: " + str(e))
        self.main_loop()

    def quit(self):
        self.stop_logger()
        sys.exit()

    def start_logger(self) -> None:
        if self.logger is None or self.logger.stopped():
            self.logger = SystemLogger(self.sql, log_interval)
        self.logger.start()

    def stop_logger(self) -> None:
        thread = threading.Thread(target=self.logger.stop)
        thread.start()
        thread.join()

    def test_connection(self) -> None:
        print("Database connection " + ("established." if hasattr(self.sql, "connection")
                                        and self.sql.connection.is_connected() else "failed."))


if __name__ == '__main__':
    app = App()
    app.main_loop()
