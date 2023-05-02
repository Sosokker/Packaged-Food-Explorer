import tkinter as tk
from app.controller import Controller
from app.model import Model
from app.view import View

if __name__ == '__main__':
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    root.mainloop()
