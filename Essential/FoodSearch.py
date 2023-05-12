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
        self.col_index = {'index': 0, 'product_name': 1, 'brands': 2, 'brands_tags': 3, 'categories': 4, 'categories_tags': 5,
                        'categories_en': 6, 'origins': 7, 'origins_tags': 8, 'origins_en': 9, 'countries': 10, 'countries_tags': 11,
                        'countries_en': 12, 'image_url': 13, 'image_ingredients_url': 14, 'image_nutrition_url': 15,
                        'energy-kcal_100g': 16, 'fat_100g': 17, 'saturated-fat_100g': 18, 'unsaturated-fat_100g': 19,
                        'omega-3-fat_100g': 20, 'omega-6-fat_100g': 21, 'omega-9-fat_100g': 22, 'trans-fat_100g': 23, 
                        'cholesterol_100g': 24, 'carbohydrates_100g': 25, 'sugars_100g': 26, 'sucrose_100g': 27, 'glucose_100g': 28, 
                        'fructose_100g': 29, 'lactose_100g': 30, 'maltose_100g': 31, 'fiber_100g': 32, 'soluble-fiber_100g': 33, 
                        'insoluble-fiber_100g': 34, 'proteins_100g': 35, 'salt_100g': 36, 'added-salt_100g': 37, 'sodium_100g': 38, 
                        'alcohol_100g': 39, 'vitamin-a_100g': 40, 'beta-carotene_100g': 41, 'vitamin-d_100g': 42, 'vitamin-e_100g': 43, 
                        'vitamin-k_100g': 44, 'vitamin-c_100g': 45, 'vitamin-b1_100g': 46, 'vitamin-b2_100g': 47, 'vitamin-pp_100g': 48, 
                        'vitamin-b6_100g': 49, 'vitamin-b9_100g': 50, 'vitamin-b12_100g': 51, 'bicarbonate_100g': 52, 
                        'potassium_100g': 53, 'chloride_100g': 54, 'calcium_100g': 55, 'phosphorus_100g': 56, 'iron_100g': 57, 
                        'magnesium_100g': 58, 'zinc_100g': 59, 'copper_100g': 60, 'manganese_100g': 61, 'fluoride_100g': 62, 
                        'selenium_100g': 63, 'chromium_100g': 64, 'molybdenum_100g': 65, 'iodine_100g': 66, 'caffeine_100g': 67, 

                        'cocoa_100g': 68, 'carbon-footprint_100g': 69, 'carbon-footprint-from-meat-or-fish_100g': 70}
        self.index_col = {0: 'index', 1: 'product_name', 2: 'brands', 3: 'brands_tags', 4: 'categories', 5: 'categories_tags', 
                          6: 'categories_en', 7: 'origins', 8: 'origins_tags', 9: 'origins_en', 10: 'countries', 11: 'countries_tags', 
                          12: 'countries_en', 13: 'image_url', 14: 'image_ingredients_url', 15: 'image_nutrition_url', 
                          16: 'energy-kcal_100g', 17: 'fat_100g', 18: 'saturated-fat_100g', 19: 'unsaturated-fat_100g', 
                          20: 'omega-3-fat_100g', 21: 'omega-6-fat_100g', 22: 'omega-9-fat_100g', 23: 'trans-fat_100g', 
                          24: 'cholesterol_100g', 25: 'carbohydrates_100g', 26: 'sugars_100g', 27: 'sucrose_100g', 28: 'glucose_100g', 
                          29: 'fructose_100g', 30: 'lactose_100g', 31: 'maltose_100g', 32: 'fiber_100g', 33: 'soluble-fiber_100g', 
                          34: 'insoluble-fiber_100g', 35: 'proteins_100g', 36: 'salt_100g', 37: 'added-salt_100g', 38: 'sodium_100g', 
                          39: 'alcohol_100g', 40: 'vitamin-a_100g', 41: 'beta-carotene_100g', 42: 'vitamin-d_100g', 
                          43: 'vitamin-e_100g', 44: 'vitamin-k_100g', 45: 'vitamin-c_100g', 46: 'vitamin-b1_100g', 
                          47: 'vitamin-b2_100g', 48: 'vitamin-pp_100g', 49: 'vitamin-b6_100g', 50: 'vitamin-b9_100g', 
                          51: 'vitamin-b12_100g', 52: 'bicarbonate_100g', 53: 'potassium_100g', 54: 'chloride_100g', 
                          55: 'calcium_100g', 56: 'phosphorus_100g', 57: 'iron_100g', 58: 'magnesium_100g', 59: 'zinc_100g', 
                          60: 'copper_100g', 61: 'manganese_100g', 62: 'fluoride_100g', 63: 'selenium_100g', 64: 'chromium_100g', 
                          65: 'molybdenum_100g', 66: 'iodine_100g', 67: 'caffeine_100g', 68: 'cocoa_100g', 69: 'carbon-footprint_100g', 
                          70: 'carbon-footprint-from-meat-or-fish_100g'}

    def search(self, user_input, countries=None, limit=100, categories=None, categories_both=None, column_filters=None) -> list:
        """
        Search for food data based on the user's input, country filter, category filter, and column filters.

        Parameters:
            user_input (str): The input provided by the user to search for food data.
            countries (list, optional): A list of country names to filter the results.
                If None, no filtering based on country will be applied. Defaults to None.
            limit (int, optional): The maximum number of search results to return.
                Defaults to 100.
            categories (list, optional): A list of category words to filter the results.
                If None, no filtering based on categories will be applied. Defaults to None.
            categories_both (list, optional): A list of category words to filter the results.
                The result must contain all words in this list.
                If None, no filtering based on categories will be applied. Defaults to None.
            column_filters (dict, optional): A dictionary of column index and condition pairs for filtering.
                The keys represent the column index (int), and the values represent the condition (str).
                The condition format follows the pattern: {column_index}:{condition}.
                If None, no filtering based on column values will be applied. Defaults to None.

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

                if categories is not None:
                    category_filters = []
                    for category in categories:
                        category_filters.append("categories LIKE ? OR categories_tags LIKE ? OR categories_en LIKE ?")
                        params.extend([f"%{category}%", f"%{category}%", f"%{category}%"])

                    category_filter = " OR ".join(category_filters)
                    query += f" AND ({category_filter})"
                
                if categories_both is not None:
                    category_filters2 = []
                    for category in categories_both:
                        category_filters2.append("(categories LIKE ? OR categories_tags LIKE ? OR categories_en LIKE ?)")
                        params.extend([f"%{category}%", f"%{category}%", f"%{category}%"])

                    category_filter2 = " AND ".join(category_filters2)
                    query += f" AND ({category_filter2})"
                
                if column_filters is not None:
                    for column_index, condition in column_filters.items():
                        col_name = self.index_col[column_index]
                        query += f" AND [{col_name}] {condition}"
                
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
# results = food_search.search("apple", countries=["thai"], categories=["fruit", "snack"], column_filters={16:">=1"}, limit=10)
# print(results)