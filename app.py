import tkinter as tk
from tkinter import ttk
import requests
import io
from PIL import Image, ImageTk
from Essential.prepare_db import prepare_db
from Essential.FoodSearch import FoodSearch
import threading

class App:
    def __init__(self, master):
        self.master = master

        # Search food from database -----------------

        try:
            self.food_search = FoodSearch()
        except FileNotFoundError:
            prepare_db()
            self.food_search = FoodSearch()

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_callback)

        self.search_entry = ttk.Entry(self.master, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.search_button = ttk.Button(self.master, text="Search", command=self.start_search)
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.results_frame = ttk.Frame(self.master)
        self.results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.results_frame)
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        self.results_listbox = tk.Listbox(self.results_frame, yscrollcommand=self.scrollbar.set)
        self.results_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.scrollbar.config(command=self.results_listbox.yview)

        self.selected_item = None

        # Image of food -----------------

        self.image_frame = ttk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.image_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # Progress bar -----------------

        self.progress_bar = ttk.Progressbar(self.master, mode='indeterminate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        # Default image (Not Found) -----------------

        self.default_image_path = 'resources/notfound.png'  # Replace with the correct path to your default image
        self.default_image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.default_image_label = ttk.Label(self.image_frame, image=self.default_image)
        self.default_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)

        # Configure the window size and position
        self.master.geometry("800x600")
        # self.master.attributes('-fullscreen', True)

    def search_callback(self, *args):
        pass

    def start_search(self):
        # Create a new thread to execute the search function
        search_thread = threading.Thread(target=self.search)
        search_thread.start()

    def search(self):
        results = self.food_search.search(self.search_var.get())
        # Call the update_results function on the main thread to update the GUI
        self.master.after(0, self.update_results, results)

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

    # Image Showing Section -----------------

    def show_image(self, item):
        image_url = None
        for result in self.food_search.search(self.search_var.get()):
            if result[1] == item:
                image_url = result[13]
                break

        if not image_url:
            self.display_default_image()
            return

        threading.Thread(target=self.fetch_and_display_image, args=(image_url,)).start()

    def fetch_and_display_image(self, image_url):
        self.master.after(0, self.show_progress_bar)

        # Fetch the image
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((300, 300), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        self.master.after(0, self.hide_progress_bar)

        self.master.after(0, self.update_image_label, img_tk)

    def show_progress_bar(self):
        self.progress_bar.start()
        self.progress_bar.grid(row=3, column=1)

    def hide_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def display_default_image(self):
        self.master.after(0, self.update_image_label, self.default_image)

    def update_image_label(self, image):
        # Remove old image label widget
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        image_label = tk.Label(self.image_frame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=2)

    # ---------------------

root = tk.Tk()
app = App(root)
root.title('Food Search')
app.results_listbox.bind('<<ListboxSelect>>', app.on_item_selected)

root.mainloop()
