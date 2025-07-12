import ttkbootstrap as ttk
from tkinter import Frame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import *
from ttkbootstrap.dialogs import Messagebox
from order.orderlist import OrderList

class MainPage(ttk.Window):
    def __init__(self):
        super().__init__()
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        font = ("微软雅黑", 12)
        self.menu = ttk.Menu(self, tearoff=0)
        self.theme_menu = ttk.Menu(font=font)
        colors = self.style.colors
        self.theme_menu.add_cascade(label="订单管理", menu=self.menu)
        self.menu.add_command(label="订单列表",command=lambda: self.new_tabs_page(tab_name="订单列表",page=OrderList(
            self.notebook,
            colors=colors
        )))

        self.configure(menu=self.theme_menu)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        # ToolTip(nb, text="笔记本组件", bootstyle=(PRIMARY, INVERSE))
        self.notebook.pack(side=LEFT, padx=(10, 0), pady=10, expand=YES, fill=BOTH)
        nb_text = (
            "欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页"
        )
        self.notebook.add(ttk.Label(self.notebook, text=nb_text), text="主页", sticky=NW)
    
    def new_tabs_page(self,tab_name,page):
        for i in self.notebook.tabs(): 
            if self.notebook.tab(i, "text") == tab_name:
                self.notebook.select(i)
                return
        self.notebook.add(page, text = tab_name)
        self.notebook.select(page)

if __name__ == "__main__":
    main_page = MainPage()
    main_page.state("zoomed")
    main_page.mainloop()
    