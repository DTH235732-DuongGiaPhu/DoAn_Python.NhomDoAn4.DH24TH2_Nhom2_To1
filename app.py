import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import NO, W, E, N, S 
import time

# --- MOCKUP HÀM VÀ LỚP (GIẢ ĐỊNH) ĐỂ CODE CHẠY ĐỘC LẬP ---
def getDbConnection():
    """Mock function for DB connection."""
    class MockConnection:
        def close(self): pass
    return MockConnection()

class DatabaseManager:
    # ... (Giữ nguyên phần Mockup) ...
    def __init__(self, conn):
        self.conn = conn
        # Dữ liệu mẫu (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        self.mock_data = [
            (1, 'MS001', 'Nhà Giả Kim', 'Paulo Coelho', 'Tâm Lý', 'Sách Nước Ngoài', 'NXB Văn Học', 80.0, 100.0, 5, '1988'),
            (2, 'MS002', 'Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Trẻ', 95.5, 120.0, 10, '1936'),
            (3, 'MS003', 'Toán Cao Cấp A1', 'Nhiều Tác Giả', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 120.0, 150.0, 1, '2023'),
            (4, 'MS004', 'Lập Trình Python Cơ Bản', 'Nguyễn Văn A', 'CNTT', 'Sách Trong Nước', 'NXB Khoa Học', 250.0, 300.0, 2, '2022'),
        ]
        
    def view_all(self):
        time.sleep(0.1) 
        return self.mock_data
        
    def search_for_suggestion(self, query):
        q = query.lower()
        results = [row for row in self.mock_data if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()]
        return results

    def get_book_by_id(self, db_id):
        try:
            db_id = int(db_id)
            for row in self.mock_data:
                if row[0] == db_id:
                    return row
            return None
        except:
            return None

    def insert_book_full(self, *values): 
        print(f"Mock Insert: {values}")
    def update_book_full(self, db_id, *values): 
        print(f"Mock Update ID {db_id}: {values}")
    def delete_book(self, db_id): 
        print(f"Mock Delete ID {db_id}")
# --- KẾT THÚC MOCKUP ---


