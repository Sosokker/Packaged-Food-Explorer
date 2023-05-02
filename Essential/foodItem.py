class foodItem():
    def __init__(self, row):
        self.product_name = row['product_name']
        self.brands = row['brands']
        self.brands_tags = row['brands_tags']
        self.categories = row['categories']
        self.categories_tags = row['categories_tags']
        self.categories_en = row['categories_en']
        self.origins = row['origins']
        self.origins_tags = row['origins_tags']
        self.origins_en = row['origins_en']
        self.countries = row['countries']
        self.countries_tags = row['countries_tags']
        self.countries_en = row['countries_en']
        self.image_url = row['image_url']
        self.image_ingredients_url = row['image_ingredients_url']
        self.image_nutrition_url = row['image_nutrition_url']
        self.energy_kcal_100g = row['energy-kcal_100g']
        self.fat_100g = row['fat_100g']
        self.saturated_fat_100g = row['saturated-fat_100g']
        self.unsaturated_fat_100g = row['unsaturated-fat_100g']
        self.omega_3_fat_100g = row['omega-3-fat_100g']
        self.omega_6_fat_100g = row['omega-6-fat_100g']
        self.omega_9_fat_100g = row['omega-9-fat_100g']
        self.trans_fat_100g = row['trans-fat_100g']
        self.cholesterol_100g = row['cholesterol_100g']
        self.carbohydrates_100g = row['carbohydrates_100g']
        self.sugars_100g = row['sugars_100g']
        self.sucrose_100g = row['sucrose_100g']
        self.glucose_100g = row['glucose_100g']
        self.fructose_100g = row['fructose_100g']
        self.lactose_100g = row['lactose_100g']
        self.maltose_100g = row['maltose_100g']
        self.fiber_100g = row['fiber_100g']
        self.soluble_fiber_100g = row['soluble-fiber_100g']
        self.insoluble_fiber_100g = row['insoluble-fiber_100g']
        self.proteins_100g = row['proteins_100g']
        self.salt_100g = row['salt_100g']
        self.added_salt_100g = row['added-salt_100g']
        self.sodium_100g = row['sodium_100g']
        self.alcohol_100g = row['alcohol_100g']
        self.vitamin_a_100g = row['vitamin-a_100g']
        self.beta_carotene_100g = row['beta-carotene_100g']
        self.vitamin_d_100g = row['vitamin-d_100g']
        self.vitamin_e_100g = row['vitamin-e_100g']
        self.vitamin_k_100g = row['vitamin-k_100g']
        self.vitamin_c_100g = row['vitamin-c_100g']
        self.vitamin_b1_100g = row['vitamin-b1_100g']
        self.vitamin_b2_100g = row['vitamin-b2_100g']
        self.vitamin_pp_100g = row['vitamin-pp_100g']
        self.vitamin_b6_100g = row['vitamin-b6_100g']
        self.vitamin_b9_100g = row['vitamin-b1_100g']
        self.vitamin_b12_100g = row['vitamin-b12_100g']
        self.bicarbonate_100g = row['bicarbonate_100g']
        self.potassium_100g = row['potassium_100g']
        self.chloride_100g = row['chloride_100g']
        self.calcium_100g = row['calcium_100g']
        self.phosphorus_100g = row['phosphorus_100g']
        self.iron_100g = row['iron_100g']
        self.magnesium_100g = row['magnesium_100g']
        self.zinc_100g = row['zinc_100g']
        self.copper_100g = row['copper_100g']
        self.manganese_100g = row['manganese_100g']
        self.fluoride_100g = row['fluoride_100g']
        self.selenium_100g = row['selenium_100g']
        self.chromium_100g = row['chromium_100g']
        self.molybdenum_100g = row['molybdenum_100g']
        self.iodine_100g = row['iodine_100g']
        self.caffeine_100g = row['caffeine_100g']
        self.carbon_footprint_100g = row['carbon-footprint_100g']
        self.carbon_footprint_from_meat_or_fish_100g = row['carbon-footprint-from-meat-or-fish_100g']
        self.cocoa_100g = row['cocoa_100g']

    def is_vegan(self):
        if "meat" not in self.categories_en.lower() and "dairy" not in self.categories_en.lower():
            return True
        else:
            return False

    def nutrient_score_intl(self):
        nutrient_factors = {'fat': 9, 'saturated_fat': 10, 'trans_fat': 10, 'cholesterol': 5, 
                            'sodium': 6, 'carbohydrates': 7, 'sugars': 6, 'fiber': 5, 
                            'proteins': 5, 'vitamin_a': 15, 'vitamin_c': 15, 'calcium': 10, 
                            'iron': 10}
        
        nutrient_scores = {}
        for nutrient, factor in nutrient_factors.items():
            value = getattr(self, nutrient+'_100g')
            if value is not None:
                nutrient_scores[nutrient] = min(100, max(0, factor * (value / self._get_daily_requirement(nutrient))))
        
        # sum the nutrient scores to arrive at the total nutrient score
        total_score = sum(nutrient_scores.values())
        
        return total_score
    
    def _get_daily_requirement(self, nutrient):
        daily_requirement = {'fat': 70, 'saturated_fat': 20, 'trans_fat': 2, 'cholesterol': 300, 
                             'sodium': 2000, 'carbohydrates': 260, 'sugars': 90, 'fiber': 38, 
                             'proteins': 50, 'vitamin_a': 900, 'vitamin_c': 90, 'calcium': 1000, 
                             'iron': 18}
        
        # for nutrients without a daily requirement, return None
        return daily_requirement.get(nutrient, None)

    @classmethod
    def load_from_dataframe(cls, df):
        products = []
        for i, row in df.iterrows():
            product = cls(row)
            products.append(product)
        return products
    
    def __str__(self) -> str:
        return self.product_name