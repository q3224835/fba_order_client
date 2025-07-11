# table_view.py

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import time

class TableView(ttk.Frame):
    def __init__(self, parent, coldata, rowdata):
        super().__init__(parent)

        self.coldata = coldata
        self.rowdata = rowdata

        # 初始化表格
        self.table = Tableview(
            master=self,
            coldata=self.coldata,
            paginated=True,
            searchable=True,
            bootstyle=ttk.PRIMARY,
            pagesize=10,
        )
        self.table.pack(fill=ttk.BOTH, expand=True, padx=10, pady=10)

        # 加载初始数据
        self.load_data()
        self.bind_right_client_menu()

         # 获取Treeview控件
        tree = self.table.view
        
        # 设置列内容的对齐方式
        for col_idx, col in enumerate(self.coldata):
            col_id = tree["columns"][col_idx] if col_idx < len(tree["columns"]) else f"#{col_idx+1}"
            tree.column(col_id, anchor=col.get("anchor", "w"))  # 设置列内容对齐
        
        # 设置表头（列标题）的对齐方式
        for col_idx, col in enumerate(self.coldata):
            col_id = tree["columns"][col_idx] if col_idx < len(tree["columns"]) else f"#{col_idx+1}"
            tree.heading(col_id, text=col["text"], anchor=col.get("anchor", "w"))  # 设置表头对齐

    def load_data(self):
        """加载当前 Pod 类型的数据"""
        self.table.build_table_data(self.coldata, self.rowdata)

    def refresh_data(self, rowdata):
        """刷新表格数据（可指定新的 pod_type）"""
        self.table.delete_rows()
        self.rowdata = rowdata
        self.load_data()

    def append_row(self, row_data):
        """追加一行数据"""
        self.table.insert_row(index='end', values=row_data)
        self.table.reset_table()

    def delete_row(self, index):
        """删除指定索引的一行"""
        try:
            self.table.delete_row(index)
        except IndexError:
            print(f"Index {index} out of range for deletion.")

    def update_row(self, index, new_values):
        """更新指定索引的一行数据"""
        try:
            self.table.update_row(index=index, values=new_values)
        except IndexError:
            print(f"Index {index} out of range for update.")
    
    def bind_right_client_menu(self):
        self.menu = ttk.Menu(self.master,tearoff=0)

        self.menu.add_command(label="复制", command=lambda:print("复制"))
        self.menu.add_command(label="编辑", command=lambda:print("编辑"))
        self.menu.add_command(label="删除", command=lambda:print("删除"))

        self.table.view.bind("<Button-3>",self.show_context_menu)
        self.table.view.bind("<Button-2>",self.show_context_menu)

        self.selected_index = None

    def show_context_menu(self, event):
        """显示右键菜单并记录选中行"""
        # 获取点击的行
        rowid = self.table.view.identify_row(event.y)
        value = self.table.view.item(rowid)
        print(value)
        if rowid:
            self.table.view.selection_remove(*self.table.view.selection())
            self.table.view.selection_add(rowid)
            self.selected_index = rowid
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()