# --- HÀM HỖ TRỢ CƠ BẢN ---
def center_window(win, w, h):
    """Canh giữa cửa sổ theo kích thước màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ----------------------------------------------------
#               CLASS CỬA SỔ MENU CHÍNH
# ----------------------------------------------------
class MainMenuWindow:
    def __init__(self, master, login_window_instance, db_conn):
        self.master = master
        self.login_window = login_window_instance
        self.db_conn = db_conn
        master.title("💡 HỆ THỐNG TRUNG TÂM QUẢN LÝ") 
        
        # Kích thước cửa sổ: 550x450, cân đối và gọn gàng
        self.WIDTH = 550 
        self.HEIGHT = 450 
        center_window(master, self.WIDTH, self.HEIGHT)
        master.resizable(False, False)
        
        self.book_manager_instance = None 
        
        self.setup_styles()
        self.setup_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Tiêu đề: Lớn và nổi bật
        style.configure("MenuHeader.TLabel", font=('Arial', 32, 'bold'), foreground="#1E88E5", padding=15)
        
        # Style chung cho các nút chức năng: Cỡ chữ 18 (lớn hơn), padding dọc giảm (12)
        style.configure("Menu.TButton", font=('Arial', 18, 'bold'), padding=[10, 12], relief="raised", borderwidth=0, foreground="#333333") 
        
        # 1. Quản lý kinh doanh (Xanh lá nhạt)
        style.configure("Business.Menu.TButton", background="#E8F5E9") 
        style.map("Business.Menu.TButton", background=[('active', '#C8E6C9')])

        # 2. Quản lý thông tin sách (Xanh dương nhạt)
        style.configure("BookInfo.Menu.TButton", background="#E3F2FD") 
        style.map("BookInfo.Menu.TButton", background=[('active', '#BBDEFB')])

        # 3. Quản lý kho sách (Vàng nhạt)
        style.configure("Stock.Menu.TButton", background="#FFFDE7") 
        style.map("Stock.Menu.TButton", background=[('active', '#FFF9C4')])

        # Thoát Ứng dụng (Đỏ nhạt, chữ ĐỎ) 
        style.configure("Exit.Menu.TButton", background="#FFEBEE", foreground="#C62828") 
        style.map("Exit.Menu.TButton", background=[('active', '#FFCDD2')])
        

    def setup_widgets(self):
        # Frame với padding ngang 70 để nút có độ rộng hợp lý
        main_frame = ttk.Frame(self.master, padding="70 30") 
        main_frame.pack(expand=True, fill='both')
        main_frame.columnconfigure(0, weight=1) 
        
        # Tiêu đề - pady (10, 40) tạo khoảng trống phía trên và dưới
        ttk.Label(main_frame, text="TRUNG TÂM QUẢN LÝ", style="MenuHeader.TLabel").grid(row=0, column=0, pady=(10, 40))

        buttons_info = [
            ("📈 1. Quản lý kinh doanh", "Business.Menu.TButton", lambda: messagebox.showinfo("Chức năng", "Chức năng Quản lý kinh doanh chưa được triển khai.")),
            ("📚 2. Quản lý thông tin sách", "BookInfo.Menu.TButton", self.open_book_manager),
            ("📦 3. Quản lý kho sách", "Stock.Menu.TButton", lambda: messagebox.showinfo("Chức năng", "Chức năng Quản lý kho sách chưa được triển khai.")),
            ("❌ Thoát Ứng dụng", "Exit.Menu.TButton", self.logout_to_login) 
        ]

        for i, (text, style_name, command) in enumerate(buttons_info):
            # Sử dụng pady 15 để chia đều không gian cho 4 nút
            ttk.Button(main_frame, text=text, command=command, style=style_name).grid(row=i + 1, column=0, pady=15, sticky='ew')
            
    # ... (Các hàm khác giữ nguyên) ...
    def open_book_manager(self):
        self.master.withdraw() 
        if not self.book_manager_instance or not self.book_manager_instance.master.winfo_exists():
            book_window = tk.Toplevel(self.master)
            book_window.protocol("WM_DELETE_WINDOW", self.close_book_manager)
            self.book_manager_instance = BookManagerApp(book_window, self, self.db_conn)
            center_window(book_window, 1200, 750) 
        else:
            self.book_manager_instance.master.deiconify()

    def close_book_manager(self):
        if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
            self.book_manager_instance.master.withdraw()
        self.master.deiconify()
        
    def logout_to_login(self):
        if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
            self.book_manager_instance.master.destroy() 
        
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            self.master.destroy()
            self.login_window.master.deiconify()
            self.login_window.master.focus_set()


# ----------------------------------------------------
#               CÁC LỚP KHÁC (Giữ nguyên)
# ----------------------------------------------------
class LoginWindow:
    def __init__(self, master, main_menu_class):
        self.master = master
        self.master.title("Đăng Nhập Hệ Thống Quản Lý")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.WIDTH = 480
        self.HEIGHT = 280
        center_window(master, self.WIDTH, self.HEIGHT)
        self.master.resizable(False, False)
        self.main_menu_class = main_menu_class
        self.main_menu_instance = None 
        self.username_var = tk.StringVar(value="admin") 
        self.password_var = tk.StringVar(value="123") 
        self.setup_widgets()
        
    def setup_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TLabel", font=('Arial', 12))
        style.configure("TEntry", font=('Arial', 12))
        style.configure("LoginHeader.TLabel", font=('Arial', 18, 'bold'), foreground="#1E88E5")
        style.configure("Login.TButton", font=('Arial', 13, 'bold'), padding=10, background="#4CAF50", foreground="white")
        style.map("Login.TButton", background=[('active', '#43A047')])
        
        main_frame = ttk.Frame(self.master, padding="30 20 30 20")
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="ĐĂNG NHẬP HỆ THỐNG", style="LoginHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(main_frame, text="👤 Tài khoản:", style="TLabel").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        ttk.Entry(main_frame, textvariable=self.username_var, width=35).grid(row=1, column=1, padx=10, pady=8, sticky='ew')

        ttk.Label(main_frame, text="🔒 Mật khẩu:", style="TLabel").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        ttk.Entry(main_frame, textvariable=self.password_var, show='*', width=35).grid(row=2, column=1, padx=10, pady=8, sticky='ew')

        ttk.Button(main_frame, text="ĐĂNG NHẬP", command=self.login, style="Login.TButton").grid(row=3, column=0, columnspan=2, pady=25, sticky='ew')
        
        self.master.bind('<Return>', lambda event: self.login())


    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if username == "admin" and password == "123":
            db_conn = getDbConnection()
            if db_conn is None:
                messagebox.showerror("Lỗi CSDL", "Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra Driver/Server/Tên CSDL.")
                return
            
            self.master.withdraw()

            if not self.main_menu_instance or not self.main_menu_instance.master.winfo_exists():
                self.main_window = tk.Toplevel(self.master)
                self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing_menu)
                self.main_menu_instance = self.main_menu_class(self.main_window, self, db_conn)
            
            self.main_window.deiconify()
        else:
            messagebox.showerror("Lỗi Đăng Nhập", "Tên tài khoản hoặc mật khẩu không đúng!")
            self.password_var.set("")

    def on_closing_menu(self):
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            if self.main_menu_instance and self.main_menu_instance.db_conn:
                try:
                    self.main_menu_instance.db_conn.close()
                except:
                    pass
            self.master.quit() 
        
    def on_closing(self):
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            self.master.quit()


class SearchWindow:
    def __init__(self, master, main_app_instance):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db

        master.title("🔍 Tìm Kiếm Sách Nhanh")
        master.transient(main_app_instance.master)
        master.grab_set()
        center_window(master, 650, 480)
        master.resizable(False, False)
        self.search_text = tk.StringVar()

        self.setup_widgets()
        
    def setup_widgets(self):
        style = ttk.Style()
        style.configure("SearchHeader.TLabel", font=('Arial', 14, 'bold'), foreground="#2196F3")
        style.configure("Search.TButton", font=('Arial', 11, 'bold'), padding=8)

        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill='both')

        ttk.Label(main_frame, text="Tìm Kiếm Nhanh Dữ Liệu Sách", style="SearchHeader.TLabel").pack(pady=(0, 15))
        
        ttk.Label(main_frame, text="Nhập từ khóa (Mã, Tên sách, Tác giả...):", font=('Arial', 11)).pack(pady=(5, 5), anchor='w')
        
        search_entry = ttk.Entry(main_frame, textvariable=self.search_text, font=('Arial', 12))
        search_entry.pack(pady=(0, 15), fill='x', ipady=3)
        
        self.search_text.trace_add("write", self.update_suggestions)
        self.master.bind('<Return>', lambda event: self.select_first_suggestion())

        self.results_tree = ttk.Treeview(main_frame, columns=("BookID", "Title", "Author"), show='headings', height=10)
        
        self.results_tree.column("BookID", width=100, anchor='center')
        self.results_tree.column("Title", width=300, anchor='w')
        self.results_tree.column("Author", width=200, anchor='w')
        
        self.results_tree.heading("BookID", text="Mã Sách")
        self.results_tree.heading("Title", text="Tên Sách")
        self.results_tree.heading("Author", text="Tác Giả")
        
        self.results_tree.bind('<<TreeviewSelect>>', self.select_suggestion)
        self.results_tree.pack(pady=10, fill='both', expand=True)

        ttk.Button(main_frame, text="ĐÓNG CỬA SỔ", command=self.master.destroy, style="Search.TButton").pack(pady=(15, 5), fill='x')
        
    def update_suggestions(self, *args):
        query = self.search_text.get().strip()
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if not query:
            return

        results = self.db.search_for_suggestion(query)

        for row in results[:10]:
            db_id = row[0] 
            book_id = row[1]
            title = row[2]  
            author = row[3]  
            
            self.results_tree.insert('', tk.END, values=(book_id, title, author), tags=(db_id,))
            
    def select_first_suggestion(self):
        children = self.results_tree.get_children()
        if children:
            self.results_tree.selection_set(children[0])
            self.results_tree.focus(children[0])
            self.select_suggestion(None) 

    def select_suggestion(self, event):
        selected_items = self.results_tree.selection()
        if not selected_items:
            return
            
        item_id = selected_items[0]
        
        try:
            db_id = self.results_tree.item(item_id, 'tags')[0]
        except IndexError:
            return
        
        book_info = self.db.get_book_by_id(db_id)
        
        if book_info:
            self.main_app.fill_form_with_data(book_info)
        
        self.master.destroy()

class BookManagerApp:
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance 
        master.title("📚 HỆ THỐNG QUẢN LÝ THÔNG TIN SÁCH")
        
        self.apply_styles()
        self.selected_book = None
        
        self.book_id_text = tk.StringVar()
        self.book_name_text = tk.StringVar()
        self.author_text = tk.StringVar()
        self.field_text = tk.StringVar()
        self.book_type_text = tk.StringVar()
        self.publisher_name_text = tk.StringVar()
        self.buy_price_text = tk.StringVar(value="0.0")
        self.cover_price_text = tk.StringVar(value="0.0")
        self.reprint_text = tk.StringVar(value="0")
        self.publish_year_text = tk.StringVar()
        
        self.total_books_var = tk.StringVar(value="Đang tải...")
        self.status_var = tk.StringVar(value="Kết nối CSDL: Đã sẵn sàng (Mockup)")

        self.BOOK_TYPES = ["Sách Nước Ngoài", "Sách Trong Nước"]
        
        self.setup_widgets()
        self.view_command() 
        
    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#2196F3", foreground="white", padding=[5, 5])
        style.configure("Treeview",
            font=('Arial', 10),
            rowheight=25,
            bordercolor="#E0E0E0", 
            borderwidth=1,
            relief="flat",
            fieldbackground="#F5F5F5" 
        )
        style.map('Treeview', background=[('selected', '#4CAF50')]) 
        
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("TCombobox", font=('Arial', 11), padding=2)
        style.configure("TSeparator", background="#CCCCCC") 
        
        style.configure("Action.TButton", font=('Arial', 11, 'bold'), padding=8, foreground="white")
        style.configure("Primary.TButton", font=('Arial', 10, 'bold'), padding=8)
        
        style.configure("Add.Action.TButton", background="#4CAF50") 
        style.map("Add.Action.TButton", background=[('active', '#43A047')])

        style.configure("Update.Action.TButton", background="#2196F3") 
        style.map("Update.Action.TButton", background=[('active', '#1E88E5')])
        
        style.configure("Delete.Action.TButton", background="#F44336") 
        style.map("Delete.Action.TButton", background=[('active', '#E53935')])

        style.configure("Search.Primary.TButton", background="#FFC107", foreground="#333333") 
        style.map("Search.Primary.TButton", background=[('active', '#FFB300')])
        
        style.configure("View.Primary.TButton", background="#9E9E9E", foreground="white") 
        style.map("View.Primary.TButton", background=[('active', '#757575')])
        
        style.configure("Clear.Primary.TButton", background="#BDBDBD", foreground="#333333") 
        style.map("Clear.Primary.TButton", background=[('active', '#A0A0A0')])

        style.configure("Logout.Primary.TButton", background="#795548", foreground="white") 
        style.map("Logout.Primary.TButton", background=[('active', '#6D4C41')])

        
    def setup_widgets(self):
        main_pane = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(main_pane, padding="10")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=0) 
        control_frame.grid_rowconfigure(0, weight=0) 
        control_frame.grid_rowconfigure(1, weight=1) 
        main_pane.add(control_frame, weight=0) 

        input_group = ttk.LabelFrame(control_frame, text=" CHI TIẾT SÁCH ", padding="15")
        input_group.grid(row=0, column=0, sticky=N+E+S+W, padx=(0, 10), pady=(0, 5))
        input_group.grid_columnconfigure(1, weight=1)
        input_group.grid_columnconfigure(3, weight=1)
        
        input_data = [
            ("MÃ SÁCH:", self.book_id_text, "entry"),
            ("TÊN SÁCH:", self.book_name_text, "entry"),
            ("TÁC GIẢ:", self.author_text, "entry"),
            ("LĨNH VỰC:", self.field_text, "entry"), 
            ("LOẠI SÁCH:", self.book_type_text, "combo", self.BOOK_TYPES),
            ("TÊN NXB:", self.publisher_name_text, "entry"), 
            ("GIÁ MUA:", self.buy_price_text, "spinbox", 0, 1000000),
            ("GIÁ BÌA:", self.cover_price_text, "spinbox", 0, 1000000),
            ("LẦN TÁI BẢN:", self.reprint_text, "spinbox", 0, 100),
            ("NĂM XUẤT BẢN:", self.publish_year_text, "entry"), 
        ]

        for i, data in enumerate(input_data):
            label_text, var, widget_type = data[0], data[1], data[2]
            row = i // 2
            col = (i % 2) * 2
            widget_col = col + 1

            ttk.Label(input_group, text=label_text, style="Input.TLabel").grid(row=row, column=col, sticky=W, padx=10, pady=5)

            if widget_type == "entry":
                ttk.Entry(input_group, textvariable=var).grid(row=row, column=widget_col, padx=(0, 10), pady=5, sticky='ew')
            elif widget_type == "combo":
                combo = ttk.Combobox(input_group, textvariable=var, values=data[3], state='readonly')
                combo.grid(row=row, column=widget_col, padx=(0, 10), pady=5, sticky='ew')
                if data[3]:
                    combo.set(data[3][0])
            elif widget_type == "spinbox":
                from_val, to_val = data[3], data[4]
                ttk.Spinbox(input_group, textvariable=var, from_=from_val, to=to_val, wrap=True).grid(row=row, column=widget_col, padx=(0, 10), pady=5, sticky='ew')
                
        info_group = ttk.LabelFrame(control_frame, text=" THÔNG TIN TỔNG QUAN ", padding="15")
        info_group.grid(row=1, column=0, sticky=N+E+S+W, padx=(0, 10), pady=(5, 0)) 
        info_group.grid_columnconfigure(0, weight=0) 
        info_group.grid_columnconfigure(1, weight=1) 
        
        ttk.Label(info_group, text="Tổng số đầu sách:", style="Input.TLabel").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.total_books_var, font=('Arial', 12, 'bold'), foreground="#F44336").grid(row=0, column=1, sticky=W, padx=10, pady=5)
        
        ttk.Separator(info_group, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(info_group, text="Trạng thái hệ thống:", style="Input.TLabel").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.status_var, font=('Arial', 10), foreground="#4CAF50").grid(row=2, column=1, sticky=W, padx=10, pady=5)


        button_group = ttk.LabelFrame(control_frame, text=" CHỨC NĂNG ", padding="10")
        button_group.grid(row=0, column=1, rowspan=2, sticky=N+S, padx=(10, 0))
        button_group.grid_columnconfigure(0, weight=1)

        buttons_info = [
            ("➕ THÊM SÁCH", self.add_command, "Add.Action.TButton"),
            ("🔄 CẬP NHẬT", self.update_command, "Update.Action.TButton"),
            ("❌ XÓA SÁCH", self.delete_command, "Delete.Action.TButton"),
            ("---", None, "TSeparator"),
            ("🔍 TÌM KIẾM", self.search_command, "Search.Primary.TButton"),
            ("📚 XEM TẤT CẢ", self.view_command, "View.Primary.TButton"),
            ("🧹 XÓA FORM", self.clear_form, "Clear.Primary.TButton"),
            ("---", None, "TSeparator"),
            ("⬅️ QUAY LẠI MENU", self.main_menu.close_book_manager, "Logout.Primary.TButton")
        ]

        row_index = 0
        for text, command, style_name in buttons_info:
            if text == "---":
                ttk.Separator(button_group, orient='horizontal').grid(row=row_index, column=0, sticky='ew', pady=8)
            else:
                ttk.Button(button_group, text=text, command=command, style=style_name).grid(row=row_index, column=0, padx=5, pady=4, sticky='ew')
            row_index += 1
            
        list_frame = ttk.Frame(main_pane, padding="10")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        main_pane.add(list_frame, weight=1) 

        all_column_ids = ["ID", "MaSach", "TenSach", "TacGia", "LinhVuc", "LoaiSach", "NXB", "GiaMua", "GiaBia", "LanTaiBan", "NamXB"]
        self.books_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_list.yview)
        self.books_list.configure(yscrollcommand=vsb.set)
        
        self.books_list.grid(row=0, column=0, sticky=N+E+S+W)
        vsb.grid(row=0, column=1, sticky='ns')
        
        self.books_list.column("ID", width=0, minwidth=0, stretch=NO)
        self.books_list.heading("ID", text="")
        
        display_column_names = ["Mã Sách", "Tên Sách", "Tác Giả", "Lĩnh Vực", "Loại Sách", "Tên NXB", "Năm XB", "Giá Mua", "Giá Bìa", "Lần TB"]
        display_column_ids = ["MaSach", "TenSach", "TacGia", "LinhVuc", "LoaiSach", "NXB", "NamXB", "GiaMua", "GiaBia", "LanTaiBan"]
        
        col_widths = [100, 180, 150, 100, 120, 120, 80, 80, 80, 70] 
        
        for name, col_id, width in zip(display_column_names, display_column_ids, col_widths):
            anchor = W if col_id in ["TenSach", "TacGia", "NXB", "LinhVuc", "LoaiSach"] else E
            if col_id in ["MaSach", "NamXB"]: anchor = 'center'
            
            self.books_list.column(col_id, width=width, minwidth=width, anchor=anchor)
            self.books_list.heading(col_id, text=name)
            
        self.books_list.bind('<ButtonRelease-1>', self.get_selected_row)

    def fill_form_with_data(self, book_info, update_selection=True):
        self.clear_form()
        self.selected_book = book_info

        def clean_str(val):
            if val is not None:
                return str(val).strip().strip("'") 
            return ""

        self.book_id_text.set(clean_str(book_info[1]))
        self.book_name_text.set(clean_str(book_info[2]))
        self.author_text.set(clean_str(book_info[3]))
        self.field_text.set(clean_str(book_info[4]))
        
        type_val = clean_str(book_info[5])
        self.book_type_text.set(type_val if type_val in self.BOOK_TYPES else (self.BOOK_TYPES[0] if self.BOOK_TYPES else ""))
        
        self.publisher_name_text.set(clean_str(book_info[6]))

        self.buy_price_text.set(str(book_info[7]) if book_info[7] is not None else "0.0")
        self.cover_price_text.set(str(book_info[8]) if book_info[8] is not None else "0.0")
        self.reprint_text.set(str(book_info[9]) if book_info[9] is not None else "0")
        self.publish_year_text.set(clean_str(book_info[10]))
        
        
        if update_selection:
            db_id_to_select = str(book_info[0])
            
            self.books_list.unbind('<ButtonRelease-1>')
            self.books_list.selection_remove(self.books_list.selection())

            found_item = None
            for item in self.books_list.get_children():
                if str(self.books_list.item(item, 'values')[0]) == db_id_to_select:
                    found_item = item
                    break
                    
            if found_item:
                self.books_list.selection_set(found_item)
                self.books_list.focus(found_item)
                self.books_list.see(found_item)
                    
            self.books_list.bind('<ButtonRelease-1>', self.get_selected_row)

    def clear_form(self):
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.author_text.set("")
        
        self.field_text.set("") 
        if self.BOOK_TYPES:
            self.book_type_text.set(self.BOOK_TYPES[0])

        self.publisher_name_text.set("")
        self.buy_price_text.set("0.0")
        self.cover_price_text.set("0.0")
        self.reprint_text.set("0")
        self.publish_year_text.set("")

        self.selected_book = None
        if self.books_list.selection():
            self.books_list.selection_remove(self.books_list.selection())
            
    def get_selected_row(self, event):
        selected_item = self.books_list.focus() 
        
        if not selected_item:
            self.books_list.selection_remove(self.books_list.selection())
            self.clear_form()
            return
            
        self.books_list.selection_remove(self.books_list.selection())
            
        values = self.books_list.item(selected_item, 'values')
        
        self.fill_form_with_data(values, update_selection=False)
        
    def view_command(self):
        self.clear_form()
        for item in self.books_list.get_children():
            self.books_list.delete(item)
            
        self.total_books_var.set("Đang tải...") 
        
        try:
            data = self.db.view_all()
            for row in data:
                self.books_list.insert('', tk.END, values=row)
            
            self.total_books_var.set(f"{len(data)} đầu sách") 
            self.status_var.set("Kết nối CSDL: Đã sẵn sàng (Mockup)")
            
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")
            self.total_books_var.set("LỖI KẾT NỐI!")
            self.status_var.set("Kết nối CSDL: Lỗi")
            
    def get_all_input_values(self):
        return (
            self.book_id_text.get(), self.book_name_text.get(), self.author_text.get(),
            self.field_text.get(), self.book_type_text.get(), self.publisher_name_text.get(),
            self.buy_price_text.get(), self.cover_price_text.get(), self.reprint_text.get(),
            self.publish_year_text.get()
        )
        
    def validate_input(self, values):
        if not values[0] or not values[1] or not values[2]:
            messagebox.showerror("Lỗi", "Vui lòng điền tối thiểu Mã Sách, Tên Sách, và Tác Giả.")
            return False
        try:
            float(values[6])
            float(values[7])
            reprint_val = values[8].strip()
            if reprint_val:
                 int(reprint_val)
            return True
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Giá Mua, Giá Bìa, Lần Tái Bản phải là số hợp lệ.")
            return False

    def add_command(self):
        values = self.get_all_input_values()
        if not self.validate_input(values): return
        try:
            self.db.insert_book_full(*values)
            self.view_command()
            messagebox.showinfo("Thành công", f"Đã thêm sách: {values[1]}")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi thêm sách: {e}")
            
    def update_command(self):
        if not self.selected_book:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sách để cập nhật.")
            return
        book_db_id = self.selected_book[0]
        values = self.get_all_input_values()
        if not self.validate_input(values): return
        try:
            self.db.update_book_full(book_db_id, *values)
            self.view_command()
            messagebox.showinfo("Thành công", f"Đã cập nhật sách ID: {book_db_id}")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật sách: {e}")
            
    def delete_command(self):
        if not self.selected_book:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sách để xóa.")
            return
        book_id = self.selected_book[0]
        book_title = self.selected_book[2]

        if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa sách:\n'{book_title}' (ID: {book_id})?"):
            try:
                self.db.delete_book(book_id)
                self.view_command()
                messagebox.showinfo("Thành công", "Đã xóa sách.")
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa sách: {e}")

    def search_command(self):
        search_window = tk.Toplevel(self.master)
        SearchWindow(search_window, self)


# --- KHỞI CHẠY ỨNG DỤNG ---
if __name__ == '__main__':
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow) 
    root.mainloop()