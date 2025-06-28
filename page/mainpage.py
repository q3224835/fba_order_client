import tkinter as tk
from tkinter import ttk,messagebox
from ttkthemes import ThemedStyle

class MainPage(tk.Frame):
    def __init__(self, parent, username, logout_callback):
        super().__init__(parent)
        self.logout_callback = logout_callback
        self.username = username
        # 配置主题
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")

        # 配置样式
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('SimHei', 18, 'bold'))
        self.style.configure('Content.TFrame', background='white')
        
        # 创建UI组件
        self.create_menu_bar()

    def create_menu_bar(self):
        """创建多级顶部菜单"""
        # 创建主菜单栏
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        # 定义菜单结构
        menu_structure = {
            "首页":[
                {"label":"首页","command": self.load_topmenu_page("首页","首页")},
            ],
            "订单管理": [
                {"label":"海运整柜订单","command": self.load_topmenu_page("订单管理","海运整柜订单")},
                {"label":"FBA订单","command": self.load_topmenu_page("订单管理","FBA订单")},
            ],
            "干线":[
                {"label":"空运单","command": self.load_topmenu_page("干线","空运单")},
                {"label":"海运单","command": self.load_topmenu_page("干线","海运单")},
                {"label":"提货单","command": self.load_topmenu_page("干线","提货单")},
                {"label":"批量外配单","command": self.load_topmenu_page("干线","批量外配单")},
            ],
            "客户管理":[
                {"label":"客户列表","command": self.load_topmenu_page("客户管理","客户列表")},
                {"label":"公司配置","command": self.load_topmenu_page("客户管理","公司配置")},
            ],
            "渠道管理":[
                {"label":"收货渠道","command": self.load_topmenu_page("渠道管理","收货渠道")},
                {"label":"供应渠道","command": self.load_topmenu_page("渠道管理","供应渠道")},
            ],
            "报表中心":[
                {"label":"时效分析","command": self.load_topmenu_page("报表中心","时效分析")},
                {"label":"海运配载利润","command": self.load_topmenu_page("报表中心","海运配载利润")},
                {"label":"空运配载利润","command": self.load_topmenu_page("报表中心","空运配载利润")},
                {"label":"应收统计","command": self.load_topmenu_page("报表中心","应收统计")},
                {"label":"应付统计","command": self.load_topmenu_page("报表中心","应付统计")},
                {"label":"订单收入成本利润","command": self.load_topmenu_page("报表中心","订单收入成本利润")},
                {"label":"FBA订单货量利润","command": self.load_topmenu_page("报表中心","FBA订单货量利润")},
            ],
            "财务管理":[
                {"label":"销账列表","command": self.load_topmenu_page("财务管理","销账列表")},
            ],
            "系统管理":[
                {"label":"权限列表","command": self.load_topmenu_page("系统管理","权限列表")},
            ],
            "关于":[
                {"label":"退出登录","command": self.load_topmenu_page("关于","退出登录")},
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
        self.master.bind("<Control-n>", lambda event: self.menu_new())
        self.master.bind("<Control-o>", lambda event: self.menu_open())
        self.master.bind("<Control-s>", lambda event: self.menu_save())

    def load_topmenu_page(self,name1,name2):
        if name1 == "首页" and name2 == "首页":
            messagebox.showinfo("提示", "欢迎使用")
        elif name1 == "关于":
            if name2 == "退出登录":
                self.on_logout()

    def clear_content_frame(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def on_logout(self):
        self.logout_callback()