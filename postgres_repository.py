import os

import psycopg
from psycopg.rows import dict_row

from repository import TaskRepository


class PostgresTaskRepository(TaskRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")

    def get_connection(self):
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row
        )

    def get_all(self):
        with self.get_connection() as connection:
            return connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                ORDER BY id
                """
            ).fetchall()

    def get_by_id(self, task_id: int):
        with self.get_connection() as connection:
            return connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            ).fetchone()

    def create(self, title: str):
        with self.get_connection() as connection:
            return connection.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, FALSE)
                RETURNING id, title, done
                """,
                (title,)
            ).fetchone()

    def update(self, task_id: int, title: str):
        with self.get_connection() as connection:
            return connection.execute(
                """
                UPDATE tasks
                SET title = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (title, task_id)
            ).fetchone()

    def delete(self, task_id: int):
        with self.get_connection() as connection:
            result = connection.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id
                """,
                (task_id,)
            ).fetchone()

            return result is not None