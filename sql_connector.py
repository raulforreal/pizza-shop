import sqlite3 as sqlite
from contextlib import contextmanager


class SQLiteConnector:              # helper class used to self manage
    def __init__(
        self,
        database,
    ):
        self._database = database

    @contextmanager
    def _get_connection(self):
        # Context manager helps manage and automatically close database connection
        # once connection goes out of context of with clause
        connection = sqlite.connect(self._database)
        try:
            yield connection
        finally:
            connection.close()

    def execute_insert_query(self, query, parms=()):
        # Helper function to insert or manipulate database objects
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, parms)
            result = cursor.fetchone()
            cursor.close()
            connection.commit()
            return result

    def execute_fetch_query(self, query, parms=()):
        # Helper functon to fetch data from database
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, parms)
            records = cursor.fetchall()
            cursor.close()
            return records
