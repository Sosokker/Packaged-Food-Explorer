import sqlite3

class FoodSearch:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def search(self, user_input) -> list:
        query = f"SELECT * FROM food_data WHERE product_name LIKE '%{user_input}%'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results