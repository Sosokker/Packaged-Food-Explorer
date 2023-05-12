import sqlite3
import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
import io
from PIL import Image, ImageTk
from Essential.prepare_db import prepare_db
from Essential.FoodSearch import FoodSearch
import threading
import sqlite3
import pandas as pd
from Essential.plotter import plotter


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Package Food Database')
        self.df = pd.read_sql_query("SELECT * FROM food_data", sqlite3.connect(r"Essential\data\food_data.db"))
        self.plotter = plotter()
        self.__curr_index = 0
        # Search food from database -----------------

        try:
            self.food_search = FoodSearch()
        except FileNotFoundError:
            prepare_db()
            self.food_search = FoodSearch()

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_callback)

        self.results_frame = ttk.Frame(self.master)
        self.results_frame.grid(row=0, column=0, columnspan=1, rowspan=2, sticky="nsew")
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.results_frame)
        self.scrollbar.grid(row=0, column=2,rowspan=2, sticky="ns")

        self.results_listbox = tk.Listbox(self.results_frame, yscrollcommand=self.scrollbar.set,height=20,width=20,selectmode=tk.SINGLE)
        self.results_listbox.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")

        self.scrollbar.config(command=self.results_listbox.yview)

       # Filter frame -----------------

        self.filter_frame = ttk.LabelFrame(self.master, text="Filter")
        self.filter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.checkbox_frame = ttk.LabelFrame(self.filter_frame, text="Categories")
        self.checkbox_frame.grid(row=1, column=0, sticky="nsew")

        self.nutrient_comp_frame = ttk.LabelFrame(self.filter_frame, text="Nutrients Quantity")
        self.nutrient_comp_frame.grid(row=2, column=0, sticky="nsew")

        self.calories_comp =ttk.LabelFrame(self.nutrient_comp_frame, text="Calories")
        self.calories_comp.grid(row=0, column=0, sticky="nsew")

        self.protein_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Protein")
        self.protein_comp.grid(row=0, column=1, sticky="nsew")

        self.carbohydrate_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Carbohydrate")
        self.carbohydrate_comp.grid(row=0, column=2, sticky="nsew")

        self.fat_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Fat")
        self.fat_comp.grid(row=1, column=0, sticky="nsew")

        self.sugar_comp =ttk.LabelFrame(self.nutrient_comp_frame, text="Sugar")
        self.sugar_comp.grid(row=1, column=1, sticky="nsew")
        # Filter components -----------------

        # * Filter Drop Down
        ttk.Label(self.filter_frame, text = "Select the Country :").grid(column = 0, 
                row = 0, padx = 2)
        self.country_var = tk.StringVar()
        self.country_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.country_var, values=["Any" ,"Thai", "Japan", "US"])
        self.country_dropdown.configure()
        self.country_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # * Filter CheckBox
        self.organic_var = tk.IntVar()
        self.organic_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Organic", variable=self.organic_var)
        self.organic_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.plant_based_var = tk.IntVar()
        self.plant_based_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Plant-Based", variable=self.plant_based_var)
        self.plant_based_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.beverages_var = tk.IntVar()
        self.beverages_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Beverages", variable=self.beverages_var)
        self.beverages_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.snack_var = tk.IntVar()
        self.snack_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Snack", variable=self.snack_var)
        self.snack_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        # * Filter Value filter
        self.calories_var = tk.StringVar()
        self.calories_entry = ttk.Entry(self.calories_comp, textvariable=self.calories_var)
        self.calories_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.calories_more_op = tk.IntVar()
        self.calories_op = ttk.Checkbutton(self.calories_comp, text="More than", variable=self.calories_more_op)
        self.calories_op.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.calories_less_val = tk.IntVar()
        self.calories_op = ttk.Checkbutton(self.calories_comp, text="Less than", variable=self.calories_less_val)
        self.calories_op.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")


        # Image of food -----------------

        self.image_frame = ttk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.image_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        # Progress bar -----------------

        self.process_frame = tk.Frame(root)
        self.process_frame.grid(row=4, column=0, columnspan=1, padx=10, pady=10, sticky="ew")
        s = ttk.Style()
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        # Stackoverflow.com https://stackoverflow.com/questions/13510882/how-to-change-ttk-progressbar-color-in-python
        self.progress_bar = ttk.Progressbar(self.process_frame, style="red.Horizontal.TProgressbar", orient="horizontal",
                        length=700, mode="indeterminate")
        self.progress_bar.grid(row=0, column=0)

        # Default image (Not Found) -----------------

        self.default_image_path = 'resources/notfound.png'
        self.default_image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.default_image_label = ttk.Label(self.image_frame, image=self.default_image)
        # self.default_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.default_image_label.pack(anchor='w', fill=tk.BOTH)

        # Nutrient Frame
        self.nutrient_frame = ttk.LabelFrame(self.master, text="Nutrient")
        self.nutrient_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew", rowspan=2)
        self.nutrient_table = NutrientTableHolder(self.nutrient_frame)
        self.nutrient_table.create_table()

        # Others Frame (Graph/Analyze)

        self.graph_frame = ttk.LabelFrame(self.master, text="Bar Macronutrients Graph", width=350, height=300)
        self.graph_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.graph_frame.grid_propagate(0)

        #* Option + Search
        self.fullview = ttk.LabelFrame(self.master, text="Options")
        self.fullview.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.popup_plot = ttk.Button(self.fullview, text="Full Plot", command=self.plot_popup)
        self.popup_plot.grid(row=1, column=1, padx=10, pady=10)
        self.popup_plot.configure(state=tk.DISABLED)

        # Search
        self.search_entry = ttk.Entry(self.fullview, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.search_button = ttk.Button(self.fullview, text="Search", command=self.start_search)
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # * Configure the window size and position
        # self.master.attributes('-fullscreen', True)
        width= self.master.winfo_screenwidth()
        height= self.master.winfo_screenheight()
        self.master.geometry("%dx%d" % (width, height))

    # LIST BOX selected FUNC

    def on_item_selected(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.__curr_index = selection[0]
            value = widget.get(index)
            self.selected_item = value
            self.show_image(self.selected_item)
            self.nutrient_table.nutrient_labeler(self.food_search.nutrient_show(self.selected_item))
            self.plot_preview(self.graph_frame, self.df, row_index=selection[0], nutrient_indices=[25, 26, 35, 17], g_type='bar')
            self.popup_plot.configure(state=tk.NORMAL)

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
        img.thumbnail((300, 300), Image.LANCZOS)

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
        image_label.pack(anchor='w', fill=tk.BOTH)
    # ---------------------

    # Plot zone

    def plot_preview(self, frame, df, row_index: int, nutrient_indices: list, g_type: str):
        for widget in frame.winfo_children():
            widget.pack_forget()
        self.p = plotter()
        self.p.nutrient_plotter(df, row_index, nutrient_indices, g_type, popup=False, frame=frame)

    def plot_popup(self):
        self.p = plotter()
        self.p.nutrient_plotter(self.df, self.__curr_index, [17,25, 32, 26, 18, 19, 38, 36, 23, 24], 'barpie')

    # --------------------- Properties

    @property
    def getCurrIndex(self):
        return self.__curr_index
    
    @getCurrIndex.setter
    def setCurrIndex(self, val):
        self.__curr_index = val

class NutrientTableHolder:
    def __init__(self, root):
        self.root = root
        self.treeview = None

    def create_table(self):
        selected_nutrients = [
            'energy-kcal_100g',
            'proteins_100g',
            'carbohydrates_100g',
            'fat_100g',
            'fiber_100g',
            'sugars_100g',
            'saturated-fat_100g',
            'unsaturated-fat_100g',
            'sodium_100g',
            'vitamin-a_100g',
            'vitamin-c_100g',
            'calcium_100g',
            'iron_100g',
            'potassium_100g',
            'cholesterol_100g',
            'trans-fat_100g'
        ]

        self.treeview = ttk.Treeview(self.root)
        self.treeview['columns'] = ('Value')
        self.treeview.heading("#0", text="Nutrient")
        self.treeview.heading("Value", text="Value")
        
        for name in selected_nutrients:
            value = 0
            value_text = f"{value:.3f}"
            self.treeview.insert('', 'end', text=name, values=(value_text,))
        
        self.treeview.pack(fill='both', expand=True)

    def nutrient_labeler(self, nutrient_dict_product):
        selected_nutrients = [
            'energy-kcal_100g',
            'proteins_100g',
            'carbohydrates_100g',
            'fat_100g',
            'fiber_100g',
            'sugars_100g',
            'saturated-fat_100g',
            'unsaturated-fat_100g',
            'salt_100g',
            'sodium_100g',
            'vitamin-a_100g',
            'vitamin-c_100g',
            'calcium_100g',
            'iron_100g',
            'potassium_100g',
            'cholesterol_100g',
            'trans-fat_100g'
        ]

        for widget in self.root.winfo_children():
            widget.pack_forget()

        treeview = ttk.Treeview(self.root)
        treeview['columns'] = ('Value')
        treeview.heading("#0", text="Nutrient")
        treeview.heading("Value", text="Value")

        for name, value in nutrient_dict_product.items():
            if name in selected_nutrients:
                if value is None:
                    value_text = "N/A"
                else:
                    value_text = f"{value:.3f}"
                treeview.insert('', 'end', text=name, values=(value_text,))

        treeview.pack(fill='both', expand=True)

root = tk.Tk()
root.deiconify()
app = App(root)
app.results_listbox.bind('<<ListboxSelect>>', app.on_item_selected)

root.mainloop()
