"""SQLite DB manager with thread-safe operations."""
import sqlite3
import threading
from pathlib import Path
from typing import List, Optional

from bmi_calculator.database.models import User, BMIRecord


class DBManager:
    """Manage SQLite connection and CRUD operations."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(Path(__file__).parent.parent / "bmi_data.db")
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self.create_tables()

    def create_tables(self):
        with self._lock, self._conn:
            cur = self._conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    weight_kg REAL NOT NULL,
                    height_m REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

    # User operations
    def add_user(self, username: str, age: int, gender: str) -> User:
        with self._lock, self._conn:
            cur = self._conn.cursor()
            cur.execute(
                "INSERT INTO users (username, age, gender) VALUES (?, ?, ?)",
                (username, age, gender),
            )
            user_id = cur.lastrowid
            return User(id=user_id, username=username, age=age, gender=gender)

    def get_user_by_username(self, username: str) -> Optional[User]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return User(id=row["id"], username=row["username"], age=row["age"], gender=row["gender"])
        return None

    def list_users(self) -> List[User]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY created_at DESC")
        return [User(id=r["id"], username=r["username"], age=r["age"], gender=r["gender"]) for r in cur.fetchall()]

    # BMI record operations
    def add_bmi_record(self, user_id: int, weight_kg: float, height_m: float, bmi: float, category: str) -> BMIRecord:
        with self._lock, self._conn:
            cur = self._conn.cursor()
            cur.execute(
                """
                INSERT INTO bmi_records (user_id, weight_kg, height_m, bmi, category)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, weight_kg, height_m, bmi, category),
            )
            rec_id = cur.lastrowid
            cur.execute("SELECT * FROM bmi_records WHERE id = ?", (rec_id,))
            row = cur.fetchone()
            return BMIRecord(id=row["id"], user_id=row["user_id"], weight_kg=row["weight_kg"], height_m=row["height_m"], bmi=row["bmi"], category=row["category"], recorded_at=row["recorded_at"])  # type: ignore

    def get_records_for_user(self, user_id: int) -> List[BMIRecord]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM bmi_records WHERE user_id = ? ORDER BY recorded_at ASC", (user_id,))
        rows = cur.fetchall()
        return [BMIRecord(id=r["id"], user_id=r["user_id"], weight_kg=r["weight_kg"], height_m=r["height_m"], bmi=r["bmi"], category=r["category"], recorded_at=r["recorded_at"]) for r in rows]

    def delete_record(self, record_id: int):
        with self._lock, self._conn:
            cur = self._conn.cursor()
            cur.execute("DELETE FROM bmi_records WHERE id = ?", (record_id,))

    def stats_for_user(self, user_id: int) -> dict:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt, MIN(bmi) as min_bmi, MAX(bmi) as max_bmi, AVG(bmi) as avg_bmi FROM bmi_records WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return {"count": row["cnt"], "min": row["min_bmi"], "max": row["max_bmi"], "avg": row["avg_bmi"]}
