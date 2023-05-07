import sqlite3
import os.path

# Static path
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = (current_dir + r"\data\food_data.db")

class FoodSearch:
    """
    A class for searching food data in a SQLite database.

    Methods:
        search(user_input): Search for food data based on user input.

    Usage:
        food_search = FoodSearch()
        results = food_search.search("apple")
    """

    def __init__(self):
        if not os.path.exists(db_path):
            raise FileNotFoundError("Database file not found.")

        self.db_path = db_path
        
    def search(self, user_input) -> list:
        """
        Search for food data based on the user's input.

        Parameters:
            user_input (str): The input provided by the user to search for food data.

        Returns:
            list: A list of tuples representing the search results from the database.

        Raises:
            sqlite3.Error: If there is an error in executing the database query.
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM food_data WHERE product_name LIKE ?"
                cursor.execute(query, (f"%{user_input}%",))
                results = cursor.fetchall()
                return results
        except sqlite3.Error as e:

            print(f"Database error: {e}")
            return []