import sqlite3 as sqlite
from contextlib import contextmanager
from typing import Dict, Optional


class SQLiteConnector:
    def __init__(
        self,
        database: str,
    ):
        self._database = database

    @contextmanager
    def _get_connection(self):
        connection = sqlite.connect(self._database)
        try:
            yield connection
        finally:
            connection.close()

    def execute_insert_query(self, query: str, parms: Optional[Dict[str, str]] = {}):
        with self._get_connection() as connection:
            currsor = connection.cursor()
            currsor.execute(query, parms)
            currsor.close()
            connection.commit()

    def execute_fetch_query(self, query: str, parms: Optional[Dict[str, str]] = {}):
        with self._get_connection() as connection:
            currsor = connection.cursor()
            currsor.execute(query, parms)
            records = currsor.fetchall()
            currsor.close()
            return records
