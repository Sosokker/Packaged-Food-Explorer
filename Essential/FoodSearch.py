import sqlite3
import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = (current_dir + r"\data\food_data.db")

class FoodSearch:
    def __init__(self):
        self.status = os.path.exists(db_path)
        if self.status:
            self.conn = sqlite3.connect(db_path)
        else:
            raise FileNotFoundError
        self.cursor = self.conn.cursor()
        
    def search(self, user_input) -> list:
        query = f"SELECT * FROM food_data WHERE product_name LIKE '%{user_input}%'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results