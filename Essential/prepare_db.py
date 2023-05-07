import os
import sqlite3
import pandas as pd
import re

def prepare_db():

    dfs = []
    for i in range(1, 5):
        filename = f'Essential/data/us_data_{i}.csv'
        df = pd.read_csv(filename)
        dfs.append(df)

    thai_df = pd.read_csv('Essential/data/thai_data.csv')
    us_df = pd.concat(dfs, ignore_index=True)
    japan_df = pd.read_csv('Essential/data/japan_data.csv')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(current_dir + r"\data\food_data.db")

    # Clean
    combined_df = pd.concat([thai_df, us_df, japan_df], ignore_index=True)
    combined_df = combined_df[~combined_df.product_name.str.contains('to be deleted', na=False, flags=re.IGNORECASE)]
    combined_df = combined_df.dropna(subset=['product_name'])

    combined_df.to_sql('food_data', conn, if_exists='replace')

    conn.commit()
    conn.close()