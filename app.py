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
        self.master.title('Food Search')

        # Search food from database -----------------

        try:
            self.food_search = FoodSearch()
        except FileNotFoundError:
            prepare_db()
            self.food_search = FoodSearch()

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_callback)

        self.results_frame = ttk.Frame(self.master)
        self.results_frame.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.results_frame)
        self.scrollbar.grid(row=0, column=2,rowspan=2, sticky="ns")

        self.results_listbox = tk.Listbox(self.results_frame, yscrollcommand=self.scrollbar.set,height=20,width=20,selectmode=tk.SINGLE)
        self.results_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.scrollbar.config(command=self.results_listbox.yview)

       # Filter frame -----------------

        self.filter_frame = ttk.LabelFrame(self.master, text="Filter")
        self.filter_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # Filter components -----------------

        # Search
        self.search_entry = ttk.Entry(self.filter_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.search_button = ttk.Button(self.filter_frame, text="Search", command=self.start_search)
        self.search_button.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # Filter
        self.country_var = tk.StringVar()
        self.country_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.country_var, values=["Any" ,"Thai", "Japan", "US"])
        self.country_dropdown.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.organic_var = tk.IntVar()
        self.organic_checkbox = ttk.Checkbutton(self.filter_frame, text="Organic", variable=self.organic_var)
        self.organic_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.plant_based_var = tk.IntVar()
        self.plant_based_checkbox = ttk.Checkbutton(self.filter_frame, text="Plant-Based", variable=self.plant_based_var)
        self.plant_based_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.beverages_var = tk.IntVar()
        self.beverages_checkbox = ttk.Checkbutton(self.filter_frame, text="Beverages", variable=self.beverages_var)
        self.beverages_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.snack_var = tk.IntVar()
        self.snack_checkbox = ttk.Checkbutton(self.filter_frame, text="Snack", variable=self.snack_var)
        self.snack_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        self.calories_var = tk.StringVar()
        self.calories_entry = ttk.Entry(self.filter_frame, textvariable=self.calories_var)
        self.calories_entry.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

        self.nutrient_var = tk.StringVar()
        self.nutrient_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.nutrient_var, values=["Protein", "Carbohydrates", "Fat", ""])
        self.nutrient_dropdown.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")

        self.nutrient_value_var = tk.StringVar()
        self.nutrient_value_entry = ttk.Entry(self.filter_frame, textvariable=self.nutrient_value_var)
        self.nutrient_value_entry.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")

        # Filter components (continued) -----------------

        self.nutrient_operator_var = tk.StringVar()
        self.nutrient_operator_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.nutrient_operator_var, values=["<", ">", "="])
        self.nutrient_operator_dropdown.grid(row=8, column=0, padx=10, pady=5, sticky="nsew")

        # Image of food -----------------

        self.image_frame = ttk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.image_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.image_frame.grid_propagate(0)

        # Progress bar -----------------

        self.process_frame = tk.Frame(root)
        self.process_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="ew")
        s = ttk.Style()
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        # Stackoverflow.com https://stackoverflow.com/questions/13510882/how-to-change-ttk-progressbar-color-in-python
        self.progress_bar = ttk.Progressbar(self.process_frame, style="red.Horizontal.TProgressbar", orient="horizontal",
                        length=700, mode="indeterminate")
        self.progress_bar.grid(row=0, column=0)

        # Default image (Not Found) -----------------

        self.default_image_path = 'resources/notfound.png'  # Replace with the correct path to your default image
        self.default_image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.default_image_label = ttk.Label(self.image_frame, image=self.default_image)
        # self.default_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.default_image_label.pack(anchor='w', fill=tk.BOTH)

        # Nutrient Frame

        self.nutrient_frame = ttk.LabelFrame(self.master, text="Nutrient")
        self.nutrient_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Others Frame (Graph/Analyze)

        # * Configure the window size and position
        # self.master.attributes('-fullscreen', True)
        # width= self.master.winfo_screenwidth()
        # height= self.master.winfo_screenheight()
        # self.master.geometry("%dx%d" % (width, height))

    # LIST BOX selected FUNC

    def nutrient_labeler(self, product_name, frame):
        count = 0
        selected_nutrients = [
            'energy-kcal_100g',
            'proteins_100g',
            'carbohydrates_100g',
            'fat_100g',
            'fiber_100g',
            'sugars_100g',
            'saturated-fat_100g',
            'unsaturated-fat_100g'
            'sodium_100g',
            'vitamin-a_100g',
            'vitamin-c_100g',
            'calcium_100g',
            'iron_100g',
            'potassium_100g',
            'cholesterol_100g',
            'trans-fat_100g'
        ]

        for widget in frame.winfo_children():
            widget.grid_forget()
        for name, value in self.food_search.nutrient_show(product_name).items():
            if name in selected_nutrients:
                count += 1
                if value is None:
                    value_text = "N/A"
                else:
                    value_text = f"{value:.3f}"
                ttk.Label(frame, text=f"{name}: {value_text}").grid(row=count, column=0)

    def on_item_selected(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            value = widget.get(index)
            self.selected_item = value
            self.show_image(self.selected_item)
            self.nutrient_labeler(self.selected_item, self.nutrient_frame)

    # SEARCH FUNC

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
        img = img.resize((300, 300), Image.LANCZOS)
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
app.results_listbox.bind('<<ListboxSelect>>', app.on_item_selected)

root.mainloop()
