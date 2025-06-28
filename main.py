import tkinter as tk
from page.login import LoginPage
from ttkthemes import ThemedTk  # 导入ThemedTk
from page.mainpage import MainPage

class App(ThemedTk):  # 使用ThemedTk代替tk.Tk
    def __init__(self):
        super().__init__()
        self.title("FBA-登录")

        # 设置主题
        # self.set_theme("arc")
        # self.set_theme("equilux")
        # self.set_theme("clearlooks")
        # self.set_theme("plastik")  # 默认
        # self.set_theme("radiance")
        self.set_theme("ubuntu") # 默认2    
        # self.set_theme("winxpblue")
        # self.set_theme("scidblue")

        # self.geometry("400x300")
        # 设置窗口初始大小
        self.login_width, self.login_height = 400, 300
        self.center_window(self.login_width,self.login_height)
        self.resizable(False, False)        
        
        # 创建登录页面
        self.current_page = LoginPage(self,self.on_login_success)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def center_window(self, width, height):
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 3
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_login_success(self, username):
        self.current_page.destroy()
        self.title("FBA-主页")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.login_width, self.login_height = int(screen_width * 0.85), int(screen_height * 0.85)
        self.center_window(self.login_width, self.login_height)
        self.resizable(True, True)
        self.current_page = MainPage(self, username, self.on_logout)
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def on_logout(self):
        self.current_page.destroy()
        self.title("FBA-登录")
        self.state('normal')
        self.login_width, self.login_height = 400, 300
        self.center_window(self.login_width,self.login_height)
        self.resizable(False, False)
        
        self.current_page = LoginPage(self,self.on_login_success)
        self.current_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()    

# 创建主窗口
# root = Tk()
# root.title("TTK Themes 示例")

# 创建并设置主题
# style = ThemedStyle(root)
# style.set_theme("arc") 
# style.set_theme("equilux")
# style.set_theme("clearlooks")
# style.set_theme("plastik")
# style.set_theme("radiance")
# style.set_theme("ubuntu")
# style.set_theme("winxpblue")
# style.set_theme("scidblue")

# 添加一些组件
# frame = Frame(root)
# frame.pack(pady=10)

# label = Label(frame, text="欢迎使用 TTK Themes!")
# label.pack(pady=5)

# button = Button(frame, text="点击我")
# button.pack(pady=5)



# # 运行主循环
# root.mainloop()