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
        
    def search(self, user_input, countries=None, limit=100) -> list:
        """
        Search for food data based on the user's input and country filter.

        Parameters:
            user_input (str): The input provided by the user to search for food data.
            countries (list, optional): A list of country names to filter the results.
                If None, no filtering based on country will be applied. Defaults to None.
            limit (int, optional): The maximum number of search results to return.
                Defaults to 100.

        Returns:
            list: A list of tuples representing the search results from the database.

        Raises:
            sqlite3.Error: If there is an error in executing the database query.
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON food_data(product_name)")

                query = "SELECT * FROM food_data WHERE product_name LIKE ?"
                params = [f"%{user_input}%"]

                if countries is not None:
                    country_filter = " OR ".join(["countries LIKE ?"] * len(countries))
                    query += f" AND ({country_filter})"
                    params.extend([f"%{country}%" for country in countries])

                query += f" LIMIT {limit}"
                results = conn.execute(query, params).fetchall()

                return results
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        
    def nutrient_show(self, product_name) -> dict:
        """Get nutrient information for a given product name from the food database.

            Parameters:
                product_name (str): The name of the product to retrieve nutrient information for.

            Returns:
                dict: A dictionary containing nutrient information as key-value pairs, where the keys represent
                    column names and the values represent the corresponding nutrient values. If no matching
                    record is found, an empty dictionary is returned.

            Raises:
                sqlite3.Error: If there is an error while accessing the database.

            """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT * 
                    FROM food_data
                    WHERE product_name = ?
                """

                cursor.execute(query, (product_name,))
                result = cursor.fetchone()
                column_names = [d[0] for d in cursor.description]
                
                if result:
                    columns_nutrient = result[16:]
                    data_dict = dict(zip(column_names[16:], columns_nutrient))
                    return data_dict
                else:
                    return dict()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        

# food_search = FoodSearch()
# results = food_search.search("pizza", countries=["thai", "japan"])
# print(results)