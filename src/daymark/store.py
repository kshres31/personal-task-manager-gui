import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    title: str
    priority: str = "medium"
    done: bool = False
    id: int | None = None


class TaskStore:
    def __init__(self, database: Path) -> None:
        self.database = database

    def initialize(self) -> None:
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.database)) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, priority TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
            connection.commit()

    def add(self, title: str, priority: str) -> int:
        title = title.strip()
        if not title:
            raise ValueError("title is required")
        if priority not in {"low", "medium", "high"}:
            raise ValueError("invalid priority")
        with closing(sqlite3.connect(self.database)) as connection:
            cursor = connection.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
            connection.commit()
            return int(cursor.lastrowid)

    def list(self, search: str = "", show_done: bool = True) -> list[Task]:
        query = "SELECT id, title, priority, done FROM tasks WHERE title LIKE ?"
        params: list[object] = [f"%{search.strip()}%"]
        if not show_done:
            query += " AND done = 0"
        query += " ORDER BY done, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, id DESC"
        with closing(sqlite3.connect(self.database)) as connection:
            rows = connection.execute(query, params).fetchall()
        return [Task(row[1], row[2], bool(row[3]), row[0]) for row in rows]

    def set_done(self, task_id: int, done: bool) -> None:
        self._change("UPDATE tasks SET done = ? WHERE id = ?", (int(done), task_id))

    def delete(self, task_id: int) -> None:
        self._change("DELETE FROM tasks WHERE id = ?", (task_id,))

    def _change(self, query: str, params: tuple[object, ...]) -> None:
        with closing(sqlite3.connect(self.database)) as connection:
            connection.execute(query, params)
            connection.commit()

