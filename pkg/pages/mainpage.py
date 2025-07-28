import ttkbootstrap as ttk
from tkinter import Frame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import *
from ttkbootstrap.dialogs import Messagebox
from pkg.pages.order.orderlist import OrderList
from pkg.pages.files.filelist import FileList
import time

class MainPage(ttk.Frame):
    def __init__(self,parent,app,username):
        super().__init__(parent)
        self.parent =parent
        self.parent.title(f"FBA管理后台    {username}     {time.localtime().tm_year}年{time.localtime().tm_mon}月{time.localtime().tm_mday}日 {time.localtime().tm_hour}时{time.localtime().tm_min}分{time.localtime().tm_sec}秒")
        self.parent.state("zoomed")
        self.parent.resizable(True, True)
        self.app = app
        self.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # font = ("微软雅黑", 12)
        self.menu = ttk.Menu(self.parent, tearoff=0)
        self.order_menu = ttk.Menu(self.menu)
        colors = self.parent.style.colors
        self.menu.add_cascade(label="订单管理", menu=self.order_menu)
        self.order_menu.add_command(label="订单列表",command=lambda: self.new_tabs_page(tab_name="订单列表",page=OrderList(
            self.notebook,
            colors=colors
        )))
        self.file_menu = ttk.Menu(self.menu)
        self.menu.add_cascade(label="文件管理", menu=self.file_menu)
        self.parent.configure(menu=self.menu)
        self.file_menu.add_command(label="文件列表",command=lambda: self.new_tabs_page(tab_name="文件列表",page=FileList(
            self.notebook,
            colors=colors
        )))

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        # ToolTip(nb, text="笔记本组件", bootstyle=(PRIMARY, INVERSE))
        self.notebook.pack(side=LEFT, padx=0, pady=0, expand=YES, fill=BOTH)
        nb_text = (
            "欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页"
        )
        self.notebook.add(ttk.Label(self.notebook, text=nb_text), text="主页", sticky=NW)
    
    def new_tabs_page(self,tab_name,page):
        for i in self.notebook.tabs(): 
            if self.notebook.tab(i, "text") == tab_name:
                # existing_page = self.notebook.nametowidget(i)
                self.notebook.select(i)
                return
        
        print("new page")
        self.notebook.add(page, text = tab_name)
        self.notebook.select(page)
    