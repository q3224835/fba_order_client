import tkinter as tk
from tkinter import ttk, messagebox

class MainPage(tk.Frame):
    def __init__(self, parent, username, logout_callback):
        super().__init__(parent)
        self.logout_callback = logout_callback
        self.username = username
        
        # 配置样式
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('SimHei', 18, 'bold'))
        self.style.configure('Content.TFrame', background='white')
        
        # 创建UI组件
        self.create_menu_bar()
        self.create_content_area()
        
        # 加载默认页面
        self.load_welcome_page()

    def create_menu_bar(self):
        """创建多级顶部菜单"""
        # 创建主菜单栏
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        # 定义菜单结构
        menu_structure = {
            "首页":[
                {"label":"首页","command": self.load_welcome_page},
            ],
            "订单管理": [
                {"label":"海运整柜订单","command": lambda: self.load_order_page("海运整柜订单")},
                {"label":"FBA订单","command": lambda: self.load_order_page("FBA订单")},
            ],
            "干线":[
                {"label":"空运单","command": lambda: self.load_ticket_page("空运单")},
                {"label":"海运单","command": lambda: self.load_ticket_page("海运单")},
                {"label":"提货单","command": lambda: self.load_ticket_page("提货单")},
                {"label":"批量外配单","command": lambda: self.load_ticket_page("批量外配单")},
            ],
            "客户管理":[
                {"label":"客户列表","command": lambda: self.load_customer_page("客户列表")},
                {"label":"公司配置","command": lambda: self.load_customer_page("公司配置")},
            ],
            "渠道管理":[
                {"label":"收货渠道","command": lambda: self.load_channel_page("收货渠道")},
                {"label":"供应渠道","command": lambda: self.load_channel_page("供应渠道")},
            ],
            "报表中心":[
                {"label":"时效分析","command": lambda: self.load_report_page("时效分析")},
                {"label":"海运配载利润","command": lambda: self.load_report_page("海运配载利润")},
                {"label":"空运配载利润","command": lambda: self.load_report_page("空运配载利润")},
                {"label":"应收统计","command": lambda: self.load_report_page("应收统计")},
                {"label":"应付统计","command": lambda: self.load_report_page("应付统计")},
                {"label":"订单收入成本利润","command": lambda: self.load_report_page("订单收入成本利润")},
                {"label":"FBA订单货量利润","command": lambda: self.load_report_page("FBA订单货量利润")},
            ],
            "财务管理":[
                {"label":"销账列表","command": lambda: self.load_finace_page("销账列表")},
            ],
            "系统管理":[
                {"label":"权限列表","command": lambda: self.load_system_page("权限列表")},
            ],
            "关于":[
                {"label":"退出登录","command": lambda: self.on_logout},
            ]
        }
        
        # 构建菜单
        for menu_name, items in menu_structure.items():
            menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label=menu_name, menu=menu)
            
            for item in items:
                if item == "-":
                    menu.add_separator()
                elif "menu" in item:  # 子菜单
                    submenu = tk.Menu(menu, tearoff=0)
                    menu.add_cascade(label=item["label"], menu=submenu)
                    
                    for subitem in item["menu"]:
                        if subitem == "-":
                            submenu.add_separator()
                        else:
                            submenu.add_command(
                                label=subitem["label"],
                                command=subitem["command"],
                                accelerator=subitem.get("accelerator", "")
                            )
                else:  # 普通菜单项
                    menu.add_command(
                        label=item["label"],
                        command=item["command"],
                        accelerator=item.get("accelerator", "")
                    )
        
        # 绑定快捷键
        # self.master.bind("<Control-n>", lambda event: self.menu_new())
        # self.master.bind("<Control-o>", lambda event: self.menu_open())
        # self.master.bind("<Control-s>", lambda event: self.menu_save())

    def load_welcome_page(self):
        """加载欢迎页面"""
        self.clear_content_frame()
        
        title = ttk.Label(
            self.content_frame, 
            text=f"欢迎，{self.username}!", 
            style='Title.TLabel'
        )
        title.pack(pady=30)
        
        info = ttk.Label(
            self.content_frame, 
            text="这是应用程序的主界面。\n\n"
                 "你可以通过顶部菜单导航到不同的功能模块。",
            font=('SimHei', 12)
        )
        info.pack(pady=20)

    def create_content_area(self):
        """创建内容区域"""
        self.content_frame = ttk.Frame(self, style='Content.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_order_page(self,subpage):
        messagebox.showinfo("订单管理", subpage)
    
    def load_ticket_page(self,subpage):
        messagebox.showinfo("干线", subpage)
    
    def load_customer_page(self,subpage):
        messagebox.showinfo("客户管理", subpage)

    def load_channel_page(self,subpage):
        messagebox.showinfo("渠道管理", subpage)

    def load_report_page(self,subpage):
        messagebox.showinfo("报表中心", subpage)

    def load_finace_page(self,subpage):
        messagebox.showinfo("财务管理", subpage)

    def load_system_page(self,subpage):
        messagebox.showinfo("系统管理", subpage)

    def load_abort_page(self,subpage):
        messagebox.showinfo("关于", subpage)

    def on_logout(self):
        self.logout_callback()
    

    def clear_content_frame(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()