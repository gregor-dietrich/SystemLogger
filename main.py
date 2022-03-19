import sys

from EventReader import EventReader
from SQLAdapter import SQLAdapter
from SystemLogger import SystemLogger

from env import log_interval


def test_connection():
    sql = SQLAdapter()
    if hasattr(sql, "connection") and sql.connection.is_connected():
        print("Database connection established.")


def main_loop():
    print("1 - Start logger")
    print("2 - Stop logger")
    print("3 - Toggle logger printing (current setting: %s)" % logger.printing)
    print("4 - Toggle logger saving to database (current setting: %s)" % logger.saving)
    print("5 - Display database contents")
    print("6 - Dump database contents as CSV")
    print("7 - Test database connection")
    print("0 - Quit")
    try:
        choice = int(input("Enter command: "))
        commands.get(choice)()
    except (TypeError, ValueError) as e:
        print("Invalid command: " + str(e))
    main_loop()


if __name__ == '__main__':
    # Start a SystemLogger that ticks every 5 seconds
    logger = SystemLogger(log_interval)
    # Instantiate an EventReader
    reader = EventReader()
    # Define available commands
    commands = {
        0: sys.exit,
        1: logger.start,
        2: logger.stop,
        3: logger.toggle_printing,
        4: logger.toggle_saving,
        5: reader.display,
        6: reader.csv_dump,
        7: test_connection
    }
    main_loop()
