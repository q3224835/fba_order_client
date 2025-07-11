import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os
from pkg.common.encryption import Encryption
from pkg.pages.mainpage import MainApp
import sys

class LoginApp:
    
    # 创建窗口（此时主题已预加载）
    def __init__(self):
        self.root = ttk.Window(
            themename="minty",
            title="系统登录",
            size=(400, 550),
            resizable=(False, False)
        )
        self.root.withdraw()  # 先隐藏
        
        # 创建UI
        self.create_widgets()
        
        # 最终显示
        self.root.position_center()
        self.root.deiconify()
        
    def create_widgets(self):
        """创建登录界面组件"""
        # 顶部LOGO区域
        logo_frame = ttk.Frame(self.root)
        logo_frame.pack(pady=40)
        
        # 这里可以替换为你的LOGO图片
        ttk.Label(
            logo_frame, 
            text="🔒",  # 或用 ttk.Label(image=logo_image)
            font=("Helvetica", 48),
            bootstyle="primary"
        ).pack()
        
        ttk.Label(
            logo_frame, 
            text="欢迎登录", 
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=10)
        
        # 登录表单区域
        form_frame = ttk.Frame(self.root)
        form_frame.pack(padx=40, pady=10, fill=tk.X)
        
        # 用户名输入
        ttk.Label(form_frame, text="用户名", bootstyle="primary").pack(anchor=tk.W, pady=(5, 0))
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.pack(fill=tk.X, pady=5)
        self.username_entry.focus()  # 自动聚焦

        # 密码输入
        ttk.Label(form_frame, text="密码", bootstyle="primary").pack(anchor=tk.W, pady=(10, 0))
        self.password_entry = ttk.Entry(form_frame, show="•")  # 密码隐藏符号
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # 记住我选项
        self.remember_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            form_frame, 
            text="记住我",
            variable=self.remember_var,
            bootstyle="primary-round-toggle"
        ).pack(anchor=tk.W, pady=10)
        
        # 登录按钮
        login_btn = ttk.Button(
            self.root,
            text="登 录",
            command=self.on_login,
            bootstyle=(OUTLINE, SUCCESS),
            width=20
        )
        login_btn.pack(pady=5)

        ttk.Button(
            self.root,
            text="快速登录",
            bootstyle=(LINK, INVERSE),
            command=self.show_quick_login_dialog
        ).pack(padx=20)
        
        # 底部版权信息
        ttk.Label(
            self.root, 
            text="© 2025 世纪众云 | v1.0.0",
            font=("Helvetica", 8),
            bootstyle="secondary"
        ).pack(side=tk.BOTTOM, pady=10)

        # 绑定回车键登录
        self.root.bind("<Return>", lambda e: self.on_login())
    
    def on_login(self):
        """登录按钮事件处理"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("提示", "用户名和密码不能为空！")
            return
    
        # 模拟登录验证
        if username and password:
            if self.remember_var.get() == True:
                self.save_login_info(username, Encryption.bcrypt_hash(password))
            messagebox.showinfo("成功", f"欢迎回来，{username}！")
            self.load_mainapp_page(username,password)
        else:
            messagebox.showerror("失败", "用户名或密码错误")
            self.password_entry.delete(0, tk.END)
    
    def load_mainapp_page(self, username, password):
        # 隐藏登录窗口而不是销毁
        self.root.withdraw()
        
        # # 创建主界面
        main_window = ttk.Window(themename="simplex")
        main_window.title(f"管理后台 - {username}")
        main_window.state("zoomed")
        self.main_app = MainApp(main_window, username)
        self.main_app.pack(fill='both', expand=True)
        

        # 设置主窗口关闭时的回调
        main_window.protocol("WM_DELETE_WINDOW", self.on_main_window_close)
        main_window.mainloop()

    def on_main_window_close(self):
        """主窗口关闭时的处理"""
        sys.exit()
        # main_app.root.destroy()
        
        # if main_app.root.winfo_exists():
        #     main_app.root.destroy()
        
        # # 重新显示登录窗口
        # if self.root.winfo_exists():
        #     self.root.deiconify()

    # 登录成功后保存登录信息
    def save_login_info(self, username, password):
        try:
            # 如果文件不存在或为空，创建新数据
            if not os.path.exists("login_config.json") or os.path.getsize("login_config.json") == 0:
                data = [{"username": username, "password": password}]
                with open("login_config.json", "w") as file:
                    json.dump(data, file, indent=4)
            else:
                # 先读取现有数据
                with open("login_config.json", "r") as file:
                    data = json.load(file)
                
                # 确保data是列表
                if not isinstance(data, list):
                    data = [data]  # 如果不是列表，转换为列表

                exists = any(
                    entry["username"] == username
                    for entry in data
                )

                if not exists:
                    # 写入更新后的数据
                    with open("login_config.json", "w") as file:
                        # 添加新数据
                        data.append({"username": username, "password": password})
                        json.dump(data, file, indent=4)
                else:
                    with open("login_config.json", "w") as file:
                        for entry in data:
                            if entry["username"] == username:
                                entry["password"] = password
                        json.dump(data, file, indent=4)
    
        except FileNotFoundError:
            messagebox.showerror("系统异常",f"未找到配置文件: login_config.json")
        except json.JSONDecodeError:
            messagebox.showerror("系统异常",f"配置文件 login_config.json 格式错误")
        except Exception as e:
            messagebox.showerror("系统异常",f"发生未知错误: {str(e)}")

    # 加载保存的登录人选择界面
    def show_quick_login_dialog(self):
        """显示快速登录选择对话框"""
        # 获取保存的用户列表
        saved_users = self.get_saved_users()
        
        if not saved_users:
            messagebox.showinfo("提示", "没有保存的登录记录")
            return
        
        # 创建选择对话框
        dialog = ttk.Toplevel(self.root)
        dialog.title("选择用户")
        dialog.transient(self.root)  # 设为父窗口的子窗口
        dialog.grab_set()  # 模态对话框
        
        # 设置对话框大小和位置
        dialog_width = 300
        dialog_height = 300
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # 用户列表框架
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建Treeview显示用户列表
        columns = ("username",)
        self.user_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            bootstyle="primary",
            height=8
        )
        
        # 设置列
        self.user_tree.heading("username", text="已保存用户", anchor=tk.W)
        self.user_tree.column("username", width=250, anchor=tk.W)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.user_tree.yview
        )
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充用户数据
        for user in saved_users:
            self.user_tree.insert("", tk.END, values=(user["username"],))
        
        # 按钮框架
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 选择按钮
        select_btn = ttk.Button(
            btn_frame,
            text="选择并登录",
            command=lambda: self.on_user_selected(dialog),
            bootstyle=(OUTLINE, SUCCESS),
            width=12
        )
        select_btn.pack(side=tk.LEFT, padx=5)
        
        # 取消按钮
        cancel_btn = ttk.Button(
            btn_frame,
            text="取消",
            command=dialog.destroy,
            bootstyle=(OUTLINE, SECONDARY),
            width=12
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # 绑定双击事件
        self.user_tree.bind("<Double-1>", lambda e: self.on_user_selected(dialog))

    # 选择保存的登录人事件
    def on_user_selected(self, dialog):
        """用户选择后的处理"""
        selected_item = self.user_tree.focus()
        if not selected_item:
            return
        
        # 获取选中的用户名
        username = self.user_tree.item(selected_item)["values"][0]
        
        # 查找对应的用户数据
        saved_users = self.get_saved_users()
        selected_user = next((user for user in saved_users if user["username"] == username), None)
        
        if selected_user:
            username = selected_user["username"]
            password = selected_user["password"]
            if not username or not password:
                messagebox.showwarning("提示", "用户名和密码不能为空！")
                return
        
            # 模拟登录验证
            if username and password:
                messagebox.showinfo("成功", f"欢迎回来，{username}！")
                self.load_mainapp_page(username,password)
            else:
                messagebox.showerror("失败", "用户名或密码错误")
                self.password_entry.delete(0, tk.END)
    
    # 获取所有保存的用户
    def get_saved_users(self):
        """获取所有保存的用户"""
        try:
            if os.path.exists("login_config.json") and os.path.getsize("login_config.json") > 0:
                with open("login_config.json", "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    return [data] if data else []
        except:
            return []
        return []
        
    def run(self):
        self.root.mainloop()