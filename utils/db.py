import os
from typing import Optional

from psycopg_pool import AsyncConnectionPool


def get_conn_str():
    return f"""
    dbname={os.getenv('POSTGRES_DB') or "vectordb"}
    user={os.getenv('POSTGRES_USER') or "user"}
    password={os.getenv('POSTGRES_PASSWORD') or "password"}
    host={os.getenv('POSTGRES_HOST') or "localhost"}
    port={os.getenv('POSTGRES_PORT') or "5432"}
    """


class PostgresDatabase:
    def __init__(self):
        self.db_pool = Optional[None]
        self.conn = Optional[None]

    async def create_connection_pool(self):
        try:
            self.conn = AsyncConnectionPool(conninfo=get_conn_str())
            if self.conn:
                self.db_pool = self.conn
        except ConnectionError as error:
            print(f"DB connection error {error}")

    async def close_connection_pool(self):
        try:
            if self.db_pool:
                await self.conn.close()
        except Exception as error:
            print(f"Error in closing db connection {error}")


postgres_db = PostgresDatabase()
