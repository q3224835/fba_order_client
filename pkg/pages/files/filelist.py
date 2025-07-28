# orderlist.py

import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap.constants import *
from pkg.pages.widgets.table_view import TableView
import time
from pkg.common import http_get,http_post,http_upload,files_url

col_data = [
            {"text": "id", "stretch": True, "anchor": "w"},
            {"text": " 文件名", "stretch": True, "anchor": "w"},
            {"text": " 文件路径", "stretch": True, "anchor": "w"},
            {"text": " 文件大小", "stretch": True, "anchor": "w"},
            {"text": " 文件类型", "stretch": True, "anchor": "w"},
            {"text": " 文件key", "stretch": True, "anchor": "w"},
            {"text": " 上传人", "stretch": True, "anchor": "w"},
            {"text": " 上传时间", "stretch": True, "anchor": "w"}
        ]

class FileList(ttk.Frame):
    def __init__(self, master, colors):
        super().__init__(master)
        self.colors = colors
        self.row_data = []
        # self.pack(fill=ttk.BOTH, expand=True)
        self.create_widgets()
        self.bind_events()
        self.load_data()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill=BOTH, padx=10)
        search_group = ttk.Labelframe(
            master=container, text="查询", padding=(10, 5)
        )
        search_group.pack(fill=BOTH,padx=15,pady=(10,0))
        self.status_menu_val = ttk.IntVar(value=0)
        # 查询按钮区
        search_btn_frame = ttk.Frame(search_group)
        search_btn_frame.pack(pady=5,fill=X,side=TOP,anchor=E)
        status_menu_text = ["全部",".xls",".xlsx",".docs",".doc",".pdf",".txt",".zip",".rar",".7z",".tar.gz",
                            ".tar",".gz",".jpg",".jpeg",".png",".gif",".bmp",".svg",".mp4",".avi",".mkv",
                            ".mov",".wmv",".flv",".mp3",".wav",".aac",".ogg",".flac"]
        self.status_menu = ttk.Menu(self)
        for i, t in enumerate(status_menu_text):
            self.status_menu.add_radiobutton(label=t, 
                                             value=i,
                                             variable=self.status_menu_val,
                                             command=lambda text=t,value=i: self.enforce_exclusive(text=text,value=value))

        # 查询区
        ttk.Label(search_btn_frame, text="文件类型").pack(side=LEFT,padx=10,pady=10)
        self.status_menu_btn = ttk.Menubutton(
            master=search_btn_frame,
            bootstyle=(PRIMARY, OUTLINE),
            menu=self.status_menu,
            width=10,
            text="全部",
        )
        self.status_menu_btn.pack(side=LEFT, pady=10)

        ttk.Label(search_btn_frame, text="文件名").pack(side=LEFT,padx=10)
        s_filename = ttk.Entry(search_btn_frame,width=20)
        s_filename.pack(side=LEFT,padx=10)
        ttk.Label(search_btn_frame, text="上传日期").pack(side=LEFT,padx=10)
        start = ttk.DateEntry(search_btn_frame,width=20)
        start.pack(side=LEFT,padx=10)
        ttk.Label(search_btn_frame, text="--").pack(side=LEFT)
        end = ttk.DateEntry(search_btn_frame,width=20)
        end.pack(side=LEFT,padx=10)
        ttk.Button(
            search_btn_frame, 
            text="查询", 
            bootstyle="success",
            command=self.load_data
        ).pack(side=LEFT, padx=10)


        # 操作按钮区
        option_group = ttk.Labelframe(
            master=container, text="操作按钮", padding=(10, 5)
        )
        option_group.pack(fill=BOTH,padx=15,pady=10)
        option_btn_frame = ttk.Frame(option_group)
        option_btn_frame.pack(pady=5,fill=X,side=LEFT,anchor=E)

        ttk.Button(
            option_btn_frame, 
            text="上传文件", 
            bootstyle="success",
            command=self.add_data
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            option_btn_frame, 
            text="刷新数据", 
            bootstyle="info",
            command=self.load_data
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            option_btn_frame, 
            text="批量删除", 
            bootstyle="danger",
            command=self.batch_del_data
        ).pack(side=LEFT, padx=5)

        self.menu = ttk.Menu(self, tearoff=0)
        self.menu.add_command(label="删除文件",command=self.delete_data)
        self.menu.add_command(label="下载文件",command=self.edit_data)

        # 表格控件（父容器为当前OrderList Frame）
        self.table = TableView(
            master=self,  # 关键：表格的父容器是当前OrderList Frame
            colors=self.colors,
            coldata=col_data,
            rowdata=self.row_data,
            pagesize=50
        )
        self.table.pack(fill=BOTH, expand=YES, padx=10, pady=0)

    def add_data(self):
        """新增一行订单数据（注意与表格列数匹配）"""
        root = tk.Tk()
        root.withdraw() 
        file_path = filedialog.askopenfilename(title="选择要上传的文件", filetypes=[("所有文件", "*.*")])
        root.destroy()
        try:
            with open(file_path, 'rb') as file_stream:
                response = http_upload(
                    url=f'{files_url}/upload',
                    file_stream=file_stream,
                    file_name=file_path.split('/')[-1],
                    timeout=60
                )
                if response.get("code") == 200:
                    file_data = response.get('data', {})
                    self.row_data.append((
                        file_data.get("id"),
                        file_data.get("fileName"),
                        file_data.get("filePath"),
                        file_data.get("fileSize"),
                        file_data.get("fileType"),
                        file_data.get("fileKey"),
                        file_data.get("createdUserName"),
                        file_data.get("createdTime"),
                    ))
                    self.table.refresh_data(self.row_data)
        except Exception as e:
            raise Exception(f"File upload failed: {e}")

    def delete_data(self):
        """删除指定行"""
        # 调用接口删除行
        self.table.table.delete_row(self.current_index)

    def edit_data(self):
        """模拟编辑某行数据"""
        self.current_value["values"][0] = "1111111111"
        tuple_data = tuple(self.current_value["values"])
        self.table.table.view.item(self.current_rowid,values=tuple_data)
    
    def detail_data(self):
        """模拟查看某行数据详情"""
        # 这里可以弹出一个新窗口显示详细信息
        print(f"查看订单详情: {self.current_value['values']}")

    def batch_del_data(self):
        """批量删除数据"""
        print(f"批量删除数据: {self.current_value['values']}")

    def import_data(self):
        """导入数据"""
        print("导入订单数据")

    def export_data(self):
        """导出数据"""
        print("导出订单数据")

    def bind_events(self):
        """绑定表格事件（如右键菜单）"""
        self.table.table.view.bind("<Button-3>", self.show_context_menu)
        self.table.table.view.bind("<Button-2>", self.show_context_menu)
        self.table.table.view.bind("<Double-Button-1>", self.double_click_handler)

    def show_context_menu(self, event):
        """显示右键菜单并记录选中行"""
        # 获取点击的行
        rowid = self.table.table.view.identify_row(event.y)
        if rowid:
            self.table.table.view.selection_remove(*self.table.table.view.selection())
            self.table.table.view.selection_add(rowid)
            self.current_rowid = rowid  # 保存当前行ID
            self.current_index = self.table.table.view.index(rowid)  # 保存当前行索引
            self.current_value = self.table.table.view.item(rowid)  # 保存当前行数据
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
                self.menu.grab_release()
            finally:
                self.menu.grab_release()

    def double_click_handler(self, event):
        """双击行时的处理函数"""
        rowid = self.table.table.view.identify_row(event.y)
        if rowid:
            self.table.table.view.selection_remove(*self.table.table.view.selection())
            self.table.table.view.selection_add(rowid)
            self.current_rowid = rowid
            self.current_index = self.table.table.view.index(rowid)
            self.current_value = self.table.table.view.item(rowid)
            self.detail_data()

    def enforce_exclusive(self,text,value):
        self.status_menu_btn.configure(text=text)

    def load_data(self):
        """加载初始数据"""
        self.row_data = []
        params = {
            "page": 1,
            "page_size": 50,
            "file_type": "",
            "file_name": ""
        }
        response  = http_get(url=f"{files_url}/list", params=params,timeout=30)
        if response.get("code") == 200:
            file_list = response.get('data', {}).get('fileList', [])
            for item in file_list:
                self.row_data.append((
                    item.get("id"),
                    item.get("fileName"),
                    item.get("filePath"),
                    item.get("fileSize"),
                    item.get("fileType"),
                    item.get("fileKey"),
                    item.get("createdUserName"),
                    item.get("createdTime"),
                ))
        self.table.refresh_data(self.row_data)