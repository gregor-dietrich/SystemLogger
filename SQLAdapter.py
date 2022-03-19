import mysql.connector

from env import db


class SQLAdapter:
    def __init__(self):
        try:
            # Connecting to database
            self.connection = mysql.connector.connect(
                user=db["username"],
                password=db["password"],
                host=db["hostname"],
                database=db["database"])
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            else:
                self.cursor = None
            self.db_setup()
        except mysql.connector.Error as e:
            print("Database connection error: ", e)

    def __del__(self):
        try:
            if hasattr(self, "connection"):
                if self.connection.is_connected():
                    # Closing database connection
                    if hasattr(self, "cursor"):
                        try:
                            self.cursor.close()
                        except ReferenceError as ignored:
                            pass
                    self.connection.close()
        except mysql.connector.Error as e:
            print("Database connection error: ", e)

    def db_setup(self):
        # Create table in database if it does not exist
        self.commit("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";")
        self.commit("START TRANSACTION")
        self.commit("SET time_zone = \"+00:00\";")
        self.commit(f"USE `{db['database']}`;")
        query_string = "CREATE TABLE IF NOT EXISTS `events` ("
        query_string += "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        query_string += "  `cpu_usage` float NOT NULL,"
        query_string += "  `mem_usage` float NOT NULL,"
        query_string += "  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),"
        query_string += "  PRIMARY KEY (`id`)"
        query_string += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        self.commit(query_string)
        self.commit("COMMIT;")

    def commit(self, query: str) -> bool:
        try:
            if hasattr(self, "connection") and hasattr(self, "cursor"):
                self.cursor.execute(query)
                self.connection.commit()
                return True
            return False
        except mysql.connector.Error as e:
            print("Database connection error: ", e)
            self.__del__()
            return False

    def insert(self, table: str, columns: [str], values: [str]) -> bool:
        query_string = f"INSERT INTO {table} "
        if columns is not None and len(columns) > 0:
            query_string += "("
            for column in columns:
                if column != columns[0]:
                    query_string += ", "
                query_string += column
            query_string += ") "
        query_string += "VALUES ("
        for value in values:
            if value != values[0]:
                query_string += ", "
            query_string += "'" + value + "'"
        query_string += ")"
        return self.commit(query_string)

    def delete(self, table: str, condition: str) -> bool:
        query_string = f"DELETE FROM {table} WHERE {condition}"
        return self.commit(query_string)

    def update(self, table: str, condition: str, columns: [str], values: [str]) -> bool:
        query_string = f"UPDATE {table} SET "
        if len(columns) != len(values):
            raise AssertionError("Columns/Values Array Length Mismatch")
        for i in range(len(columns)):
            if i > 0:
                query_string += ", "
            query_string += columns[i] + " = '" + values[i] + "'"
        query_string += f" WHERE {condition}"
        return self.commit(query_string)

    def select_all(self, table: str) -> list:
        return self.select(table, "1")

    def select(self, table: str, condition: str) -> list:
        return self.select_cols(table, ["*"], condition)

    def select_cols(self, table: str, columns: [str], condition: str) -> list:
        try:
            query_string = "SELECT "
            for column in columns:
                if column != columns[0]:
                    query_string += ", "
                query_string += column
            query_string += f" FROM {table}"
            if condition is not None and condition != "":
                query_string += f" WHERE {condition}"
            self.cursor.execute(query_string)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print("Database connection error: ", e)
            return []
