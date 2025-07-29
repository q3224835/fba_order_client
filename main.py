from pkg.pages.login import LoginApp
import ttkbootstrap as ttk

class Main(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("用户登录")
        # self.geometry("400x550")
        self.window_width = 400  # 窗口期望的宽度
        self.window_height = 550  # 窗口期望的高度
        self.resizable(False, False)
        self.center_window(self.window_width, self.window_height)  # 调用居中函数
        self.resizable(False, False)
        LoginApp(self, self)

    def center_window(self, width, height):
        # 获取屏幕宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 计算窗口应放置的 x 和 y 坐标
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # 设置窗口的大小和位置
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = Main()
    app.mainloop()
    