import sqlite3
import pandas as pd

class TradeDatabase:
    def __init__(self, db_name="trades.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Create trades table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    time TEXT,
                    symbol TEXT,
                    type TEXT,
                    price REAL,
                    quantity INTEGER
                )
            """)
            conn.commit()

    def save_trade(self, trade):
        """Save a trade to the database."""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                INSERT INTO trades (time, symbol, type, price, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (trade["time"], trade["symbol"], trade["type"], trade["price"], trade["quantity"]))
            conn.commit()

    def get_trades(self):
        """Retrieve all trades from the database."""
        with sqlite3.connect(self.db_name) as conn:
            df = pd.read_sql_query("SELECT * FROM trades", conn)
            return df