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
        current_time = time.localtime()
        self.parent.title(
            f"FBA管理后台    {username}     "
            f"{current_time.tm_year}年{current_time.tm_mon}月{current_time.tm_mday}日 "
            f"{current_time.tm_hour}时{current_time.tm_min}分{current_time.tm_sec}秒"
        )
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
        self.notebook = ClosableNotebook(self)
        # ToolTip(nb, text="笔记本组件", bootstyle=(PRIMARY, INVERSE))
        self.notebook.pack(side=LEFT, padx=0, pady=0, expand=YES, fill=BOTH)
        nb_text = "欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页欢迎页"
        home_page = ttk.Label(self.notebook, text=nb_text)
        self.notebook.add_tab(home_page, "主页", closable=False)
    
    def new_tabs_page(self,tab_name,page):
        for i in self.notebook.tabs(): 
            if self.notebook.tab(i, "text") == tab_name:
                # existing_page = self.notebook.nametowidget(i)
                self.notebook.select(i)
                return
        
        self.notebook.add_tab(page, title=tab_name)
        self.notebook.select(page)  

class ClosableNotebook(ttk.Notebook):
    """带关闭按钮的Notebook组件"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master,** kwargs)
        self.closable_tabs = set()  # 存储可关闭标签页的标识
        self.bind("<<NotebookTabChanged>>", self._update_tab_buttons)
        # 绑定右键事件，注意这里使用一个通用绑定而非按索引绑定
        self.bind("<Button-3>", self._show_close_menu)
        
    def add_tab(self, frame, title, closable=True):
        """添加新标签页"""
        self.add(frame, text=title)
        tab_index = self.index("end") - 1
        tab_id = self.tabs()[tab_index]
        
        # 记录可关闭的标签页
        if closable:
            self.closable_tabs.add(tab_id)
        
        return frame
    
    def close_tab(self, frame=None, index=None):
        """关闭指定标签页"""
        if self.index("end") <= 1:
            return
            
        if frame:
            index = self.index(frame)
        elif index is None:
            index = self.index("current")
            
        tab_id = self.tabs()[index]
        # 只允许关闭标记为可关闭的标签页
        if tab_id in self.closable_tabs:
            frame_to_remove = self.nametowidget(tab_id)
            self.forget(index)
            frame_to_remove.destroy()
            self.closable_tabs.discard(tab_id)  # 从集合中移除
    
    def _show_close_menu(self, event):
        """显示关闭右键菜单，仅对可关闭标签有效"""
        try:
            index = self.index(f"@{event.x},{event.y}")
            tab_id = self.tabs()[index]
            
            # 检查当前标签是否可关闭
            if tab_id in self.closable_tabs:
                close_menu = ttk.Menu(self, tearoff=0)
                close_menu.add_command(
                    label="上一页",
                    command=lambda: self.prev_page()
                )
                close_menu.add_command(
                    label="下一页",
                    command=lambda : self.next_page()
                )
                close_menu.add_command(
                    label="关闭",
                    command=lambda i=index: self.close_tab(index=i)
                )
                close_menu.post(event.x_root, event.y_root)
        except:
            return
    
    def prev_page(self):
        """上一页功能"""
        current_index = self.index("current")
        if current_index > 0:
            self.select(current_index - 1)

    def next_page(self):
        """下一页功能"""
        current_index = self.index("current")
        if current_index < self.index("end") - 1:
            self.select(current_index + 1)

    def _update_tab_buttons(self, event=None):
        """更新标签页按钮状态"""
        pass