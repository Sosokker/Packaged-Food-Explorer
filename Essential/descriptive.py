import sqlite3
import tkinter as tk
from tkinter import ttk
import pandas as pd

class Descriptive:
    def __init__(self, data):
        self.data = data

    def show_statistics(self):
        statistics = self.data.describe()
        window = tk.Toplevel()
        tree = ttk.Treeview(window)
        columns = statistics.columns.tolist()
        tree["columns"] = columns
        tree.heading("#0", text="Statistic")
        for column in columns:
            tree.heading(column, text=column)

        for stat in statistics.index:
            values = statistics.loc[stat].tolist()
            tree.insert("", "end", text=stat, values=values)

        tree.pack()
        window.mainloop()



# df = pd.read_sql_query("SELECT * FROM food_data", sqlite3.connect(r"D:\Food-Nutrient-Viewer-Tkinter\Essential\data\food_data.db"))
# descriptive = Descriptive(df[['product_name', 'carbohydrates_100g','sugars_100g','energy-kcal_100g','fat_100g','proteins_100g']])
# descriptive.show_statistics()