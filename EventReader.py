import csv

from env import db
from SQLAdapter import SQLAdapter


class EventReader:
    def __init__(self):
        self.sql = SQLAdapter()
        self.table = "events"

    def get_events(self) -> list:
        return self.sql.select_all(self.table)

    def display(self) -> None:
        cpu_total = 0.0
        mem_total = 0.0
        for event in self.get_events():
            print("Timestamp: " + str(event[3]))
            print("CPU Workload: %.1f" % event[1] + "%")
            print("Memory Usage: %.1f" % event[2] + "%\n")
            cpu_total += event[1]
            mem_total += event[2]
        if len(self.get_events()) > 0:
            print(30 * "-")
            print("Average CPU Workload: %.1f" % (cpu_total / len(self.get_events())))
            print("Average Memory Usage: %.1f" % (mem_total / len(self.get_events())))
            print(30 * "-")

    def csv_dump(self, output_file="./output.csv", include_column_names=False) -> None:
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            if include_column_names:
                column_names = []
                for col in self.sql.select_cols("INFORMATION_SCHEMA.COLUMNS", ["COLUMN_NAME"],
                                                "TABLE_NAME = '%s' AND TABLE_SCHEMA = '%s'"
                                                % (self.table, db["database"])):
                    column_names.append(col[0])
                writer.writerow(column_names)
            writer.writerows(self.get_events())
