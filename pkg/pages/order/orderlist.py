# orderlist.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from widgets.table_view import TableView
import time

col_data = [
                    {"text": " Name"            , "stretch": True, "anchor": "w"},
                    {"text": " Age"             , "stretch": True, "anchor": "w"},
                    {"text": " Email"           , "stretch": True, "anchor": "w"},
                    {"text": " Address"         , "stretch": True, "anchor": "w"},
                    {"text": " Phone Number"    , "stretch": True, "anchor": "w"},
                 ]

row_data = [
                ('John Doe',      28, 'johnqwertyuiohj67895tg.doe@example.com',      '1234 Elm Street, Springfield'  , '(555) 123-4567'),
                ('Jane Smith',    34, 'jane.smith@example.com',    '5678 Oak Avenue, Metropolis'   , '(555) 987-6543'),
                ('Emily Johnson', 22, 'emily.johnson@example.com', '9101 Pine Road, Rivertown'     , '(555) 555-1234'),
                ('Michael Brown', 41, 'michael.brown@example.com', '2345 Maple Street, Smalltown'  , '(555) 223-4567'),
                ('Sarah Davis',   29, 'sarah.davis@example.com',   '6789 Birch Avenue, Lakeside'   , '(555) 876-5432'),
                ('David Wilson',  33, 'david.wilson@example.com',  '1357 Cedar Drive, Uptown'      , '(555) 111-2233'),
                ('Linda Moore',   38, 'linda.moore@example.com',   '2468 Pine Hill, Midtown'       , '(555) 444-5678'),
                ('James Taylor',  25, 'james.taylor@example.com',  '3690 Elm Lane, Rivertown'      , '(555) 999-1234'),
                ('Rachel Clark',   36, 'rachel.clark@example.com', '4812 Oak Road, Hilltop'        , '(555) 555-7890'),
                ('Christopher Lewis', 30, 'christopher.lewis@example.com', '1023 Cherry Street, Downtown', '(555) 333-4455'),
                ('Samantha Green', 27, 'samantha.green@example.com', '7890 Maple Road, Westfield'        , '(555) 777-1122'),
                ('Daniel Lee',     31, 'daniel.lee@example.com', '2221 Pine Ridge, Brookside'            , '(555) 321-4567'),
                ('Olivia Martinez', 40, 'olivia.martinez@example.com', '4200 Cedar Drive, Oldtown'       , '(555) 654-7890'),
                ('Sophia Brown',    23, 'sophia.brown@example.com', '3421 Oak Lane, Rivertown'           , '(555) 876-4321'),
                ('Jack Wilson', 35, 'jack.wilson@example.com', '1156 Birch Avenue, Northside'            , '(555) 231-6789'),
                ('Emma Scott', 29, 'emma.scott@example.com', '1345 Pine Avenue, Lakeside'                , '(555) 444-1234'),
                ('Henry White', 45, 'henry.white@example.com', '2777 Maple Street, West Hills'           , '(555) 555-6789'),
                ('Ava Hall', 32, 'ava.hall@example.com', '8902 Cedar Lane, Greenfield'                   , '(555) 666-7890'),
                ('Ethan Harris', 28, 'ethan.harris@example.com', '1035 Elmwood Drive, Midtown'           , '(555) 777-3345'),
                ('Mason Allen', 37, 'mason.allen@example.com', '2468 Oakwood Street, Hillside'           , '(555) 555-1122'),
                ('Isabella Young', 24, 'isabella.young@example.com', '7823 Birch Road, Riverbend'        , '(555) 888-1234'),
                ('Liam King', 34, 'liamisabellamasonhenry_white.king@example.com', '3322 Pine Avenue, Southgate'                 , '(555) 222-3456'),
            
            ]

class OrderList(ttk.Frame):
    def __init__(self, master, colors):
        super().__init__(master)
        self.colors = colors
        self.pack(fill=ttk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill=BOTH, padx=10)
        btn_group = ttk.Labelframe(
            master=container, text="订单管理", padding=(10, 5)
        )
        btn_group.pack(fill=BOTH,padx=15)

        # 操作按钮区
        option_btn_frame = ttk.Frame(btn_group)
        option_btn_frame.pack(pady=5,fill=BOTH)
        status_menu_text = ["全部","未提交","已提交"]
        self.status_menu = ttk.Menu(self)
        for i, t in enumerate(status_menu_text):
            self.status_menu.add_radiobutton(label=t, value=i,command=lambda text=t,value=i: self.enforce_exclusive(text=text,value=value))

        # 查询区
        ttk.Label(option_btn_frame, text="状态筛选").pack(side=LEFT,padx=10)
        self.status_menu_btn = ttk.Menubutton(
            master=option_btn_frame,
            text="全部",
            bootstyle=(WARNING, OUTLINE),
            menu=self.status_menu,
            width=10
        )
        self.status_menu_btn.pack(side=LEFT, pady=5)

        ttk.Label(option_btn_frame, text="订单号").pack(side=LEFT,padx=10)
        s_orderno = ttk.Entry(option_btn_frame,width=20)
        s_orderno.pack(side=LEFT,padx=10)
        ttk.Label(option_btn_frame, text="订单日期").pack(side=LEFT,padx=10)
        start = ttk.DateEntry(option_btn_frame,width=20)
        start.pack(side=LEFT,padx=10)
        ttk.Label(option_btn_frame, text="--").pack(side=LEFT)
        end = ttk.DateEntry(option_btn_frame,width=20)
        end.pack(side=LEFT,padx=10)
        ttk.Button(
            option_btn_frame, 
            text="查询", 
            bootstyle="success",
            command=self.refresh_orders
        ).pack(side=LEFT, padx=10)

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

        # 表格控件（父容器为当前OrderList Frame）
        self.table = TableView(
            master=self,  # 关键：表格的父容器是当前OrderList Frame
            colors=self.colors,
            coldata=col_data,
            rowdata=row_data,
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
        self.table.refresh_data(row_data)

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
    
    def enforce_exclusive(self,text,value):
        print(text,value)
        self.status_menu_btn.configure(text=text)