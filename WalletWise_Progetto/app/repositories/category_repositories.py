import sqlite3
from typing import Optional, Dict, Any, List

class CategoryRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def list_all(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM categories ORDER BY name ASC")
            return [{"id": r[0], "name": r[1]} for r in cur.fetchall()]

    def get_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM categories WHERE id = ?", (category_id,))
            r = cur.fetchone()
            if r is None:
                return None
            return {"id": r[0], "name": r[1]}
