# orderlist.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pkg.pages.widgets.table_view import TableView
from pkg.pages.widgets.button_renderer import ButtonRenderer
import time

coldata = [{"text": "订单号","anchor": "w"},
           {"text": "创建时间","anchor": "w"},
           {"text": "揽收仓库","anchor": "w"},
           {"text": "客户备注","anchor": "w"},
           {"text": "承运商","anchor": "w"},
           {"text": "收件人","anchor": "w"},
           {"text": "发件人","anchor": "w"},
           {"text": "操作","anchor": "w"}]
rowdata = [
    ["2023100001","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100002","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100003","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100004","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100005","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100006","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100007","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100008","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100009","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
    ["2023100010","2023-10-01 10:00:00","上海仓库","客户备注","中通","收件人","发件人"],
]

class OrderList(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ttk.BOTH, expand=True)

        # 表格控件
        self.table = TableView(self,coldata=coldata,rowdata=rowdata)  # 可以改为 "pod1" 或其他类型
        self.table.pack(fill=ttk.BOTH, expand=True, padx=10, pady=10)

        # 操作按钮区域
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="新增", bootstyle="success", command=self.add_order).pack(side=ttk.LEFT, padx=5)
        ttk.Button(btn_frame, text="刷新", bootstyle="info", command=self.refresh_orders).pack(side=ttk.LEFT, padx=5)

    def add_order(self):
        """模拟新增一行订单数据"""
        new_row = [f"new-order-{int(time.time())}", "2/2", "Running", "0", "1h", "192.168.1.1", "node-1", "", ""]
        self.table.append_row(new_row)

    def refresh_orders(self):
        """刷新当前 Pod 类型的数据"""
        self.table.refresh_data()

    def delete_order(self, row_id):
        """删除指定行"""
        index = self.table.table.get_row_index(row_id)
        self.table.delete_row(index)

    def edit_order(self, row_id):
        """模拟编辑某行数据"""
        index = self.table.table.get_row_index(row_id)
        old_values = self.table.table.get_row_values(row_id)
        new_values = list(old_values)
        new_values[0] = f"edited-{new_values[0]}"
        self.table.update_row(index, new_values)