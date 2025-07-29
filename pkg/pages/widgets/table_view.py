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
        
                # 创建遮罩层
        self.loading_mask = ttk.Frame(
            master=self,
            bootstyle=DARK,
        )
        self.loading_mask.configure(style="Transparent.TFrame")
        self.loading_mask.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_mask.lower()  # 默认隐藏在表格下方
        
        # 加载提示标签
        self.loading_label = ttk.Label(
            master=self.loading_mask,
            text="加载中...",
            bootstyle=INFO,
            font=("Helvetica", 12, "bold")
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # 加载动画（可选）
        self.loading_animation = ttk.Progressbar(
            master=self.loading_mask,
            mode=INDETERMINATE,
            bootstyle=INFO,
            length=200
        )
        self.loading_animation.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.coldata = coldata
        self.rowdata = rowdata
        self.master = master
        self.add_callback = add_callback
        self.update_callback = update_callback
        self.delete_callback = delete_callback
        self.detail_callback = detail_callback
        self.checkbox_vars = {}
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
        # self.refresh_data(self.rowdata)

    def _set_alignment(self):
        """设置列和表头对齐方式"""
        tree = self.table.view
        for col_idx, col in enumerate(self.coldata):
            col_id = tree["columns"][col_idx]
            if col.get("text") == "id":
                tree.column(col_id, width=0)
                tree.column(col_id, stretch=False)
            else:
                tree.column(col_id, anchor=col.get("anchor", "w"))  # 内容对齐
                tree.heading(col_id, text=col["text"], anchor=col.get("anchor", "w"))  # 表头对齐
        # self.table.view.tk

    def refresh_data(self, rowdata):
        """刷新表格数据（可指定新的 pod_type）"""
        self.table.delete_rows()
        self.rowdata = rowdata
        self.table.build_table_data(self.coldata, self.rowdata)
        self._set_alignment()


    def append_row(self, row_data):
        """追加一行数据"""
        self.table.insert_row(index='end', values=row_data)
        self.table.reset_table()

    def get_selected_rows(self):
        """获取所有选中的行"""
        selected = []
        for key, var in self.checkbox_vars.items():
            if var.get():
                selected.append(key)
        return selected

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
    
    def show_loading(self):
        """显示加载遮罩层"""
        self.loading_mask.lift()  # 显示在表格上方
        self.loading_animation.start()  # 启动动画

    def hide_loading(self):
        """隐藏加载遮罩层"""
        self.loading_mask.lower()  # 隐藏到表格下方
        self.loading_animation.stop()  # 停止动画