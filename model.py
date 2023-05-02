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
    
import sqlite3

class FoodNutrient:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.nutrient_columns = [
            'energy-kcal_100g',
            'fat_100g',
            'saturated-fat_100g',
            'cholesterol_100g',
            'carbohydrates_100g',
            'fiber_100g',
            'proteins_100g',
            'salt_100g',
            'sodium_100g',
            'potassium_100g',
            'calcium_100g',
            'iron_100g',
            'vitamin-a_100g',
            'vitamin-c_100g'
        ]

    def throw_nutrient(self, index_val):
        nutrient_cols = ", ".join([f"`{col}`" for col in self.nutrient_columns])
        query = f"SELECT {nutrient_cols} FROM food_data WHERE `index` = {index_val}"
        self.cursor.execute(query)
        nutrient_data = self.cursor.fetchone()

        return {col: nutrient_data[i] for i, col in enumerate(self.nutrient_columns)}

fn = FoodNutrient('food_data.db')
print(fn.throw_nutrient(3))