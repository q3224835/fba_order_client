import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle  # 导入ThemedStyle

class LoginPage(tk.Frame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.parent = parent
        self.login_callback = login_callback
        
        # 创建ThemedStyle实例并设置主题
        self.style = ThemedStyle(self)
        # self.style.set_theme("arc")
        # self.style.set_theme("equilux")
        # self.style.set_theme("clearlooks")
        # self.style.set_theme("plastik") # 默认
        # self.style.set_theme("radiance")
        self.style.set_theme("ubuntu") # 默认2
        # self.style.set_theme("winxpblue")
        # self.style.set_theme("scidblue")
        
        # 配置自定义样式
        self.style.configure('Title.TLabel', font=('SimHei', 20, 'bold'))
        self.style.configure('TLabel', font=('SimHei', 12))
        self.style.configure('TButton', font=('SimHei', 12))
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 标题 - 使用ttk.Label以应用主题
        title_label = ttk.Label(
            self, 
            text="用户登录", 
            style='Title.TLabel'
        )
        title_label.pack(pady=30)
        
        # 用户名框架
        username_frame = ttk.Frame(self)
        username_frame.pack(fill=tk.X, padx=50, pady=10)
        
        username_label = ttk.Label(
            username_frame, 
            text="用户名:", 
            width=8
        )
        username_label.pack(side=tk.LEFT, padx=5)
        
        self.username_entry = ttk.Entry(
            username_frame, 
            width=50
        )
        self.username_entry.pack(side=tk.LEFT, padx=5)
        self.username_entry.focus()
        
        # 密码框架
        password_frame = ttk.Frame(self)
        password_frame.pack(fill=tk.X, padx=50, pady=10)
        
        password_label = ttk.Label(
            password_frame, 
            text="密码:", 
            width=8
        )
        password_label.pack(side=tk.LEFT, padx=5)
        
        self.password_entry = ttk.Entry(
            password_frame, 
            width=50,
            show="*"
        )
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=30, pady=30)
        
        login_button = ttk.Button(
            button_frame, 
            text="登录", 
            command=self.on_login,
            width=10
        )
        login_button.pack(side=tk.LEFT, padx=35)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="取消", 
            command=self.parent.destroy,
            width=10
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.username_entry.bind("<Return>", lambda event: self.on_login())
        self.password_entry.bind("<Return>", lambda event: self.on_login())
    
    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("登录失败", "用户名和密码不能为空!")
            return

        # 模拟验证
        if username == "admin" and password == "admin":
            messagebox.showinfo("登录成功", f"欢迎回来，{username}!")
            self.login_callback(username)
        else:
            messagebox.showerror("登录失败", "用户名或密码错误!")

