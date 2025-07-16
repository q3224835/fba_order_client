import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
class Checkbox_Renderer(ttk.Frame):
    """自定义复选框单元格"""
    def __init__(self, master, value=False, command=None):
        super().__init__(master)
        self.var = ttk.BooleanVar(value=value)
        self.checkbox = ttk.Checkbutton(
            self, 
            variable=self.var, 
            command=lambda: command(self.var.get()) if command else None
        )
        self.checkbox.pack(fill=BOTH, expand=True, padx=5, pady=2)