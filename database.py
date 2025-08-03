import sqlite3
import pandas as pd

class TradeDatabase:
    def __init__(self, db_name="trades.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Create trades table if it doesn't exist."""
        try:
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
        except Exception as e:
            print(f"Error creating database table: {e}")

    def save_trade(self, trade):
        """Save a trade to the database."""
        try:
            # Validate trade data
            required_fields = ["time", "symbol", "type", "price", "quantity"]
            if not all(field in trade for field in required_fields):
                print(f"Trade missing required fields: {required_fields}")
                return False
                
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("""
                    INSERT INTO trades (time, symbol, type, price, quantity)
                    VALUES (?, ?, ?, ?, ?)
                """, (trade["time"], trade["symbol"], trade["type"], trade["price"], trade["quantity"]))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving trade to database: {e}")
            return False

    def get_trades(self):
        """Retrieve all trades from the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query("SELECT * FROM trades", conn)
                return df
        except Exception as e:
            print(f"Error retrieving trades from database: {e}")
            return pd.DataFrame()