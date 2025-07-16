# orderlist.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from widgets.table_view import TableView
import time

class OrderList(ttk.Frame):
    def __init__(self, master, colors):
        super().__init__(master)
        self.load_data()
        self.colors = colors
        self.pack(fill=ttk.BOTH, expand=True)
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill=BOTH, padx=10)
        search_group = ttk.Labelframe(
            master=container, text="查询", padding=(10, 5)
        )
        search_group.pack(fill=BOTH,padx=15,pady=(10,0))

        # 查询按钮区
        search_btn_frame = ttk.Frame(search_group)
        search_btn_frame.pack(pady=5,fill=X,side=TOP,anchor=E)
        status_menu_text = ["全部","未提交","已提交"]
        self.status_menu = ttk.Menu(self)
        for i, t in enumerate(status_menu_text):
            self.status_menu.add_radiobutton(label=t, value=i,command=lambda text=t,value=i: self.enforce_exclusive(text=text,value=value))

        # 查询区
        ttk.Label(search_btn_frame, text="状态筛选").pack(side=LEFT,padx=10)
        self.status_menu_btn = ttk.Menubutton(
            master=search_btn_frame,
            text="全部",
            bootstyle=(PRIMARY, OUTLINE),
            menu=self.status_menu,
            width=10
        )
        self.status_menu_btn.pack(side=LEFT, pady=(0,10))

        ttk.Label(search_btn_frame, text="订单号").pack(side=LEFT,padx=10)
        s_orderno = ttk.Entry(search_btn_frame,width=20)
        s_orderno.pack(side=LEFT,padx=10)
        ttk.Label(search_btn_frame, text="订单日期").pack(side=LEFT,padx=10)
        start = ttk.DateEntry(search_btn_frame,width=20)
        start.pack(side=LEFT,padx=10)
        ttk.Label(search_btn_frame, text="--").pack(side=LEFT)
        end = ttk.DateEntry(search_btn_frame,width=20)
        end.pack(side=LEFT,padx=10)
        ttk.Button(
            search_btn_frame, 
            text="查询", 
            bootstyle="success",
            command=self.refresh_orders
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
            text="新增订单", 
            bootstyle="success",
            command=self.add_order
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            option_btn_frame, 
            text="刷新数据", 
            bootstyle="info",
            command=self.refresh_orders
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            option_btn_frame, 
            text="批量删除", 
            bootstyle="danger",
            command=self.add_order
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            option_btn_frame, 
            text="导入订单", 
            bootstyle="info",
            command=self.add_order
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            option_btn_frame, 
            text="导出订单", 
            bootstyle="info",
            command=self.add_order
        ).pack(side=LEFT, padx=5)

        self.menu = ttk.Menu(self, tearoff=0)
        self.menu.add_command(label="删除订单",command=self.delete_order)
        self.menu.add_command(label="编辑订单",command=self.edit_order)
        self.menu.add_command(label="查看详情",command=self.detail_order)
        self.menu.add_command(label="受理订单")
        self.menu.add_command(label="复制订单")
        self.menu.add_command(label="取消订单")

        # 表格控件（父容器为当前OrderList Frame）
        self.table = TableView(
            master=self,  # 关键：表格的父容器是当前OrderList Frame
            colors=self.colors,
            coldata=self.col_data,
            rowdata=self.row_data,
            pagesize=50
        )
        self.table.pack(fill=BOTH, expand=YES, padx=10, pady=0)

    def add_order(self):
        """新增一行订单数据（注意与表格列数匹配）"""
        # 新增数据需与col_data的5列对应
        new_row = [
            f"User-{int(time.time())}", 
            str(20 + int(time.time()) % 30),  # 随机年龄
            f"user{int(time.time())}@example.com",
            f"{int(time.time()) % 1000} 街道",
            f"(555) {int(time.time()) % 1000}-{int(time.time()) % 10000}"
        ]
        self.table.append_row(new_row)  # 调用TableView的追加方法

    def refresh_orders(self):
        """刷新当前 Pod 类型的数据"""
        self.table.refresh_data(self.row_data)

    def delete_order(self):
        """删除指定行"""
        # 调用接口删除行
        self.table.table.delete_row(self.current_index)

    def edit_order(self):
        """模拟编辑某行数据"""
        self.current_value["values"][0] = "1111111111"
        tuple_data = tuple(self.current_value["values"])
        self.table.table.view.item(self.current_rowid,values=tuple_data)
    
    def detail_order(self):
        """模拟查看某行数据详情"""
        # 这里可以弹出一个新窗口显示详细信息
        print(f"查看订单详情: {self.current_value['values']}")

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
            self.detail_order()

    def enforce_exclusive(self,text,value):
        print(text,value)
        self.status_menu_btn.configure(text=text)

    def load_data(self):
        """加载初始数据"""
        self.col_data = [
                    {"text": " 订单号", "stretch": True, "anchor": "w"},
                    {"text": " 客户名称", "stretch": True, "anchor": "w"},
                    {"text": " 承运商", "stretch": True, "anchor": "w"},
                    {"text": " 业务员", "stretch": True, "anchor": "w"},
                    {"text": " 客服", "stretch": True, "anchor": "w"},
                    {"text": " 重量", "stretch": True, "anchor": "w"},
                    {"text": " 体积", "stretch": True, "anchor": "w"},
                    {"text": " 件数", "stretch": True, "anchor": "w"},
                    {"text": " 货物性质", "stretch": True, "anchor": "w"},
                    {"text": " 目的地", "stretch": True, "anchor": "w"},
                    {"text": " 收件人", "stretch": True, "anchor": "w"},
                    {"text": " 发件人", "stretch": True, "anchor": "w"},
                 ]

        self.row_data = [
                ('GTF25AI0000001','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000002','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000003','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000004','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000005','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000006','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000007','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000008','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000009','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000010','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000011','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000012','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000013','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000014','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000015','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
                ('GTF25AI0000016','测试客户1','承运商1','业务员1','客服1',10.5,0.02,5,'易碎','上海','张三','李四'),
            ]