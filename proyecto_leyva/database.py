import hashlib
import os
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from typing import Any

DATABASE_URL = os.environ.get("DATABASE_URL", "vida_saludable.db")
DB_PATH = Path(DATABASE_URL.replace("sqlite:///", "")) if DATABASE_URL.startswith("sqlite:///") else Path(DATABASE_URL)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(database_url: str | None = None) -> None:
    global DB_PATH
    if database_url:
        DB_PATH = Path(database_url.replace("sqlite:///", "")) if database_url.startswith("sqlite:///") else Path(database_url)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with closing(_connect()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bmi_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                imc REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        columns = [row["name"] for row in conn.execute("PRAGMA table_info(bmi_history)").fetchall()]
        if "user_id" not in columns:
            conn.execute("ALTER TABLE bmi_history ADD COLUMN user_id INTEGER DEFAULT 0")

        conn.commit()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, email: str, password: str) -> bool:
    init_db()
    now = datetime.utcnow().isoformat(timespec="seconds")
    try:
        with closing(_connect()) as conn:
            conn.execute(
                """
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (username, email, _hash_password(password), now),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username: str, password: str) -> int | None:
    init_db()
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row and row["password_hash"] == _hash_password(password):
        return int(row["id"])
    return None


def get_user(user_id: int) -> dict[str, Any] | None:
    init_db()
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def save_bmi(user_id: int, weight: float, height: float, imc: float, category: str) -> None:
    init_db()
    now = datetime.utcnow().isoformat(timespec="seconds")
    with closing(_connect()) as conn:
        conn.execute(
            """
            INSERT INTO bmi_history (user_id, weight, height, imc, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, weight, height, imc, category, now),
        )
        conn.commit()


def get_history(user_id: int, limit: int = 100) -> list[dict[str, Any]]:
    init_db()
    with closing(_connect()) as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, weight, height, imc, category, date
            FROM bmi_history
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]
