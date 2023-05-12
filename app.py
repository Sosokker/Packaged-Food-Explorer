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
from Essential.descriptive import Descriptive

class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Package Food Database')
        self.df = pd.read_sql_query("SELECT * FROM food_data", sqlite3.connect(r"Essential\data\food_data.db"))
        self.plotter = plotter()
        self.__curr_index = 0

        # ! For plot
        self.ind = []
        self.gmode = None
        # ! --------
        
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
        self.checkbox_frame.grid(row=1, column=0, sticky="nsew", padx=15)

        self.nutrient_comp_frame = ttk.LabelFrame(self.filter_frame, text="Nutrients Quantity")
        self.nutrient_comp_frame.grid(row=2, column=0, sticky="nsew", pady=5)

        self.calories_comp =ttk.LabelFrame(self.nutrient_comp_frame, text="Calories")
        self.calories_comp.grid(row=0, column=0, sticky="nsew", padx=15)

        self.protein_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Protein")
        self.protein_comp.grid(row=0, column=1, sticky="nsew", padx=15)

        self.carbohydrate_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Carbohydrate")
        self.carbohydrate_comp.grid(row=1, column=1, sticky="nsew", padx=15)

        self.fat_comp = ttk.LabelFrame(self.nutrient_comp_frame, text="Fat")
        self.fat_comp.grid(row=1, column=0, sticky="nsew", padx=15)

        self.country_frame = ttk.LabelFrame(self.filter_frame, text="Country")
        self.country_frame.grid(row=0, column=0, sticky='nsew', padx=15)
        # Filter components -----------------

        # * Filter Drop Down
        self.country_var = tk.StringVar()
        self.country_dropdown = ttk.Combobox(self.country_frame, textvariable=self.country_var, values=["Any" ,"Thai", "Japan", "US"])
        self.country_dropdown.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # * Filter CheckBox
        self.organic_var = tk.IntVar()
        self.organic_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Organic", variable=self.organic_var)
        self.organic_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.plant_based_var = tk.IntVar()
        self.plant_based_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Plant-Based", variable=self.plant_based_var)
        self.plant_based_checkbox.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.beverages_var = tk.IntVar()
        self.beverages_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Beverages", variable=self.beverages_var)
        self.beverages_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.snack_var = tk.IntVar()
        self.snack_checkbox = ttk.Checkbutton(self.checkbox_frame, text="Snack", variable=self.snack_var)
        self.snack_checkbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.entry_own_var = tk.StringVar()
        self.entry_own = ttk.Entry(self.checkbox_frame, textvariable=self.entry_own_var)
        self.entry_own.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

        # * Filter Value filter


        self.calories_var_op = tk.StringVar()
        self.calories_less_op = ttk.Radiobutton(self.calories_comp, text='Less than', value='<', variable=self.calories_var_op)
        self.calories_more_op = ttk.Radiobutton(self.calories_comp, text='More than', value='>', variable=self.calories_var_op)
        self.calories_less_op.grid(row=1, column=0)
        self.calories_more_op.grid(row=2, column=0)

        self.calories_var = tk.StringVar()
        self.calories_entry = ttk.Entry(self.calories_comp, textvariable=self.calories_var)
        self.calories_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        #!-------
        self.protein_var_op = tk.StringVar()
        self.protein_less_op = ttk.Radiobutton(self.protein_comp, text='Less than', value='<', variable=self.protein_var_op)
        self.protein_more_op = ttk.Radiobutton(self.protein_comp, text='More than', value='>', variable=self.protein_var_op)
        self.protein_less_op.grid(row=1, column=0)
        self.protein_more_op.grid(row=2, column=0)

        self.protein_var = tk.StringVar()
        self.protein_entry = ttk.Entry(self.protein_comp, textvariable=self.protein_var)
        self.protein_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        #!-------
        self.carbo_var_op = tk.StringVar()
        self.carbo_less_op = ttk.Radiobutton(self.carbohydrate_comp, text='Less than', value='<', variable=self.carbo_var_op)
        self.carbo_more_op = ttk.Radiobutton(self.carbohydrate_comp, text='More than', value='>', variable=self.carbo_var_op)
        self.carbo_less_op.grid(row=1, column=0)
        self.carbo_more_op.grid(row=2, column=0)

        self.carbo_var = tk.StringVar()
        self.carbo_entry = ttk.Entry(self.carbohydrate_comp, textvariable=self.carbo_var)
        self.carbo_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        
        #!-------
        self.fat_var_op = tk.StringVar()
        self.fat_less_op = ttk.Radiobutton(self.fat_comp, text='Less than', value='<', variable=self.fat_var_op)
        self.fat_more_op = ttk.Radiobutton(self.fat_comp, text='More than', value='>', variable=self.fat_var_op)
        self.fat_less_op.grid(row=1, column=0)
        self.fat_more_op.grid(row=2, column=0)

        self.fat_var = tk.StringVar()
        self.fat_entry = ttk.Entry(self.fat_comp, textvariable=self.fat_var)
        self.fat_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        
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
                        length=500, mode="indeterminate")
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

        self.graph_frame = ttk.Notebook(self.master, width=350, height=300)
        self.graph_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.graph_frame.grid_propagate(0)

        self.g1f = ttk.LabelFrame(self.graph_frame, text="Bar Macronutrients Graph", width=350, height=300)
        self.g1f.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.g1f.grid_propagate(0)

        self.g2f = ttk.LabelFrame(self.graph_frame, text="Pie Macronutrients Graph", width=350, height=300)
        self.g2f.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.g2f.grid_propagate(0)
        self.graph_frame.add(self.g1f, text='Bar Graph')
        self.graph_frame.add(self.g2f, text='Pie Graph')

        #* Option + Search

        self.fullview = ttk.Notebook(self.master)
        self.fullview.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.plot_frame = ttk.LabelFrame(self.fullview)
        self.plot_frame.grid(row=1 ,column=0, sticky="nsew", padx=10)

        self.search_frame = ttk.LabelFrame(self.fullview)
        self.search_frame.grid(row=1 ,column=0, sticky="nsew", padx=10)

        self.sub_search = ttk.LabelFrame(self.search_frame, text="Search and Adjust")
        self.sub_search.pack(fill=tk.BOTH, padx=5)

        self.sub_plot = ttk.LabelFrame(self.plot_frame, text="Plot")
        self.sub_plot.pack(fill=tk.BOTH, padx=5)

        self.fullview.add(self.search_frame, text="Search Page")
        self.fullview.add(self.plot_frame, text="Plot Page")

        self.popup_plot = ttk.Button(self.sub_plot, text="Plot", command=self.plot_popup)
        self.popup_plot.grid(row=1, column=0, padx=10, pady=10)
        self.popup_plot.configure(state=tk.DISABLED)

        self.descriptive_stat = ttk.Button(self.sub_plot, text='Statistic Of Current Filtered Data', command=self.show_des_stat)
        self.descriptive_stat.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.plotall = ttk.Button(self.sub_plot, text="Plot All Component", command=self.plot_popup)
        self.plotall.grid(row=1, column=1, padx=10, pady=10)
        self.plotall.configure(state=tk.DISABLED)

        self.cal16 = tk.IntVar()
        self.cal_plot = ttk.Checkbutton(self.sub_plot, text="Calories", variable=self.cal16)
        self.cal_plot.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.pro35 = tk.IntVar()
        self.pro_plot = ttk.Checkbutton(self.sub_plot, text="Protein", variable=self.pro35)
        self.pro_plot.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)

        self.car25 = tk.IntVar()
        self.car_plot = ttk.Checkbutton(self.sub_plot, text="Carbohydrate", variable=self.car25)
        self.car_plot.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

        self.fat17 = tk.IntVar()
        self.fat_plot = ttk.Checkbutton(self.sub_plot, text="Fat", variable=self.fat17)
        self.fat_plot.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)

        self.sodium38 = tk.IntVar()
        self.sodium_plot = ttk.Checkbutton(self.sub_plot, text="Sodium", variable=self.sodium38)
        self.sodium_plot.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)

        self.tran23 = tk.IntVar()
        self.tran_plot = ttk.Checkbutton(self.sub_plot, text="Tran-fats", variable=self.tran23)
        self.tran_plot.grid(row=5, column=1, sticky="nsew", padx=10, pady=5)

        self.cholesterol24 = tk.IntVar()
        self.tran_plot = ttk.Checkbutton(self.sub_plot, text="Cholesterol", variable=self.cholesterol24)
        self.tran_plot.grid(row=6, column=0, sticky="nsew", padx=10, pady=5)

        # Search

        # This code is from <https://stackoverflow.com/questions/17635905/ttk-entry-background-colour>
        entrystyle = ttk.Style()
        entrystyle.element_create("plain.field", "from", "clam")
        entrystyle.layout("EntryStyle.TEntry",
                        [('Entry.plain.field', {'children': [(
                            'Entry.background', {'children': [(
                                'Entry.padding', {'children': [(
                                    'Entry.textarea', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})], 'sticky': 'nswe'})],
                            'border':'2', 'sticky': 'nswe'})])
        entrystyle.configure("EntryStyle.TEntry",
                        background="green", 
                        foreground="grey",
                        fieldbackground="gray")
        # --------------------------------------------------------------------------------------------

        ttk.Label(self.sub_search, text="Search Bar").pack(fill="both", pady=10, padx= 10)

        self.search_entry = ttk.Entry(self.sub_search, textvariable=self.search_var, style="EntryStyle.TEntry")
        self.search_entry.pack(fill="both", pady=10, padx= 10)

        self.search_button = ttk.Button(self.sub_search, text="Search", command=self.start_search)
        self.search_button.pack(fill="both", pady=10, padx= 10)

        ttk.Label(self.sub_search, text="Set Limit Per Search").pack(fill="both", pady=10, padx= 10)

        self.current_limit = tk.StringVar(value=100)
        self.spinb_lim = ttk.Spinbox(self.sub_search,from_=0,to=50000,textvariable=self.current_limit) 
        self.spinb_lim.pack(fill="both", pady=10, padx= 10)

        self.apply_filter = tk.IntVar(value=1)
        self.apply_filter_box = ttk.Checkbutton(self.sub_search, text="Apply Filter", variable=self.apply_filter)
        self.apply_filter_box.pack(fill="both", pady=10, padx= 10)

        # * Configure the window size and position
        # self.master.attributes('-fullscreen', True)
        # width= self.master.winfo_screenwidth()
        # height= self.master.winfo_screenheight()
        # self.master.geometry("%dx%d" % (width, height))

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
            self.plot_preview(self.g1f, self.df, row_index=selection[0], nutrient_indices=[25, 26, 35, 17], g_type='bar')
            self.plot_preview(self.g2f, self.df, row_index=selection[0], nutrient_indices=[25, 26, 35, 17], g_type='pie')
            self.popup_plot.configure(state=tk.NORMAL)
            self.plotall.configure(state=tk.NORMAL)

    # SEARCH FUNC

    def search_callback(self, *args):
        pass

    def start_search(self):
        # Create a new thread to execute the search function
        search_thread = threading.Thread(target=self.search)
        search_thread.start()
    
    def search(self):
        countries = []
        categories_both = None
        column_filters = {}
        if self.apply_filter.get() == 1:
            if self.country_var.get() == "Any":
                countries = None
            else:
                countries.append((self.country_var.get()))

            if self.calories_var != None:
                cqtext = f"{self.calories_var_op.get()}{self.calories_var.get()}"
                column_filters[16] = cqtext
            if self.protein_var != None:
                pqtext = f"{self.protein_var_op.get()}{self.protein_var.get()}"
                column_filters[35] = pqtext
            if self.carbo_var != None:
                ccqtext = f"{self.carbo_var_op.get()}{self.carbo_var.get()}"
                column_filters[25] = ccqtext
            if self.fat_var != None:
                fqtext = f"{self.fat_var_op.get()}{self.fat_var.get()}"
                column_filters[17] = fqtext

            c = self.snack_var.get()+self.beverages_var.get()+self.plant_based_var.get()+self.organic_var.get()
            if (c != 0) or (self.entry_own_var.get() != None):
                categories_both = []
                if self.snack_var.get() == 1:
                    categories_both.append('snack')
                if self.beverages_var.get() == 1:
                    categories_both.append('beverage')
                if self.plant_based_var.get() == 1:
                    categories_both.append('plant')
                if self.organic_var.get() == 1:
                    categories_both.append('organic')
                if self.entry_own_var.get() != None:
                    categories_both.append(self.entry_own_var.get())

            results = self.food_search.search(self.search_var.get(), countries=countries, column_filters=column_filters, categories_both=categories_both, limit=int(self.spinb_lim.get()))
        else:
            results = self.food_search.search(self.search_var.get(), limit=int(self.spinb_lim.get()))
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
        self.ind = 1
        self.gmode = 1
        self.p = plotter()
        self.p.nutrient_plotter(self.df, self.__curr_index, [17,25, 32, 26, 18, 19, 38, 36, 23, 24], 'barpie')

    # Descriptive

    def show_des_stat(self):
        self.d = Descriptive(self.df[['product_name', 'carbohydrates_100g','sugars_100g','energy-kcal_100g','fat_100g','proteins_100g']])
        self.d.show_statistics()
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
