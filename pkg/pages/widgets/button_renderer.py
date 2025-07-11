# renderers.py

import ttkbootstrap as ttk
from tkinter import Frame


class ButtonRenderer:
    def __init__(self, tableview, column, callback):
        self.tableview = tableview
        self.column = column
        self.callback = callback

    def render(self, tv_row, tv_col, widget=None, width=None):
        """渲染按钮到指定单元格"""
        if widget is None:
            widget = Frame(self.tableview)

        row_iid = tv_row.iid
        btn_frame = Frame(widget)
        btn_frame.pack(fill="both", expand=True)

        edit_btn = ttk.Button(
            btn_frame,
            text="编辑",
            bootstyle="warning-outline",
            width=6,
            command=lambda: self.callback("edit", row_iid)
        )
        edit_btn.pack(side="left", padx=2)

        del_btn = ttk.Button(
            btn_frame,
            text="删除",
            bootstyle="danger-outline",
            width=6,
            command=lambda: self.callback("delete", row_iid)
        )
        del_btn.pack(side="left", padx=2)

        return widget