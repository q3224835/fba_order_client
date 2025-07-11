import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

class HomePage(ttk.Frame):
    """欢迎页面"""
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="欢迎使用系统管理平台", font=("Arial", 24), bootstyle="success")
        label.pack(pady=20)

        desc = ttk.Label(self, text="请从上方菜单选择功能模块，打开新页面。", font=("Arial", 14))
        desc.pack(pady=10)