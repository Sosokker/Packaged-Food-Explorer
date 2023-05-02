import sqlite3
import pandas as pd
import re

thai_df = pd.read_csv('thai_data.csv')
us_df = pd.read_csv('us_data.csv')
japan_df = pd.read_csv('japan_data.csv')

conn = sqlite3.connect('food_data.db')

thai_df = thai_df[~thai_df.product_name.str.contains('to be deleted', na=False, flags=re.IGNORECASE)]
japan_df = japan_df[~japan_df.product_name.str.contains('to be deleted', na=False, flags=re.IGNORECASE)]
us_df = us_df[~us_df.product_name.str.contains('to be deleted', na=False, flags=re.IGNORECASE)]

thai_df = thai_df.dropna(subset=['product_name'])
japan_df = japan_df.dropna(subset=['product_name'])
us_df = us_df.dropna(subset=['product_name'])

thai_df.to_sql('thai_food', conn, if_exists='replace', index=False)
us_df.to_sql('us_food', conn, if_exists='replace', index=False)
japan_df.to_sql('japan_food', conn, if_exists='replace', index=False)

conn.commit()
conn.close()