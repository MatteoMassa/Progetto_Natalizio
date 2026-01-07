import sqlite3
from typing import Optional, List, Dict, Any, Tuple

class TransactionRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add(
        self,
        user_id: int,
        category_id: int,
        tx_type: str,
        description: str,
        amount: float,
        date: str
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO transactions(user_id, category_id, type, description, amount, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, category_id, tx_type, description, amount, date))
            conn.commit()

    def list_for_user(
        self,
        user_id: int,
        start: Optional[str],
        end: Optional[str]
    ) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            query = """
            SELECT t.id, t.type, t.description, t.amount, t.date, c.name
            FROM transactions t
            JOIN categories c ON c.id = t.category_id
            WHERE t.user_id = ?
            """
            params = [user_id]

            if start:
                query += " AND t.date >= ?"
                params.append(start)
            if end:
                query += " AND t.date <= ?"
                params.append(end)

            query += " ORDER BY t.date DESC, t.id DESC"

            cur.execute(query, params)
            rows = cur.fetchall()

            return [{
                "id": r[0],
                "type": r[1],
                "description": r[2],
                "amount": float(r[3]),
                "date": r[4],
                "category": r[5]
            } for r in rows]

    def totals_for_user(
        self,
        user_id: int,
        start: Optional[str],
        end: Optional[str]
    ) -> Tuple[float, float]:
        txs = self.list_for_user(user_id, start, end)
        income = sum(t["amount"] for t in txs if t["type"] == "income")
        expense = sum(t["amount"] for t in txs if t["type"] == "expense")
        return income, expense
