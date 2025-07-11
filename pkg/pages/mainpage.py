import copy

import ttkbootstrap as ttk
from ttkbootstrap.themes.standard import STANDARD_THEMES
from ttkbootstrap import Style
from pkg.pages.homepage import HomePage
from pkg.pages.order.orderlist import OrderList

# from ttkb_pprof import TtkbPprof


class MainApp(ttk.Frame):
    def __init__(self,master_window,username):
        super().__init__(master_window)
        self.username = username
        self.master_window = master_window
        self.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True,padx=10,pady=10)
        self.load_home_page()
        self.create_menubar()
        # TtkbPprof(self.app)

    def create_menubar(self):
        menubar = ttk.Menu(self)
        
        file_menu = ttk.Menu(menubar)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="复制",command=print('复制'))
        file_menu.add_command(label="粘贴",command=print('粘贴'))

        order_menu = ttk.Menu(menubar)
        menubar.add_cascade(label="订单管理", menu=order_menu)
        order_menu.add_command(label="订单列表", command=lambda:self.open_new_tab("订单列表",OrderList))

        theme_menu = ttk.Menu(menubar)  # 新增一个主题菜单
        menubar.add_cascade(label="主题", menu=theme_menu)

        theme_menu_sub = ttk.Menu(theme_menu)
        theme_menu.add_cascade(label="切换主题", menu=theme_menu_sub, underline=0)
        th_list = list(STANDARD_THEMES.keys())
        for i in range(len(th_list)):  # 遍历所有主题
            print("th: ", th_list[i])
            theme_menu_sub.add_command(label=th_list[i], command=lambda th=th_list[i]: self.master_window.style.theme_use(th))

        about_menu = ttk.Menu(menubar)  # 新增一个关于菜单
        menubar.add_cascade(label="关于", menu=about_menu)

        menubar.add_command(label="退出", command=self.quit)

        self.master_window.config(menu=menubar)

    def load_home_page(self):
        """加载主页面"""
        home_page = HomePage(self.notebook)
        home_page.pack(fill="both", expand=True)
        self.notebook.add(home_page, text="首页")

    def open_new_tab(self,tab_name,page):
        """在Tabs中新增一个tab页面"""
        for index in range(self.notebook.index("end")):
            if self.notebook.tab(index, "text") == tab_name:
                self.notebook.select(index)
                return
        
        # 创建新页面内容
        if page is None:
            # 默认空白页面
            new_frame = ttk.Frame(self.notebook)
            new_frame.pack(fill="both", expand=True)
            label = ttk.Label(new_frame, text=f"{tab_name} 内容区域", font=("Arial", 18))
            label.pack(pady=50)
        else:
            # 使用传入的类初始化页面控件
            new_frame = page(self.notebook)

        self.notebook.add(new_frame, text=tab_name)
        self.notebook.select(self.notebook.index("end") - 1) 