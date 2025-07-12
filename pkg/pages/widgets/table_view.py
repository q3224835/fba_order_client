# table_view.py

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import time

class TableView(ttk.Frame):
    def __init__(self, master, colors, coldata, rowdata,pagesize=10):
        super().__init__(master)

        self.coldata = coldata
        self.rowdata = rowdata
        
        # 初始化表格
        self.table = Tableview(
            master     = self,
            coldata    = self.coldata,
            rowdata    = self.rowdata,
            pagesize   = pagesize,
            height     = 15,
            autofit    = True,
            paginated  = True,
            # searchable = True,
            bootstyle  = SUCCESS,
            stripecolor = (colors.light, None)
        )
        self.table.pack(fill = BOTH, expand = YES, padx = 15)
        self._set_alignment()
        self.menu = ttk.Menu(self, tearoff=0)
        self.menu.add_command(label="删除", command=lambda:self.delete_row)
        self.menu.add_command(label="编辑", command=lambda:self.update_row)
        self.bind_events()

    def _set_alignment(self):
        """设置列和表头对齐方式"""
        tree = self.table.view
        for col_idx, col in enumerate(self.coldata):
            col_id = tree["columns"][col_idx]
            tree.column(col_id, anchor=col.get("anchor", "w"))  # 内容对齐
            tree.heading(col_id, text=col["text"], anchor=col.get("anchor", "w"))  # 表头对齐

    def refresh_data(self, rowdata):
        """刷新表格数据（可指定新的 pod_type）"""
        self.table.delete_rows()
        self.rowdata = rowdata
        self.table.build_table_data(self.coldata, self.rowdata)

    def append_row(self, row_data):
        """追加一行数据"""
        self.table.insert_row(index='end', values=row_data)
        self.table.reset_table()

    def delete_row(self):
        """删除指定索引的一行"""
        try:
            self.table.delete_row(self.current_index)
        except IndexError:
            print(f"Index {self.selected_index} out of range for deletion.")

    def update_row(self):
        """更新指定索引的一行数据"""
        try:
            self.table.update_row_data(self.current_index, self.current_value)
        except IndexError:
            print(f"Index {self.selected_index} out of range for update.")

    def bind_events(self):
        """绑定表格事件（如右键菜单）"""
        self.table.view.bind("<Button-3>", self.show_context_menu)
        self.table.view.bind("<Button-2>", self.show_context_menu)

    def show_context_menu(self, event):
        """显示右键菜单并记录选中行"""
        # 获取点击的行
        rowid = self.table.view.identify_row(event.y)
        if rowid:
            self.table.view.selection_remove(*self.table.view.selection())
            self.table.view.selection_add(rowid)
            self.current_index = self.table.view.index(rowid)  # 保存当前行索引
            self.current_value = self.table.view.item(rowid)["values"]  # 保存当前行数据
            self.current_value[0] = self.current_value[0] + "(修改后)"
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
                self.menu.grab_release()
            finally:
                self.menu.grab_release()