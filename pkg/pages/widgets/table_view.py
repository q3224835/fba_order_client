# table_view.py

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import time

class TableView(ttk.Frame):
    def __init__(self, 
                 master, 
                 colors, 
                 coldata, 
                 rowdata,
                 pagesize=10,
                 add_callback=None,
                 update_callback=None,
                 delete_callback=None,
                 detail_callback=None):
        super().__init__(master)

        self.coldata = coldata
        self.rowdata = rowdata
        self.master = master
        self.add_callback = add_callback
        self.update_callback = update_callback
        self.delete_callback = delete_callback
        self.detail_callback = detail_callback
        # 初始化表格
        self.table = Tableview(
            master     = self,
            coldata    = self.coldata,
            # rowdata    = self.rowdata,
            pagesize   = pagesize,
            height     = 15,
            autofit    = True,
            paginated  = True,
            # searchable = True,
            bootstyle  = SUCCESS,
            stripecolor = (colors.light, None),
            
        )
        self.table.pack(fill = BOTH, expand = YES, padx = 15)
        self.refresh_data(self.rowdata)

    def _set_alignment(self):
        """设置列和表头对齐方式"""
        tree = self.table.view
        for col_idx, col in enumerate(self.coldata):
            col_id = tree["columns"][col_idx]
            tree.column(col_id, anchor=col.get("anchor", "w"))  # 内容对齐
            tree.heading(col_id, text=col["text"], anchor=col.get("anchor", "w"))  # 表头对齐
        # self.table.view.tk

    def refresh_data(self, rowdata):
        """刷新表格数据（可指定新的 pod_type）"""
        self.table.delete_rows()
        self.rowdata = rowdata
        self.table.build_table_data(self.coldata, self.rowdata)
        self._set_alignment()
        # self.add_checkboxes_to_first_column()


    def append_row(self, row_data):
        """追加一行数据"""
        self.table.insert_row(index='end', values=row_data)
        self.table.reset_table()

    def get_treeview(self,widget):
        """递归查找Treeview组件"""
        if isinstance(widget, ttk.Treeview):
            return widget
        
        for child in widget.winfo_children():
            result = self.get_treeview(child)
            print(f"Searching in {widget} found: {result}")
            if result:
                return result
        
        return None


class CheckboxCell(ttk.Frame):
    def __init__(self, master, value=False, command=None):
        super().__init__(master)
        self.var = ttk.BooleanVar(value=value)
        self.checkbox = ttk.Checkbutton(
            self, 
            variable=self.var, 
            command=lambda: command(self.var.get()) if command else None
        )
        self.checkbox.pack(fill=ttk.BOTH, expand=True, padx=5, pady=2)
        