import tkinter as tk
from tkinter import ttk, messagebox
# Import hàm kết nối từ file riêng
from connection_manager import getDbConnection
# Import DatabaseManager
from database import DatabaseManager


# --- HÀM HỖ TRỢ CƠ BẢN ---
def center_window(win, w, h):
    """Canh giữa cửa sổ theo kích thước màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# --- CLASS CỬA SỔ ĐĂNG NHẬP ---
class LoginWindow:
    def __init__(self, master, main_app_class):
        self.master = master
        self.master.title("Đăng Nhập Hệ Thống Quản Lý")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.WIDTH = 450
        self.HEIGHT = 220
        center_window(master, self.WIDTH, self.HEIGHT)
        self.master.resizable(False, False)
        self.main_app_class = main_app_class
        self.main_app_instance = None
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.setup_widgets()

    def setup_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=('Arial', 12, 'bold'))
        style.configure("TEntry", font=('Arial', 12))
        style.configure("Login.TButton", font=('Arial', 13, 'bold'), padding=8, background="#4CAF50", foreground="white")

        main_frame = ttk.Frame(self.master, padding="25 20 25 20")
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="👤 Tên tài khoản:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        ttk.Entry(main_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, padx=10, pady=8, sticky='ew')

        ttk.Label(main_frame, text="🔒 Mật khẩu:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        ttk.Entry(main_frame, textvariable=self.password_var, show='*', width=30).grid(row=1, column=1, padx=10, pady=8, sticky='ew')

        ttk.Button(main_frame, text="Đăng Nhập", command=self.login, style="Login.TButton").grid(row=2, column=0, columnspan=2, pady=20, sticky='ew')
        
        self.master.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if username == "admin" and password == "123":
            # GỌI HÀM KẾT NỐI TỪ connection_manager.py
            db_conn = getDbConnection()
            if db_conn is None:
                messagebox.showerror("Lỗi CSDL", "Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra Driver/Server/Tên CSDL.")
                return
            
            self.master.withdraw()

            if not self.main_app_instance:
                self.main_window = tk.Toplevel(self.master)
                self.main_window.protocol("WM_DELETE_WINDOW", self.logout_and_quit)

                # TRUYỀN ĐỐI TƯỢNG KẾT NỐI (db_conn) VÀO BookManagerApp
                self.main_app_instance = self.main_app_class(self.main_window, self, db_conn)

                self.main_window.state('zoomed')
                center_window(self.main_window, 950, 650)
                self.main_window.deiconify()
            else:
                self.main_window.deiconify()
                self.main_window.state('zoomed')
        else:
            messagebox.showerror("Lỗi Đăng Nhập", "Tên tài khoản hoặc mật khẩu không đúng!")
            self.password_var.set("")

    def logout_and_show_login(self):
        if self.main_app_instance and self.main_app_instance.master:
            self.main_app_instance.master.withdraw()
            
            # Đóng kết nối CSDL khi đăng xuất
            if self.main_app_instance and self.main_app_instance.db.conn:
                try:
                    self.main_app_instance.db.conn.close()
                except:
                    pass
            
        self.master.deiconify()
        self.master.focus_set()

    def logout_and_quit(self):
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            # Đóng kết nối CSDL khi thoát
            if self.main_app_instance and self.main_app_instance.db.conn:
                try:
                    self.main_app_instance.db.conn.close()
                except:
                    pass
            self.master.quit()

    def on_closing(self):
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            # Đóng kết nối CSDL khi thoát
            if self.main_app_instance and self.main_app_instance.db.conn:
                try:
                    self.main_app_instance.db.conn.close()
                except:
                    pass
            self.master.quit()

# --- CLASS CỬA SỔ TÌM KIẾM CÓ GỢI Ý ---
class SearchWindow:
    def __init__(self, master, main_app_instance):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db

        master.title("🔍 Tìm Kiếm Sách Nhanh")
        master.transient(main_app_instance.master)
        master.grab_set()
        center_window(master, 600, 480)
        master.resizable(False, False)
        self.search_text = tk.StringVar()

        self.setup_widgets()

    def setup_widgets(self):
        main_frame = ttk.Frame(self.master, padding="15")
        main_frame.pack(expand=True, fill='both')

        ttk.Label(main_frame, text="Nhập từ khóa tìm kiếm (Tên sách, Tác giả, Mã sách...):", font=('Arial', 12, 'bold')).pack(pady=10, anchor='w')
        
        search_entry = ttk.Entry(main_frame, textvariable=self.search_text, width=70, font=('Arial', 12))
        search_entry.pack(pady=5, fill='x')
        
        self.search_text.trace_add("write", self.update_suggestions)
        
        self.results_tree = ttk.Treeview(main_frame, columns=("BookID", "Title", "Author"), show='headings', height=10)
        
        self.results_tree.column("BookID", width=100, anchor='center')
        self.results_tree.column("Title", width=250, anchor='w')
        self.results_tree.column("Author", width=150, anchor='w')
        
        self.results_tree.heading("BookID", text="Mã Sách")
        self.results_tree.heading("Title", text="Tên Sách")
        self.results_tree.heading("Author", text="Tác Giả")
        
        self.results_tree.bind('<<TreeviewSelect>>', self.select_suggestion)

        self.results_tree.pack(pady=10, fill='both', expand=True)

        ttk.Button(main_frame, text="Đóng", command=self.master.destroy, style="TButton").pack(pady=15, padx=10, fill='x')
        
    def update_suggestions(self, *args):
        query = self.search_text.get().strip()
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if not query:
            return

        # Dữ liệu trả về: (Id, MaSach, TenSach, TenTacGia)
        results = self.db.search_for_suggestion(query)

        for row in results[:10]:
            db_id = row[0]
            book_id = row[1]
            title = row[2]  
            author = row[3]  
            
            self.results_tree.insert('', tk.END, values=(book_id, title, author), tags=(db_id,))

    def select_suggestion(self, event):
        selected_items = self.results_tree.selection()
        if not selected_items:
            return
            
        item_id = selected_items[0]
        db_id = self.results_tree.item(item_id, 'tags')[0]
        
        book_info = self.db.get_book_by_id(db_id)
        
        if book_info:
            self.main_app.fill_form_with_data(book_info)
        
        self.master.destroy()


# --- CLASS ỨNG DỤNG CHÍNH (QUẢN LÝ SÁCH) ---
class BookManagerApp:
    def __init__(self, master, login_window_instance, db_conn):
        # TRUYỀN KẾT NỐI VÀO DATABASE MANAGER
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.login_window = login_window_instance
        master.title("📚 Hệ Thống Quản Lý Sách Chuyên Nghiệp")
        
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

        # KHÔNG KHAI BÁO self.FIELDS NỮA (Lĩnh vực là Entry)
        self.BOOK_TYPES = ["Sách Nước Ngoài", "Sách Trong Nước"]

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)

        self.setup_widgets()
        self.view_command()
        
    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4CAF50", foreground="white")
        style.configure("Treeview",
            font=('Arial', 10),
            rowheight=25,
            # Cấu hình để có đường kẻ ngang và dọc như table
            bordercolor="#B0B0B0",
            borderwidth=1,
            relief="solid",
            fieldbackground="white" # Màu nền trắng giúp đường kẻ nổi bật
        )
        style.map('Treeview', background=[('selected', '#45A049')])

        style.configure("TLabel", font=('Arial', 11))
        style.configure("TEntry", font=('Arial', 11))
        style.configure("Input.TLabel", font=('Arial', 11, 'bold'))

        style.configure("Add.TButton", font=('Arial', 11, 'bold'), padding=8, background="#4CAF50", foreground="white")
        style.configure("Update.TButton", font=('Arial', 11, 'bold'), padding=8, background="#2196F3", foreground="white")
        style.configure("Delete.TButton", font=('Arial', 11, 'bold'), padding=8, background="#F44336", foreground="white")

        style.configure("Small.TButton", font=('Arial', 10, 'bold'), padding=6)
        style.configure("Search.TButton", font=('Arial', 10, 'bold'), padding=6, background="#FFC107", foreground="#333333")
        
    def setup_widgets(self):
        top_frame = ttk.Frame(self.master, padding="10 10 10 10", relief=tk.RAISED)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        top_frame.grid_columnconfigure(0, weight=3)
        top_frame.grid_columnconfigure(1, weight=1)

        # A. Khu vực Input (10 trường) - ĐÃ CẬP NHẬT LĨNH VỰC LÀ ENTRY
        input_frame = ttk.Frame(top_frame, padding="5 5 5 5", relief=tk.GROOVE, borderwidth=1)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        input_data = [
            ("MÃ SÁCH:", self.book_id_text, "entry"),
            ("TÊN SÁCH:", self.book_name_text, "entry"),
            ("TÁC GIẢ:", self.author_text, "entry"),          
            ("LĨNH VỰC:", self.field_text, "entry"),          # ĐÃ CHUYỂN THÀNH ENTRY
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

            ttk.Label(input_frame, text=label_text, style="Input.TLabel").grid(row=row, column=col, sticky="w", padx=5, pady=5)

            if widget_type == "entry":
                ttk.Entry(input_frame, textvariable=var, font=('Arial', 11)).grid(row=row, column=widget_col, padx=5, pady=5, sticky='ew')
            elif widget_type == "combo":
                combo = ttk.Combobox(input_frame, textvariable=var, values=data[3], font=('Arial', 11), state='readonly')
                combo.grid(row=row, column=widget_col, padx=5, pady=5, sticky='ew')
                if data[3]:
                    combo.set(data[3][0])
            elif widget_type == "spinbox":
                from_val, to_val = data[3], data[4]
                ttk.Spinbox(input_frame, textvariable=var, from_=from_val, to=to_val, wrap=True, font=('Arial', 11)).grid(row=row, column=widget_col, padx=5, pady=5, sticky='ew')
                
        # B. Khu vực Buttons
        button_frame = ttk.Frame(top_frame, padding="5 5 5 5")
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        buttons_info = [
            ("➕ Thêm Sách", self.add_command, "Add.TButton"),
            ("🔄 Cập Nhật", self.update_command, "Update.TButton"),
            ("❌ Xóa Sách", self.delete_command, "Delete.TButton"),
            ("🔍 Tìm Kiếm", self.search_command, "Search.TButton"),
            ("📚 Xem Tất Cả", self.view_command, "Small.TButton"),
            ("🧹 Xóa Form", self.clear_form, "Small.TButton"),
            ("🚪 Thoát", self.login_window.logout_and_show_login, "Small.TButton")
        ]

        for i, (text, command, style_name) in enumerate(buttons_info):
            ttk.Button(button_frame, text=text, command=command, style=style_name).grid(row=i, column=0, padx=5, pady=4, sticky='ew')

        button_frame.grid_columnconfigure(0, weight=1)
        
        # 2. Bảng hiển thị (Treeview)
        list_frame = ttk.Frame(self.master, padding="10 10 10 10")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # CỘT CSDL trả về: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        all_column_ids = ["ID", "MaSach", "TenSach", "TacGia", "LinhVuc", "LoaiSach", "NXB", "GiaMua", "GiaBia", "LanTaiBan", "NamXB"]
        self.books_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")
        self.books_list.grid(row=0, column=0, sticky="nsew")
        
        self.books_list.column("ID", width=0, minwidth=0, stretch=tk.NO)
        self.books_list.heading("ID", text="")
        
        display_column_names = ["Mã Sách", "Tên Sách", "Tác Giả", "Lĩnh Vực", "Loại Sách", "Tên NXB", "Giá Mua", "Giá Bìa", "Lần TB", "Năm XB"]
        display_column_ids = ["MaSach", "TenSach", "TacGia", "LinhVuc", "LoaiSach", "NXB", "GiaMua", "GiaBia", "LanTaiBan", "NamXB"]
        col_widths = [100, 200, 150, 100, 100, 150, 80, 80, 60, 100]
        
        for i, (name, col_id, width) in enumerate(zip(display_column_names, display_column_ids, col_widths)):
            anchor = 'w' if col_id in ["TenSach", "TacGia", "NXB", "LinhVuc"] else 'center'
            if col_id in ["GiaMua", "GiaBia"]: anchor = 'e'
            
            self.books_list.column(col_id, width=width, minwidth=width, anchor=anchor)
            self.books_list.heading(col_id, text=name)
            
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_list.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.books_list.configure(yscrollcommand=vsb.set)

        self.books_list.bind('<Button-1>', self.get_selected_row)

    # --- LOGIC XỬ LÝ FORM VÀ CSDL ---
    def fill_form_with_data(self, book_info, update_selection=True):
        self.clear_form()
        self.selected_book = book_info

        # Hàm hỗ trợ làm sạch chuỗi
        def clean_str(val):
            if val is not None:
                return str(val).strip().strip("'")
            return ""

        # Dữ liệu chuỗi: ID DB (0), Mã Sách (1), Tên Sách (2), Tác Giả (3), Lĩnh Vực (4), Loại Sách (5), Tên NXB (6)
        self.book_id_text.set(clean_str(book_info[1]))
        self.book_name_text.set(clean_str(book_info[2]))
        self.author_text.set(clean_str(book_info[3]))
        
        # Xử lý Lĩnh Vực (Entry)
        self.field_text.set(clean_str(book_info[4]))
        
        # Xử lý ComboBox Loại Sách
        type_val = clean_str(book_info[5])
        self.book_type_text.set(type_val if type_val in self.BOOK_TYPES else self.BOOK_TYPES[0])
        
        self.publisher_name_text.set(clean_str(book_info[6]))

        # Dữ liệu số: Giá Mua (7), Giá Bìa (8), Lần TB (9), Năm XB (10)
        self.buy_price_text.set(str(book_info[7]) if book_info[7] is not None else "0.0")
        self.cover_price_text.set(str(book_info[8]) if book_info[8] is not None else "0.0")
        self.reprint_text.set(str(book_info[9]) if book_info[9] is not None else "0")
        self.publish_year_text.set(clean_str(book_info[10]))
        
        
        # === PHẦN KHẮC PHỤC LỖI ĐỆ QUY VÀ CHỈ CHỌN LẠI KHI CẦN ===
        if update_selection:
            db_id_to_select = str(book_info[0])
            
            # 1. Hủy liên kết sự kiện trước khi thiết lập lại lựa chọn
            self.books_list.unbind('<<TreeviewSelect>>')
            
            # 2. Xóa và tìm hàng để chọn lại (cần cho chức năng TÌM KIẾM/CẬP NHẬT)
            self.books_list.selection_remove(self.books_list.selection())

            for item in self.books_list.get_children():
                # values[0] là ID (hidden column)
                if str(self.books_list.item(item, 'values')[0]) == db_id_to_select:
                    self.books_list.selection_set(item)
                    self.books_list.focus(item)
                    self.books_list.see(item)
                    break
                    
            # 3. Liên kết lại sự kiện sau khi hoàn thành
            self.books_list.bind('<<TreeviewSelect>>', self.get_selected_row)

    def clear_form(self):
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.author_text.set("")
        
        self.field_text.set("") # LĨNH VỰC - ĐÃ BỎ self.FIELDS
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
        # 1. Tìm item được click ngay dưới con trỏ chuột
        selected_item = self.books_list.identify_row(event.y)
        
        # Nếu không click vào hàng nào (click vào vùng trống/heading)
        if not selected_item:
            # Nếu có mục đã chọn trước đó, hãy xóa chọn
            if self.books_list.selection():
                self.books_list.selection_remove(self.books_list.selection())
            self.clear_form()
            return
            
        # 2. Xóa các mục đã chọn trước (để tránh chọn nhiều)
        self.books_list.selection_remove(self.books_list.selection())
        
        # 3. Chọn item vừa click
        self.books_list.selection_set(selected_item)
        self.books_list.focus(selected_item) # Bắt buộc focus để highlight
        
        # 4. Lấy dữ liệu và tải lên form
        values = self.books_list.item(selected_item, 'values')
        
        # Ngăn chặn đệ quy
        self.fill_form_with_data(values, update_selection=False)
        
        # (Bạn có thể xóa các dòng print kiểm tra nếu mọi thứ đã hoạt động)
        # print(f"✅ Đã tải dữ liệu của mục ID DB: {values[0]}")

    def view_command(self):
        self.clear_form()
        for item in self.books_list.get_children():
            self.books_list.delete(item)
            
        try:
            for row in self.db.view_all():
                self.books_list.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")
            
    def get_all_input_values(self):
        return (
            self.book_id_text.get(), self.book_name_text.get(), self.author_text.get(),
            self.field_text.get(), self.book_type_text.get(), self.publisher_name_text.get(),
            self.buy_price_text.get(), self.cover_price_text.get(), self.reprint_text.get(),
            self.publish_year_text.get()
        )
        
    def validate_input(self, values):
        # Yêu cầu MaSach, TenSach, TenTacGia (values[0], values[1], values[2])
        if not values[0] or not values[1] or not values[2]:
            messagebox.showerror("Lỗi", "Vui lòng điền tối thiểu Mã Sách, Tên Sách, và Tác Giả.")
            return False
        # Dữ liệu số
        try:
            float(values[6])
            float(values[7])
            int(values[8])
            return True
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Giá Mua, Giá Bìa, Lần Tái Bản phải là số hợp lệ.")
            return False

    def add_command(self):
        values = self.get_all_input_values()
        if not self.validate_input(values): return
        try:
            # Truyền TÊN vào hàm, database.py sẽ lo việc chuyển đổi thành ID
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
            # Truyền TÊN vào hàm, database.py sẽ lo việc chuyển đổi thành ID
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
    login_app = LoginWindow(root, BookManagerApp)
    root.mainloop()