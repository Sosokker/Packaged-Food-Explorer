# controller.py

import tkinter as tk
from model import FoodSearch
from view import AppView

class AppController:
    def __init__(self, master):
        self.master = master
        self.food_search = FoodSearch('food_data.db')
        self.view = AppView(master, self)

    def search(self, query):
        results = self.food_search.search(query)
        self.view.update_results(results)

    def clear_results(self):
        self.view.clear_results()

    def on_item_selected(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            value = widget.get(index)
            self.view.show_image(value)
