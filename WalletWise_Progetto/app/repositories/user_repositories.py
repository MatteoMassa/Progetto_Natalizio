import sqlite3
from typing import Optional, Dict, Any

class UserRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            return {"id": row[0], "username": row[1], "password_hash": row[2]}

    def create(self, username: str, password_hash: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return cur.lastrowid
