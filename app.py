import tkinter as tk
import requests
import io
from Essential.prepare_db import prepare_db
from PIL import Image, ImageTk
from Essential.FoodSearch import FoodSearch


class App:
    def __init__(self, master):
        self.master = master

        try:
            self.food_search = FoodSearch()
        except FileNotFoundError:
            prepare_db()
            self.food_search = FoodSearch()

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_callback)

        self.search_entry = tk.Entry(self.master, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        self.search_button = tk.Button(self.master, text="Search", command=self.search)
        self.search_button.grid(row=1, column=0, padx=10, pady=10)

        self.results_frame = tk.Frame(self.master)
        self.results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.results_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_listbox = tk.Listbox(self.results_frame, yscrollcommand=self.scrollbar.set)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.results_listbox.yview)

        self.selected_item = None

        self.image_frame = tk.Frame(self.master, bg='white')
        self.image_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=0)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(2, weight=1)

    def search_callback(self, *args):
        pass

    def search(self):
        results = self.food_search.search(self.search_var.get())
        self.update_results(results)

    def update_results(self, results):
        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result[1])

    def clear_results(self):
        self.results_listbox.delete(0, tk.END)

    def on_item_selected(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            value = widget.get(index)
            self.selected_item = value
            self.show_image(self.selected_item)

    def show_image(self, item):
        image_url = None
        for result in self.food_search.search(self.search_var.get()):
            if result[1] == item:
                image_url = result[13]
                break

        if not image_url:
            return

        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((300, 300), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        # remove old image label widget
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        self.image_frame.configure(bg='white')
        label = tk.Label(self.image_frame, image=img_tk, bg='white')
        label.image = img_tk
        label.pack(fill=tk.BOTH, expand=True)
root = tk.Tk()
app = App(root)
root.geometry("800x400")
root.title('Food Search')
app.results_listbox.bind('<<ListboxSelect>>', app.on_item_selected)

root.mainloop()
