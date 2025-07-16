import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview, CellRenderer
from ttkbootstrap.constants import *

class Button_Renderer(CellRenderer):
    """自定义按钮单元格"""
    def __init__(self, master, text="Button", command=None):
        super().__init__(master)
        self.button = ttk.Button(
            self, 
            text=text, 
            bootstyle=PRIMARY,
            command=command
        )
        self.button.pack(fill=BOTH, expand=True, padx=5, pady=2)
        self.button.pack(side=LEFT, padx=5, pady=2)
