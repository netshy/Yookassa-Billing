import logging

import backoff
import psycopg2
from loguru import logger
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor


class PostgresHelper:
    def __init__(self, pg_cursor):
        self._cursor = pg_cursor

    @backoff.on_exception(
        backoff.expo,
        psycopg2.OperationalError,
        logger=logger,
        backoff_log_level=logging.ERROR,
    )
    def execute_query(self, query: str) -> list:
        self._cursor.execute(query)
        all_data = self._cursor.fetchall()
        return all_data

    def get_template_html(self, template_id: str):
        query = f"""
            SELECT template_data, subject
            FROM notification_template
            WHERE id='{template_id}'
        """

        result = self.execute_query(query)
        return result

    @property
    def cursor(self):
        return self._cursor


class PostgresConnector:
    def __init__(self, dsl: dict) -> None:
        self.dsl = dsl
        self.cursor = self._cursor

    @backoff.on_exception(
        backoff.expo,
        psycopg2.OperationalError,
        logger=logger,
        backoff_log_level=logging.ERROR,
    )
    def _init_pg_connection(self) -> connection:
        conn = psycopg2.connect(**self.dsl, cursor_factory=RealDictCursor)
        return conn

    @property
    def _cursor(self) -> cursor:
        conn = self._init_pg_connection()
        return conn.cursor()
