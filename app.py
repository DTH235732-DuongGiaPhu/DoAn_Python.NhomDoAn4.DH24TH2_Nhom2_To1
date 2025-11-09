import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import NO, W, E, N, S
import time
from datetime import datetime, timedelta
import random

# ----- MOCKUP HÀM VÀ LỚP (GIẢ ĐỊNH) -----
def getDbConnection():
    """Mock function for DB connection."""
    class MockConnection:
        def close(self): pass
    return MockConnection()

class DatabaseManager:
    """Quản lý dữ liệu sách, kho và kinh doanh (Mockup dùng list)."""
    def __init__(self, conn):
        self.conn = conn
        # Dữ liệu mẫu Sách
        self.mock_data = [
            (1, 'MS001', 'Nhà Giả Kim', 'Paulo Coelho', 'Tâm Lý', 'Sách Nước Ngoài', 'NXB Văn Học', 80.0, 100.0, 5, '1988'),
            (2, 'MS002', 'Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Trẻ', 95.5, 120.0, 10, '1936'),
            (3, 'MS003', 'Toán Cao Cấp A1', 'Nhiều Tác Giả', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 120.0, 150.0, 1, '2023'),
            (4, 'MS004', 'Lập Trình Python Cơ Bản', 'Nguyễn Văn A', 'CNTT', 'Sách Trong Nước', 'NXB Khoa Học', 250.0, 300.0, 2, '2022'),
            (5, 'MS005', 'Nghệ Thuật Bán Hàng', 'Jeffrey Gitomer', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Lao Động', 90.0, 130.0, 3, '2019'),
            (6, 'MS006', 'Vật Lý Đại Cương', 'Trần Văn B', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 110.0, 140.0, 1, '2023'),
        ]
        # Dữ liệu mẫu Tồn Kho
        self.mock_inventory = {
            1: (1, 'MS001', 'Nhà Giả Kim', 50, 'Kệ A1'),
            2: (2, 'MS002', 'Đắc Nhân Tâm', 150, 'Kệ A1'),
            3: (3, 'MS003', 'Toán Cao Cấp A1', 200, 'Kệ B2'),
            4: (4, 'MS004', 'Lập Trình Python Cơ Bản', 80, 'Kệ C3'),
            5: (5, 'MS005', 'Nghệ Thuật Bán Hàng', 100, 'Kệ D4'),
            6: (6, 'MS006', 'Vật Lý Đại Cương', 120, 'Kệ B2'),
        }
        self.last_book_id = len(self.mock_data)
        
        # Dữ liệu kinh doanh
        self.mock_invoices = []
        self.last_invoice_id = 0
        self.mock_invoice_details = []
        self.last_detail_id = 0
        self._generate_sample_invoices()

    def _generate_sample_invoices(self):
        """Tạo dữ liệu hóa đơn mẫu"""
        employees = ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D']
        statuses = ['Hoàn Thành', 'Hoàn Thành', 'Hoàn Thành', 'Đã Hủy']
        
        for i in range(50):
            self.last_invoice_id += 1
            days_ago = random.randint(0, 30)
            invoice_date = datetime.now() - timedelta(days=days_ago)
            date_str = invoice_date.strftime('%Y-%m-%d %H:%M:%S')
            invoice_code = f'HD{invoice_date.strftime("%Y%m%d")}{str(self.last_invoice_id).zfill(3)}'
            employee = random.choice(employees)
            status = random.choice(statuses)
            
            num_items = random.randint(1, 5)
            total_amount = 0
            
            for _ in range(num_items):
                self.last_detail_id += 1
                book = random.choice(self.mock_data)
                quantity = random.randint(1, 5)
                price = float(book[8])
                subtotal = quantity * price
                total_amount += subtotal
                
                detail = (self.last_detail_id, self.last_invoice_id, book[0], book[1], book[2], quantity, price, subtotal)
                self.mock_invoice_details.append(detail)
            
            invoice = (self.last_invoice_id, invoice_code, date_str, total_amount if status == 'Hoàn Thành' else 0, employee, status)
            self.mock_invoices.append(invoice)

    # BOOK OPERATIONS
    def view_all(self):
        time.sleep(0.1)
        return self.mock_data

    def search_for_suggestion(self, query):
        q = query.lower()
        return [row for row in self.mock_data if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()]

    def get_book_by_id(self, db_id):
        try:
            db_id = int(db_id)
            for row in self.mock_data:
                if row[0] == db_id:
                    return row
            return None
        except:
            return None

    def get_inventory_stats(self):
        return {"TotalCount": len(self.mock_data)}

    def insert_book_full(self, *values):
        self.last_book_id += 1
        new_book_db_id = self.last_book_id
        new_book_row = (new_book_db_id, values[0], values[1], values[2], values[3], values[4], values[5], float(values[6]), float(values[7]), int(values[8]), values[9])
        self.mock_data.append(new_book_row)
        self.mock_inventory[new_book_db_id] = (new_book_db_id, values[0], values[1], 0, 'Chưa xác định')
        return new_book_db_id

    def update_book_full(self, db_id, *values):
        for i, row in enumerate(self.mock_data):
            if row[0] == db_id:
                self.mock_data[i] = (db_id, values[0], values[1], values[2], values[3], values[4], values[5], float(values[6]), float(values[7]), int(values[8]), values[9])
                break
        if db_id in self.mock_inventory:
            current_inv = list(self.mock_inventory[db_id])
            current_inv[1] = values[0]
            current_inv[2] = values[1]
            self.mock_inventory[db_id] = tuple(current_inv)

    def delete_book(self, db_id):
        self.mock_data = [row for row in self.mock_data if row[0] != db_id]
        if db_id in self.mock_inventory:
            del self.mock_inventory[db_id]

    # INVENTORY OPERATIONS
    def view_inventory(self):
        time.sleep(0.1)
        return list(self.mock_inventory.values())

    def search_inventory_for_suggestion(self, query):
        q = query.lower()
        results = []
        for row in self.mock_inventory.values():
            if q in str(row[1]).lower() or q in str(row[2]).lower():
                results.append(row)
        return results

    def update_inventory_quantity(self, book_db_id, quantity_change, location):
        try:
            book_db_id = int(book_db_id)
            quantity_change = int(quantity_change)
        except ValueError:
            return False, "ID sách hoặc số lượng không hợp lệ."

        if book_db_id not in self.mock_inventory:
            return False, f"Không tìm thấy sách với ID CSDL: {book_db_id} trong kho."

        current_inventory = list(self.mock_inventory[book_db_id])
        current_quantity = current_inventory[3]
        new_quantity = current_quantity + quantity_change

        if new_quantity < 0:
            return False, f"Số lượng tồn kho không đủ ({current_quantity} < {-quantity_change})."

        current_inventory[3] = new_quantity
        current_inventory[4] = location if location else current_inventory[4]
        self.mock_inventory[book_db_id] = tuple(current_inventory)
        return True, new_quantity

    def get_inventory_record_by_id(self, db_id):
        try:
            db_id = int(db_id)
            return self.mock_inventory.get(db_id)
        except:
            return None

    # BUSINESS OPERATIONS
    def create_invoice(self, employee_name):
        self.last_invoice_id += 1
        invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        invoice_code = f'HD{datetime.now().strftime("%Y%m%d")}{str(self.last_invoice_id).zfill(3)}'
        invoice = (self.last_invoice_id, invoice_code, invoice_date, 0, employee_name, 'Đang Xử Lý')
        self.mock_invoices.append(invoice)
        return self.last_invoice_id, invoice_code

    def add_invoice_detail(self, invoice_id, book_id, quantity, price):
        self.last_detail_id += 1
        book = self.get_book_by_id(book_id)
        if not book:
            return False, "Không tìm thấy thông tin sách"
        
        subtotal = quantity * price
        detail = (self.last_detail_id, invoice_id, book_id, book[1], book[2], quantity, price, subtotal)
        self.mock_invoice_details.append(detail)
        
        for i, inv in enumerate(self.mock_invoices):
            if inv[0] == invoice_id:
                new_total = inv[3] + subtotal
                self.mock_invoices[i] = (inv[0], inv[1], inv[2], new_total, inv[4], inv[5])
                break
        
        return True, "Đã thêm sản phẩm"

    def get_invoice_details(self, invoice_id):
        return [d for d in self.mock_invoice_details if d[1] == invoice_id]

    def complete_invoice(self, invoice_id):
        details = self.get_invoice_details(invoice_id)
        
        for detail in details:
            book_id = detail[2]
            quantity = detail[5]
            if book_id in self.mock_inventory:
                current_qty = self.mock_inventory[book_id][3]
                if current_qty < quantity:
                    return False, f"Không đủ tồn kho {detail[4]}"
        
        for detail in details:
            book_id = detail[2]
            quantity = detail[5]
            if book_id in self.mock_inventory:
                self.update_inventory_quantity(book_id, -quantity, None)
        
        for i, inv in enumerate(self.mock_invoices):
            if inv[0] == invoice_id:
                self.mock_invoices[i] = (inv[0], inv[1], inv[2], inv[3], inv[4], 'Hoàn Thành')
                break
        
        return True, "Hoàn thành"

    def cancel_invoice(self, invoice_id):
        for i, inv in enumerate(self.mock_invoices):
            if inv[0] == invoice_id:
                self.mock_invoices[i] = (inv[0], inv[1], inv[2], 0, inv[4], 'Đã Hủy')
                self.mock_invoice_details = [d for d in self.mock_invoice_details if d[1] != invoice_id]
                return True, "Đã hủy"
        return False, "Không tìm thấy"

    def get_all_invoices(self):
        return sorted(self.mock_invoices, key=lambda x: x[2], reverse=True)

    def search_invoices(self, query):
        q = query.lower()
        return [inv for inv in self.mock_invoices if q in str(inv[1]).lower() or q in str(inv[4]).lower()]

    def get_business_stats(self, start_date=None, end_date=None):
        completed = [inv for inv in self.mock_invoices if inv[5] == 'Hoàn Thành']
        
        if start_date and end_date:
            completed = [inv for inv in completed if start_date <= inv[2] <= end_date]
        
        total_revenue = sum(inv[3] for inv in completed)
        total_invoices = len(completed)
        
        total_cost = 0
        for inv in completed:
            details = self.get_invoice_details(inv[0])
            for detail in details:
                book = self.get_book_by_id(detail[2])
                if book:
                    total_cost += detail[5] * float(book[7])
        
        profit = total_revenue - total_cost
        
        return {
            'TotalRevenue': total_revenue,
            'TotalCost': total_cost,
            'TotalProfit': profit,
            'TotalInvoices': total_invoices,
            'AvgInvoiceValue': total_revenue / total_invoices if total_invoices > 0 else 0
        }

    def get_top_selling_books(self, limit=5):
        book_sales = {}
        completed = [inv for inv in self.mock_invoices if inv[5] == 'Hoàn Thành']
        
        for inv in completed:
            details = self.get_invoice_details(inv[0])
            for detail in details:
                book_id = detail[2]
                if book_id not in book_sales:
                    book_sales[book_id] = {'quantity': 0, 'revenue': 0, 'book': detail}
                book_sales[book_id]['quantity'] += detail[5]
                book_sales[book_id]['revenue'] += detail[7]
        
        sorted_books = sorted(book_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)
        return sorted_books[:limit]

    def remove_invoice_detail(self, detail_id):
        for i, detail in enumerate(self.mock_invoice_details):
            if detail[0] == detail_id:
                invoice_id = detail[1]
                subtotal = detail[7]
                del self.mock_invoice_details[i]
                
                for j, inv in enumerate(self.mock_invoices):
                    if inv[0] == invoice_id:
                        new_total = inv[3] - subtotal
                        self.mock_invoices[j] = (inv[0], inv[1], inv[2], new_total, inv[4], inv[5])
                        break
                return True, "Đã xóa"
        return False, "Không tìm thấy"

# ----- HÀM HỖ TRỢ -----
def center_window(win, w, h):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

def format_currency(amount):
    return f"{amount:,.0f} đ"

# CLASS MENU CHÍNH
class MainMenuWindow:
    def __init__(self, master, login_window_instance, db_conn):
        self.master = master
        self.login_window = login_window_instance
        self.db_conn = db_conn
        master.title("💡 HỆ THỐNG TRUNG TÂM QUẢN LÝ")
        self.WIDTH = 550
        self.HEIGHT = 480
        center_window(master, self.WIDTH, self.HEIGHT)
        master.resizable(False, False)
        
        self.book_manager_instance = None
        self.inventory_manager_instance = None
        self.business_manager_instance = None
        
        self.setup_styles()
        self.setup_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MenuHeader.TLabel", font=('Arial', 28, 'bold'), foreground="#1E88E5", padding=20)
        style.configure("Menu.TButton", font=('Arial', 16, 'bold'), padding=15, width=28, relief="raised", borderwidth=0, foreground="#333333")
        
        style.configure("Business.Menu.TButton", background="#E8F5E9", foreground="#2E7D32")
        style.map("Business.Menu.TButton", background=[('active', '#C8E6C9')])
        
        style.configure("BookInfo.Menu.TButton", background="#E3F2FD", foreground="#1565C0")
        style.map("BookInfo.Menu.TButton", background=[('active', '#BBDEFB')])
        
        style.configure("Stock.Menu.TButton", background="#FFFDE7", foreground="#FFB300")
        style.map("Stock.Menu.TButton", background=[('active', '#FFF9C4')])
        
        style.configure("Exit.Menu.TButton", background="#FFEBEE", foreground="#C62828")
        style.map("Exit.Menu.TButton", background=[('active', '#FFCDD2')])

    def setup_widgets(self):
        main_frame = ttk.Frame(self.master, padding="30")
        main_frame.pack(expand=True, fill='both')
        main_frame.columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="TRUNG TÂM QUẢN LÝ", style="MenuHeader.TLabel").grid(row=0, column=0, pady=(10, 40))

        buttons_info = [
            ("📈 1. Quản lý kinh doanh", "Business.Menu.TButton", self.open_business_manager),
            ("📚 2. Quản lý thông tin sách", "BookInfo.Menu.TButton", self.open_book_manager),
            ("📦 3. Quản lý kho sách", "Stock.Menu.TButton", self.open_inventory_manager),
            ("Thoát Ứng dụng", "Exit.Menu.TButton", self.logout_to_login)
        ]

        for i, (text, style_name, command) in enumerate(buttons_info):
            ttk.Button(main_frame, text=text, command=command, style=style_name).grid(row=i + 1, column=0, pady=12, sticky='ew')

    def open_business_manager(self):
        self.master.withdraw()
        if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
            self.book_manager_instance.master.withdraw()
        if self.inventory_manager_instance and self.inventory_manager_instance.master.winfo_exists():
            self.inventory_manager_instance.master.withdraw()
        
        if not self.business_manager_instance or not self.business_manager_instance.master.winfo_exists():
            business_window = tk.Toplevel(self.master)
            business_window.protocol("WM_DELETE_WINDOW", self.close_business_manager)
            self.business_manager_instance = BusinessManagerApp(business_window, self, self.db_conn)
            center_window(business_window, 1400, 800)
        else:
            self.business_manager_instance.master.deiconify()
        self.business_manager_instance.refresh_all_data()

    def close_business_manager(self):
        if self.business_manager_instance and self.business_manager_instance.master.winfo_exists():
            self.business_manager_instance.master.withdraw()
        self.master.deiconify()

    def open_book_manager(self):
        self.master.withdraw()
        if self.inventory_manager_instance and self.inventory_manager_instance.master.winfo_exists():
            self.inventory_manager_instance.master.withdraw()
        if self.business_manager_instance and self.business_manager_instance.master.winfo_exists():
            self.business_manager_instance.master.withdraw()
        
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

    def open_inventory_manager(self):
        self.master.withdraw()
        if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
            self.book_manager_instance.master.withdraw()
        if self.business_manager_instance and self.business_manager_instance.master.winfo_exists():
            self.business_manager_instance.master.withdraw()
        
        if not self.inventory_manager_instance or not self.inventory_manager_instance.master.winfo_exists():
            inventory_window = tk.Toplevel(self.master)
            inventory_window.protocol("WM_DELETE_WINDOW", self.close_inventory_manager)
            self.inventory_manager_instance = InventoryManagerApp(inventory_window, self, self.db_conn)
            center_window(inventory_window, 1000, 650)
        else:
            self.inventory_manager_instance.master.deiconify()
        self.inventory_manager_instance.view_inventory_command()

    def close_inventory_manager(self):
        if self.inventory_manager_instance and self.inventory_manager_instance.master.winfo_exists():
            self.inventory_manager_instance.master.withdraw()
        self.master.deiconify()

    def logout_to_login(self):
        if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
            self.book_manager_instance.master.destroy()
        if self.inventory_manager_instance and self.inventory_manager_instance.master.winfo_exists():
            self.inventory_manager_instance.master.destroy()
        if self.business_manager_instance and self.business_manager_instance.master.winfo_exists():
            self.business_manager_instance.master.destroy()
        
        self.master.destroy()
        self.login_window.master.deiconify()
        self.login_window.master.focus_set()

# CLASS ĐĂNG NHẬP
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
                messagebox.showerror("Lỗi CSDL", "Không thể kết nối đến cơ sở dữ liệu.")
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

# CLASS QUẢN LÝ KINH DOANH
class BusinessManagerApp:
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📈 HỆ THỐNG QUẢN LÝ KINH DOANH")
        
        self.current_invoice_id = None
        self.current_employee = "Nguyễn Văn A"
        
        self.apply_styles()
        self.setup_widgets()
        self.refresh_all_data()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4CAF50", foreground="white", padding=[5, 5])
        style.configure("Treeview", font=('Arial', 9), rowheight=23, bordercolor="#E0E0E0", borderwidth=1, relief="flat", fieldbackground="#F9FBE7")
        style.map('Treeview', background=[('selected', '#8BC34A')])
        
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Bold.TLabel", font=('Arial', 11, 'bold'), foreground="#333333")
        style.configure("Header.TLabel", font=('Arial', 13, 'bold'), foreground="#2E7D32")
        
        style.configure("Unified.TButton", font=('Arial', 10, 'bold'), padding=(8, 6), foreground="white")
        style.configure("Create.TButton", background="#4CAF50")
        style.map("Create.TButton", background=[('active', '#43A047')])
        style.configure("Add.TButton", background="#2196F3")
        style.map("Add.TButton", background=[('active', '#1E88E5')])
        style.configure("Complete.TButton", background="#FF9800")
        style.map("Complete.TButton", background=[('active', '#FB8C00')])
        style.configure("Cancel.TButton", background="#F44336")
        style.map("Cancel.TButton", background=[('active', '#E53935')])
        style.configure("View.TButton", background="#9E9E9E")
        style.map("View.TButton", background=[('active', '#757575')])
        style.configure("Back.TButton", background="#795548")
        style.map("Back.TButton", background=[('active', '#6D4C41')])

    def setup_widgets(self):
        main_notebook = ttk.Notebook(self.master)
        main_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TAB 1: BÁN HÀNG
        sale_frame = ttk.Frame(main_notebook, padding="10")
        main_notebook.add(sale_frame, text="🛒 BÁN HÀNG")
        self.setup_sale_tab(sale_frame)
        
        # TAB 2: QUẢN LÝ HÓA ĐƠN
        invoice_frame = ttk.Frame(main_notebook, padding="10")
        main_notebook.add(invoice_frame, text="📋 QUẢN LÝ HÓA ĐƠN")
        self.setup_invoice_tab(invoice_frame)
        
        # TAB 3: THỐNG KÊ
        stats_frame = ttk.Frame(main_notebook, padding="10")
        main_notebook.add(stats_frame, text="📊 THỐNG KÊ")
        self.setup_stats_tab(stats_frame)

    def setup_sale_tab(self, parent):
        # Chia làm 2 phần: Trái (Chọn sách) và Phải (Hóa đơn)
        paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # PHẦN TRÁI: CHỌN SÁCH
        left_frame = ttk.Frame(paned, padding="5")
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="DANH SÁCH SÁCH", style="Header.TLabel").pack(pady=(0, 10))
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=(0, 5))
        self.sale_search_var = tk.StringVar()
        self.sale_search_var.trace_add("write", self.filter_books_for_sale)
        ttk.Entry(search_frame, textvariable=self.sale_search_var, width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Treeview sách
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.books_tree = ttk.Treeview(tree_frame, columns=("ID", "MaSach", "TenSach", "GiaBan", "TonKho"), show='headings', height=20)
        self.books_tree.column("ID", width=40, anchor='center')
        self.books_tree.column("MaSach", width=80, anchor='center')
        self.books_tree.column("TenSach", width=250, anchor='w')
        self.books_tree.column("GiaBan", width=80, anchor='e')
        self.books_tree.column("TonKho", width=70, anchor='center')
        
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("MaSach", text="Mã Sách")
        self.books_tree.heading("TenSach", text="Tên Sách")
        self.books_tree.heading("GiaBan", text="Giá Bán")
        self.books_tree.heading("TonKho", text="Tồn Kho")
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=vsb.set)
        self.books_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.books_tree.bind('<Double-Button-1>', self.add_book_to_invoice)
        
        # PHẦN PHẢI: HÓA ĐƠN
        right_frame = ttk.Frame(paned, padding="5")
        paned.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="HÓA ĐƠN BÁN HÀNG", style="Header.TLabel").pack(pady=(0, 10))
        
        # Thông tin hóa đơn
        info_frame = ttk.LabelFrame(right_frame, text=" Thông Tin Hóa Đơn ", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill=tk.X)
        info_grid.columnconfigure(1, weight=1)
        
        ttk.Label(info_grid, text="Mã HĐ:", style="Bold.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=3)
        self.invoice_code_var = tk.StringVar(value="---")
        ttk.Label(info_grid, textvariable=self.invoice_code_var, foreground="#2196F3", font=('Arial', 11, 'bold')).grid(row=0, column=1, sticky='w', padx=5, pady=3)
        
        ttk.Label(info_grid, text="Nhân viên:", style="Bold.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=3)
        ttk.Label(info_grid, text=self.current_employee).grid(row=1, column=1, sticky='w', padx=5, pady=3)
        
        ttk.Label(info_grid, text="Tổng tiền:", style="Bold.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=3)
        self.total_amount_var = tk.StringVar(value="0 đ")
        ttk.Label(info_grid, textvariable=self.total_amount_var, foreground="#F44336", font=('Arial', 13, 'bold')).grid(row=2, column=1, sticky='w', padx=5, pady=3)
        
        # Chi tiết hóa đơn
        detail_frame = ttk.LabelFrame(right_frame, text=" Chi Tiết Hóa Đơn ", padding="5")
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.invoice_detail_tree = ttk.Treeview(detail_frame, columns=("STT", "MaSach", "TenSach", "SL", "DonGia", "ThanhTien"), show='headings', height=10)
        self.invoice_detail_tree.column("STT", width=40, anchor='center')
        self.invoice_detail_tree.column("MaSach", width=80, anchor='center')
        self.invoice_detail_tree.column("TenSach", width=180, anchor='w')
        self.invoice_detail_tree.column("SL", width=50, anchor='center')
        self.invoice_detail_tree.column("DonGia", width=80, anchor='e')
        self.invoice_detail_tree.column("ThanhTien", width=90, anchor='e')
        
        self.invoice_detail_tree.heading("STT", text="STT")
        self.invoice_detail_tree.heading("MaSach", text="Mã")
        self.invoice_detail_tree.heading("TenSach", text="Tên Sách")
        self.invoice_detail_tree.heading("SL", text="SL")
        self.invoice_detail_tree.heading("DonGia", text="Đơn Giá")
        self.invoice_detail_tree.heading("ThanhTien", text="Thành Tiền")
        
        vsb2 = ttk.Scrollbar(detail_frame, orient="vertical", command=self.invoice_detail_tree.yview)
        self.invoice_detail_tree.configure(yscrollcommand=vsb2.set)
        self.invoice_detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="➕ Tạo Hóa Đơn Mới", command=self.create_new_invoice, style="Create.TButton").pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(button_frame, text="✅ Hoàn Thành", command=self.complete_current_invoice, style="Complete.TButton").pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(button_frame, text="❌ Hủy HĐ", command=self.cancel_current_invoice, style="Cancel.TButton").pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(button_frame, text="🗑️ Xóa Dòng", command=self.remove_invoice_line, style="Cancel.TButton").pack(side=tk.LEFT, padx=2, pady=5)

    def setup_invoice_tab(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_frame, text="QUẢN LÝ HÓA ĐƠN", style="Header.TLabel").pack(side=tk.LEFT, padx=10)
        
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.invoice_search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.invoice_search_var, width=25).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="🔍", command=self.search_invoices_action, style="View.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🔄 Tải Lại", command=self.load_all_invoices, style="View.TButton").pack(side=tk.LEFT)
        
        # Treeview hóa đơn
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.invoices_tree = ttk.Treeview(tree_frame, columns=("ID", "MaHD", "NgayBan", "TongTien", "NhanVien", "TrangThai"), show='headings', height=25)
        self.invoices_tree.column("ID", width=50, anchor='center')
        self.invoices_tree.column("MaHD", width=150, anchor='center')
        self.invoices_tree.column("NgayBan", width=150, anchor='center')
        self.invoices_tree.column("TongTien", width=120, anchor='e')
        self.invoices_tree.column("NhanVien", width=150, anchor='w')
        self.invoices_tree.column("TrangThai", width=120, anchor='center')
        
        self.invoices_tree.heading("ID", text="ID")
        self.invoices_tree.heading("MaHD", text="Mã Hóa Đơn")
        self.invoices_tree.heading("NgayBan", text="Ngày Bán")
        self.invoices_tree.heading("TongTien", text="Tổng Tiền")
        self.invoices_tree.heading("NhanVien", text="Nhân Viên")
        self.invoices_tree.heading("TrangThai", text="Trạng Thái")
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.invoices_tree.yview)
        self.invoices_tree.configure(yscrollcommand=vsb.set)
        self.invoices_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.invoices_tree.bind('<Double-Button-1>', self.view_invoice_detail)
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="👁️ Xem Chi Tiết", command=self.view_invoice_detail, style="View.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⬅️ Quay Lại Menu", command=self.main_menu.close_business_manager, style="Back.TButton").pack(side=tk.RIGHT, padx=5)

    def setup_stats_tab(self, parent):
        ttk.Label(parent, text="THỐNG KÊ KINH DOANH", style="Header.TLabel").pack(pady=10)
        
        # Khung thống kê tổng quan
        stats_frame = ttk.LabelFrame(parent, text=" Thống Kê Tổng Quan ", padding="20")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()
        
        # Doanh thu
        revenue_frame = ttk.Frame(stats_grid, relief="solid", borderwidth=1, padding=15)
        revenue_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        ttk.Label(revenue_frame, text="💰 TỔNG DOANH THU", font=('Arial', 11, 'bold'), foreground="#4CAF50").pack()
        self.total_revenue_var = tk.StringVar(value="0 đ")
        ttk.Label(revenue_frame, textvariable=self.total_revenue_var, font=('Arial', 16, 'bold'), foreground="#4CAF50").pack(pady=5)
        
        # Chi phí
        cost_frame = ttk.Frame(stats_grid, relief="solid", borderwidth=1, padding=15)
        cost_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        ttk.Label(cost_frame, text="💸 TỔNG CHI PHÍ", font=('Arial', 11, 'bold'), foreground="#FF9800").pack()
        self.total_cost_var = tk.StringVar(value="0 đ")
        ttk.Label(cost_frame, textvariable=self.total_cost_var, font=('Arial', 16, 'bold'), foreground="#FF9800").pack(pady=5)
        
        # Lợi nhuận
        profit_frame = ttk.Frame(stats_grid, relief="solid", borderwidth=1, padding=15)
        profit_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        ttk.Label(profit_frame, text="📈 LỢI NHUẬN", font=('Arial', 11, 'bold'), foreground="#2196F3").pack()
        self.total_profit_var = tk.StringVar(value="0 đ")
        ttk.Label(profit_frame, textvariable=self.total_profit_var, font=('Arial', 16, 'bold'), foreground="#2196F3").pack(pady=5)
        
        # Số đơn hàng
        orders_frame = ttk.Frame(stats_grid, relief="solid", borderwidth=1, padding=15)
        orders_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        ttk.Label(orders_frame, text="📋 SỐ HÓA ĐƠN", font=('Arial', 11, 'bold'), foreground="#9C27B0").pack()
        self.total_orders_var = tk.StringVar(value="0")
        ttk.Label(orders_frame, textvariable=self.total_orders_var, font=('Arial', 16, 'bold'), foreground="#9C27B0").pack(pady=5)
        
        # Giá trị TB
        avg_frame = ttk.Frame(stats_grid, relief="solid", borderwidth=1, padding=15)
        avg_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        ttk.Label(avg_frame, text="📊 GIÁ TRỊ TB/HÓA ĐƠN", font=('Arial', 11, 'bold'), foreground="#FF5722").pack()
        self.avg_invoice_var = tk.StringVar(value="0 đ")
        ttk.Label(avg_frame, textvariable=self.avg_invoice_var, font=('Arial', 16, 'bold'), foreground="#FF5722").pack(pady=5)
        
        # Top sách bán chạy
        top_frame = ttk.LabelFrame(parent, text=" Top 5 Sách Bán Chạy ", padding="10")
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.top_books_tree = ttk.Treeview(top_frame, columns=("STT", "MaSach", "TenSach", "SoLuong", "DoanhThu"), show='headings', height=8)
        self.top_books_tree.column("STT", width=50, anchor='center')
        self.top_books_tree.column("MaSach", width=100, anchor='center')
        self.top_books_tree.column("TenSach", width=350, anchor='w')
        self.top_books_tree.column("SoLuong", width=100, anchor='center')
        self.top_books_tree.column("DoanhThu", width=150, anchor='e')
        
        self.top_books_tree.heading("STT", text="STT")
        self.top_books_tree.heading("MaSach", text="Mã Sách")
        self.top_books_tree.heading("TenSach", text="Tên Sách")
        self.top_books_tree.heading("SoLuong", text="SL Bán")
        self.top_books_tree.heading("DoanhThu", text="Doanh Thu")
        
        self.top_books_tree.pack(fill=tk.BOTH, expand=True)

    def filter_books_for_sale(self, *args):
        query = self.sale_search_var.get().strip().lower()
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        books = self.db.view_all()
        for book in books:
            book_id = book[0]
            if book_id in self.db.mock_inventory:
                inventory = self.db.mock_inventory[book_id]
                stock = inventory[3]
                
                if not query or query in str(book[1]).lower() or query in str(book[2]).lower():
                    self.books_tree.insert('', tk.END, values=(
                        book[0],
                        book[1],
                        book[2],
                        format_currency(book[8]),
                        stock
                    ))

    def create_new_invoice(self):
        if self.current_invoice_id:
            if not messagebox.askyesno("Xác nhận", "Bạn có hóa đơn đang xử lý. Tạo hóa đơn mới sẽ hủy hóa đơn hiện tại. Tiếp tục?"):
                return
            self.db.cancel_invoice(self.current_invoice_id)
        
        self.current_invoice_id, invoice_code = self.db.create_invoice(self.current_employee)
        self.invoice_code_var.set(invoice_code)
        self.total_amount_var.set("0 đ")
        
        for item in self.invoice_detail_tree.get_children():
            self.invoice_detail_tree.delete(item)
        
        messagebox.showinfo("Thành công", f"Đã tạo hóa đơn mới: {invoice_code}")

    def add_book_to_invoice(self, event=None):
        if not self.current_invoice_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo hóa đơn mới trước!")
            return
        
        selected = self.books_tree.selection()
        if not selected:
            return
        
        values = self.books_tree.item(selected[0])['values']
        book_id = values[0]
        book_name = values[2]
        price_str = values[3]
        stock = values[4]
        
        if stock <= 0:
            messagebox.showwarning("Cảnh báo", f"Sách '{book_name}' đã hết hàng!")
            return
        
        # Hỏi số lượng
        quantity_window = tk.Toplevel(self.master)
        quantity_window.title("Nhập Số Lượng")
        quantity_window.geometry("300x150")
        quantity_window.transient(self.master)
        quantity_window.grab_set()
        
        ttk.Label(quantity_window, text=f"Sách: {book_name}", font=('Arial', 10, 'bold')).pack(pady=10)
        ttk.Label(quantity_window, text=f"Tồn kho: {stock}", foreground="#F44336").pack()
        
        frame = ttk.Frame(quantity_window)
        frame.pack(pady=10)
        ttk.Label(frame, text="Số lượng:").pack(side=tk.LEFT, padx=5)
        quantity_var = tk.StringVar(value="1")
        entry = ttk.Entry(frame, textvariable=quantity_var, width=10)
        entry.pack(side=tk.LEFT)
        entry.focus()
        
        def confirm():
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    messagebox.showwarning("Cảnh báo", "Số lượng phải lớn hơn 0!")
                    return
                if quantity > stock:
                    messagebox.showwarning("Cảnh báo", f"Số lượng vượt quá tồn kho ({stock})!")
                    return
                
                price = float(price_str.replace(' đ', '').replace(',', ''))
                success, msg = self.db.add_invoice_detail(self.current_invoice_id, book_id, quantity, price)
                
                if success:
                    quantity_window.destroy()
                    self.refresh_invoice_detail()
                else:
                    messagebox.showerror("Lỗi", msg)
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Số lượng không hợp lệ!")
        
        ttk.Button(quantity_window, text="Xác Nhận", command=confirm, style="Create.TButton").pack(pady=10)
        quantity_window.bind('<Return>', lambda e: confirm())

    def refresh_invoice_detail(self):
        if not self.current_invoice_id:
            return
        
        for item in self.invoice_detail_tree.get_children():
            self.invoice_detail_tree.delete(item)
        
        details = self.db.get_invoice_details(self.current_invoice_id)
        total = 0
        
        for idx, detail in enumerate(details, 1):
            self.invoice_detail_tree.insert('', tk.END, values=(
                idx,
                detail[3],
                detail[4],
                detail[5],
                format_currency(detail[6]),
                format_currency(detail[7])
            ), tags=(detail[0],))
            total += detail[7]
        
        self.total_amount_var.set(format_currency(total))

    def remove_invoice_line(self):
        selected = self.invoice_detail_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
        
        detail_id = self.invoice_detail_tree.item(selected[0])['tags'][0]
        success, msg = self.db.remove_invoice_detail(detail_id)
        
        if success:
            self.refresh_invoice_detail()
        else:
            messagebox.showerror("Lỗi", msg)

    def complete_current_invoice(self):
        if not self.current_invoice_id:
            messagebox.showwarning("Cảnh báo", "Không có hóa đơn nào đang xử lý!")
            return
        
        details = self.db.get_invoice_details(self.current_invoice_id)
        if not details:
            messagebox.showwarning("Cảnh báo", "Hóa đơn chưa có sản phẩm nào!")
            return
        
        if not messagebox.askyesno("Xác nhận", "Hoàn thành hóa đơn này?"):
            return
        
        success, msg = self.db.complete_invoice(self.current_invoice_id)
        
        if success:
            messagebox.showinfo("Thành công", "Hóa đơn đã hoàn thành!")
            self.current_invoice_id = None
            self.invoice_code_var.set("---")
            self.total_amount_var.set("0 đ")
            for item in self.invoice_detail_tree.get_children():
                self.invoice_detail_tree.delete(item)
            self.refresh_all_data()
        else:
            messagebox.showerror("Lỗi", msg)

    def cancel_current_invoice(self):
        if not self.current_invoice_id:
            messagebox.showwarning("Cảnh báo", "Không có hóa đơn nào đang xử lý!")
            return
        
        if not messagebox.askyesno("Xác nhận", "Hủy hóa đơn này?"):
            return
        
        self.db.cancel_invoice(self.current_invoice_id)
        self.current_invoice_id = None
        self.invoice_code_var.set("---")
        self.total_amount_var.set("0 đ")
        for item in self.invoice_detail_tree.get_children():
            self.invoice_detail_tree.delete(item)
        messagebox.showinfo("Thành công", "Đã hủy hóa đơn!")

    def load_all_invoices(self):
        for item in self.invoices_tree.get_children():
            self.invoices_tree.delete(item)
        
        invoices = self.db.get_all_invoices()
        for inv in invoices:
            self.invoices_tree.insert('', tk.END, values=(
                inv[0],
                inv[1],
                inv[2],
                format_currency(inv[3]),
                inv[4],
                inv[5]
            ))

    def search_invoices_action(self):
        query = self.invoice_search_var.get().strip()
        if not query:
            self.load_all_invoices()
            return
        
        for item in self.invoices_tree.get_children():
            self.invoices_tree.delete(item)
        
        invoices = self.db.search_invoices(query)
        for inv in invoices:
            self.invoices_tree.insert('', tk.END, values=(
                inv[0],
                inv[1],
                inv[2],
                format_currency(inv[3]),
                inv[4],
                inv[5]
            ))

    def view_invoice_detail(self, event=None):
        selected = self.invoices_tree.selection()
        if not selected:
            return
        
        values = self.invoices_tree.item(selected[0])['values']
        invoice_id = values[0]
        
        detail_window = tk.Toplevel(self.master)
        detail_window.title(f"Chi Tiết Hóa Đơn - {values[1]}")
        detail_window.geometry("700x500")
        detail_window.transient(self.master)
        detail_window.grab_set()
        
        main_frame = ttk.Frame(detail_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Thông tin hóa đơn
        info_frame = ttk.LabelFrame(main_frame, text=" Thông Tin Hóa Đơn ", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_grid = ttk.Frame(info_frame)
        info_grid.pack()
        info_grid.columnconfigure(1, weight=1)
        info_grid.columnconfigure(3, weight=1)
        
        ttk.Label(info_grid, text="Mã HĐ:", style="Bold.TLabel").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        ttk.Label(info_grid, text=values[1], foreground="#2196F3").grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Label(info_grid, text="Ngày:", style="Bold.TLabel").grid(row=0, column=2, sticky='w', padx=10, pady=5)
        ttk.Label(info_grid, text=values[2]).grid(row=0, column=3, sticky='w', padx=10, pady=5)
        
        ttk.Label(info_grid, text="Nhân viên:", style="Bold.TLabel").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        ttk.Label(info_grid, text=values[4]).grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Label(info_grid, text="Trạng thái:", style="Bold.TLabel").grid(row=1, column=2, sticky='w', padx=10, pady=5)
        status_color = "#4CAF50" if values[5] == "Hoàn Thành" else "#F44336"
        ttk.Label(info_grid, text=values[5], foreground=status_color, font=('Arial', 10, 'bold')).grid(row=1, column=3, sticky='w', padx=10, pady=5)
        
        ttk.Label(info_grid, text="Tổng tiền:", style="Bold.TLabel").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        ttk.Label(info_grid, text=values[3], foreground="#F44336", font=('Arial', 12, 'bold')).grid(row=2, column=1, columnspan=3, sticky='w', padx=10, pady=5)
        
        # Chi tiết sản phẩm
        detail_frame = ttk.LabelFrame(main_frame, text=" Chi Tiết Sản Phẩm ", padding="10")
        detail_frame.pack(fill=tk.BOTH, expand=True)
        
        detail_tree = ttk.Treeview(detail_frame, columns=("STT", "MaSach", "TenSach", "SL", "DonGia", "ThanhTien"), show='headings', height=12)
        detail_tree.column("STT", width=50, anchor='center')
        detail_tree.column("MaSach", width=80, anchor='center')
        detail_tree.column("TenSach", width=250, anchor='w')
        detail_tree.column("SL", width=60, anchor='center')
        detail_tree.column("DonGia", width=90, anchor='e')
        detail_tree.column("ThanhTien", width=100, anchor='e')
        
        detail_tree.heading("STT", text="STT")
        detail_tree.heading("MaSach", text="Mã Sách")
        detail_tree.heading("TenSach", text="Tên Sách")
        detail_tree.heading("SL", text="SL")
        detail_tree.heading("DonGia", text="Đơn Giá")
        detail_tree.heading("ThanhTien", text="Thành Tiền")
        
        vsb = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_tree.yview)
        detail_tree.configure(yscrollcommand=vsb.set)
        detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        details = self.db.get_invoice_details(invoice_id)
        for idx, detail in enumerate(details, 1):
            detail_tree.insert('', tk.END, values=(
                idx,
                detail[3],
                detail[4],
                detail[5],
                format_currency(detail[6]),
                format_currency(detail[7])
            ))
        
        ttk.Button(main_frame, text="Đóng", command=detail_window.destroy, style="View.TButton").pack(pady=10)

    def refresh_stats(self):
        stats = self.db.get_business_stats()
        
        self.total_revenue_var.set(format_currency(stats['TotalRevenue']))
        self.total_cost_var.set(format_currency(stats['TotalCost']))
        self.total_profit_var.set(format_currency(stats['TotalProfit']))
        self.total_orders_var.set(f"{stats['TotalInvoices']} đơn")
        self.avg_invoice_var.set(format_currency(stats['AvgInvoiceValue']))
        
        # Top sách bán chạy
        for item in self.top_books_tree.get_children():
            self.top_books_tree.delete(item)
        
        top_books = self.db.get_top_selling_books(5)
        for idx, (book_id, data) in enumerate(top_books, 1):
            self.top_books_tree.insert('', tk.END, values=(
                idx,
                data['book'][3],
                data['book'][4],
                data['quantity'],
                format_currency(data['revenue'])
            ))

    def refresh_all_data(self):
        self.filter_books_for_sale()
        self.load_all_invoices()
        self.refresh_stats()

# CLASS QUẢN LÝ SÁCH (GIỮ NGUYÊN)
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
        style.configure("Treeview", font=('Arial', 10), rowheight=25, bordercolor="#E0E0E0", borderwidth=1, relief="flat", fieldbackground="#F5F5F5")
        style.map('Treeview', background=[('selected', '#4CAF50')])
        
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("TCombobox", font=('Arial', 11), padding=2)
        style.configure("TSeparator", background="#CCCCCC")
        
        style.configure("Unified.TButton", font=('Arial', 11, 'bold'), padding=(10, 8), foreground="white")
        style.configure("Add.Unified.TButton", background="#4CAF50")
        style.map("Add.Unified.TButton", background=[('active', '#43A047')])
        style.configure("Update.Unified.TButton", background="#2196F3")
        style.map("Update.Unified.TButton", background=[('active', '#1E88E5')])
        style.configure("Delete.Unified.TButton", background="#F44336")
        style.map("Delete.Unified.TButton", background=[('active', '#E53935')])
        style.configure("Search.Unified.TButton", background="#FFC107")
        style.map("Search.Unified.TButton", background=[('active', '#FFB300')])
        style.configure("View.Unified.TButton", background="#9E9E9E")
        style.map("View.Unified.TButton", background=[('active', '#757575')])
        style.configure("Clear.Unified.TButton", background="#BDBDBD")
        style.map("Clear.Unified.TButton", background=[('active', '#A0A0A0')])
        style.configure("Logout.Unified.TButton", background="#795548")
        style.map("Logout.Unified.TButton", background=[('active', '#6D4C41')])

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
            ("MÃ SÁCH:", self.book_id_text, 0, 0),
            ("TÊN SÁCH:", self.book_name_text, 0, 2),
            ("TÁC GIẢ:", self.author_text, 1, 0),
            ("LĨNH VỰC:", self.field_text, 1, 2),
            ("LOẠI SÁCH:", self.book_type_text, 2, 0, True),
            ("NXB:", self.publisher_name_text, 2, 2),
            ("GIÁ MUA:", self.buy_price_text, 3, 0),
            ("GIÁ BÌA:", self.cover_price_text, 3, 2),
            ("LẦN TÁI BẢN:", self.reprint_text, 4, 0),
            ("NĂM XB:", self.publish_year_text, 4, 2)
        ]
        
        for text, var, row, col, *is_combo in input_data:
            ttk.Label(input_group, text=text, style="Input.TLabel").grid(row=row, column=col, sticky=W, padx=10, pady=5)
            if is_combo and is_combo[0]:
                ttk.Combobox(input_group, textvariable=var, values=self.BOOK_TYPES, state="readonly", width=30).grid(row=row, column=col+1, padx=(0, 10), pady=5, sticky='ew')
            else:
                ttk.Entry(input_group, textvariable=var, width=35).grid(row=row, column=col+1, padx=(0, 10), pady=5, sticky='ew')
        
        button_group = ttk.Frame(control_frame, padding="10")
        button_group.grid(row=0, column=1, rowspan=2, sticky=N+S, padx=(10, 0))
        button_group.grid_columnconfigure(0, weight=1)
        
        buttons_info = [
            ("➕ THÊM MỚI", self.add_command, "Add.Unified.TButton"),
            ("🔄 CẬP NHẬT", self.update_command, "Update.Unified.TButton"),
            ("❌ XÓA SÁCH", self.delete_command, "Delete.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("🔍 TÌM KIẾM", self.search_command, "Search.Unified.TButton"),
            ("🔄 TẢI LẠI", self.view_command, "View.Unified.TButton"),
            ("🧹 XÓA FORM", self.clear_form, "Clear.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("⬅️ QUAY LẠI MENU", self.main_menu.close_book_manager, "Logout.Unified.TButton")
        ]
        
        row_index = 0
        for text, command, style_name in buttons_info:
            if text == "---":
                ttk.Separator(button_group, orient='horizontal').grid(row=row_index, column=0, sticky='ew', pady=10)
            else:
                ttk.Button(button_group, text=text, command=command, style=style_name).grid(row=row_index, column=0, padx=5, pady=4, sticky='ew')
            row_index += 1
        
        info_group = ttk.LabelFrame(control_frame, text=" THÔNG TIN TỔNG QUAN ", padding="15")
        info_group.grid(row=1, column=0, sticky=N+E+S+W, padx=(0, 10), pady=(5, 0))
        info_group.columnconfigure(1, weight=1)
        
        ttk.Label(info_group, text="Tổng số đầu sách:", style="Input.TLabel").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.total_books_var, font=('Arial', 12, 'bold'), foreground="#F44336").grid(row=0, column=1, sticky=W, padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.status_var, font=('Arial', 9), foreground="#666666").grid(row=1, column=0, columnspan=2, sticky=W, padx=10, pady=(5, 0))
        
        list_frame = ttk.Frame(main_pane, padding="10")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        main_pane.add(list_frame, weight=1)
        
        all_column_ids = ["ID", "MaSach", "TenSach", "TenTacGia", "TenLinhVuc", "LoaiSach", "TenNXB", "GiaMua", "GiaBia", "LanTaiBan", "NamXB"]
        self.books_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")
        
        column_configs = [
            ("ID", 50, 'center'), ("MaSach", 80, 'center'), ("TenSach", 250, 'w'), ("TenTacGia", 150, 'w'),
            ("TenLinhVuc", 100, 'w'), ("LoaiSach", 100, 'w'), ("TenNXB", 120, 'w'), ("GiaMua", 80, 'e'),
            ("GiaBia", 80, 'e'), ("LanTaiBan", 60, 'center'), ("NamXB", 60, 'center')
        ]
        
        for col_id, width, anchor in column_configs:
            self.books_list.column(col_id, width=width, anchor=anchor)
            self.books_list.heading(col_id, text=col_id.replace("NamXB", "Năm XB").replace("LanTaiBan", "Tái Bản").replace("TenNXB", "Tên NXB").replace("GiaMua", "Giá Mua").replace("GiaBia", "Giá Bìa").replace("TenLinhVuc", "Lĩnh Vực").replace("TenTacGia", "Tác Giả").replace("TenSach", "Tên Sách").replace("MaSach", "Mã Sách"), anchor='center')
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_list.yview)
        self.books_list.configure(yscrollcommand=vsb.set)
        self.books_list.grid(row=0, column=0, sticky=N+E+S+W)
        vsb.grid(row=0, column=1, sticky='ns')
        
        self.books_list.bind('<ButtonRelease-1>', self.get_selected_row)

    def fill_form_with_data(self, row_data):
        self.selected_book = row_data
        self.book_id_text.set(row_data[1] if row_data[1] is not None else "")
        self.book_name_text.set(row_data[2] if row_data[2] is not None else "")
        self.author_text.set(row_data[3] if row_data[3] is not None else "")
        self.field_text.set(row_data[4] if row_data[4] is not None else "")
        self.book_type_text.set(row_data[5] if row_data[5] is not None else "")
        self.publisher_name_text.set(row_data[6] if row_data[6] is not None else "")
        self.buy_price_text.set(row_data[7] if row_data[7] is not None else "0.0")
        self.cover_price_text.set(row_data[8] if row_data[8] is not None else "0.0")
        self.reprint_text.set(row_data[9] if row_data[9] is not None else "0")
        self.publish_year_text.set(row_data[10] if row_data[10] is not None else "")

    def select_row_by_db_id(self, db_id_to_select):
        db_id_to_select = str(db_id_to_select)
        found_item = None
        if self.books_list.selection():
            self.books_list.selection_remove(self.books_list.selection())
        
        for item in self.books_list.get_children():
            if str(self.books_list.item(item, 'values')[0]) == db_id_to_select:
                found_item = item
                break
        
        if found_item:
            self.books_list.selection_set(found_item)
            self.books_list.focus(found_item)
            self.books_list.see(found_item)

    def clear_form(self):
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.author_text.set("")
        self.field_text.set("")
        self.book_type_text.set("")
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
        self.books_list.selection_set(selected_item)
        values = self.books_list.item(selected_item, 'values')
        self.fill_form_with_data(values)

    def view_command(self):
        try:
            self.clear_form()
            for item in self.books_list.get_children():
                self.books_list.delete(item)
            
            data = self.db.view_all()
            for row in data:
                self.books_list.insert('', tk.END, values=row)
            
            stats = self.db.get_inventory_stats()
            self.total_books_var.set(f"{stats['TotalCount']} đầu sách")
            self.status_var.set("Tải lại dữ liệu hoàn tất.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")
            self.total_books_var.set("LỖI KẾT NỐI!")
            self.status_var.set("Kết nối CSDL: Lỗi")

    def get_all_input_values(self):
        return (
            self.book_id_text.get().strip(), self.book_name_text.get().strip(), self.author_text.get().strip(),
            self.field_text.get().strip(), self.book_type_text.get().strip(), self.publisher_name_text.get().strip(),
            self.buy_price_text.get().strip(), self.cover_price_text.get().strip(), self.reprint_text.get().strip(),
            self.publish_year_text.get().strip()
        )

    def validate_input(self, values):
        if not all(values[:6]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đủ thông tin cơ bản: Mã, Tên, Tác giả, Lĩnh vực, Loại, NXB.")
            return False
        try:
            float(values[6])
            float(values[7])
            int(values[8])
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Giá mua/Giá bìa phải là số, Lần tái bản phải là số nguyên.")
            return False
        return True

    def add_command(self):
        values = self.get_all_input_values()
        if not self.validate_input(values): return
        try:
            new_id = self.db.insert_book_full(*values)
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
            messagebox.showinfo("Thành công", f"Đã cập nhật sách ID {book_db_id}.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật sách: {e}")

    def delete_command(self):
        if not self.selected_book:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sách để xóa.")
            return
        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa sách '{self.selected_book[2]}' ({self.selected_book[1]})?"):
            return
        try:
            self.db.delete_book(self.selected_book[0])
            self.clear_form()
            self.view_command()
            messagebox.showinfo("Thành công", "Đã xóa sách khỏi hệ thống.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa sách: {e}")

    def search_command(self):
        search_window = tk.Toplevel(self.master)
        SearchWindow(search_window, self)

# CLASS TÌM KIẾM SÁCH
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
        ttk.Label(main_frame, text="Nhập từ khóa (Mã, Tên sách, Tác giả):", font=('Arial', 11)).pack(pady=(5, 5), anchor='w')
        
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
            self.main_app.select_row_by_db_id(db_id)
            self.master.destroy()

# CLASS QUẢN LÝ KHO
class InventoryManagerApp:
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📦 HỆ THỐNG QUẢN LÝ KHO SÁCH")
        
        self.apply_styles()
        self.selected_inventory_record = None
        
        self.book_id_text = tk.StringVar()
        self.book_name_text = tk.StringVar()
        self.quantity_text = tk.StringVar(value="0")
        self.location_text = tk.StringVar()
        
        self.total_inventory_count_var = tk.StringVar(value="Đang tải...")
        self.status_var = tk.StringVar(value="Kết nối CSDL: Đã sẵn sàng (Mockup)")
        
        self.setup_widgets()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#FFB300", foreground="#333333", padding=[5, 5])
        style.configure("Treeview", font=('Arial', 10), rowheight=25, bordercolor="#E0E0E0", borderwidth=1, relief="flat", fieldbackground="#FFF8E1")
        style.map('Treeview', background=[('selected', '#FFD740')])
        
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("TSeparator", background="#CCCCCC")
        
        style.configure("Unified.TButton", font=('Arial', 11, 'bold'), padding=(10, 8), foreground="white")
        style.configure("Import.Unified.TButton", background="#00BCD4")
        style.map("Import.Unified.TButton", background=[('active', '#00ACC1')])
        style.configure("Export.Unified.TButton", background="#FF5722")
        style.map("Export.Unified.TButton", background=[('active', '#F4511E')])
        style.configure("Search.Unified.TButton", background="#FFC107")
        style.map("Search.Unified.TButton", background=[('active', '#FFB300')])
        style.configure("ViewInv.Unified.TButton", background="#9E9E9E")
        style.map("ViewInv.Unified.TButton", background=[('active', '#757575')])
        style.configure("Clear.Unified.TButton", background="#BDBDBD")
        style.map("Clear.Unified.TButton", background=[('active', '#A0A0A0')])
        style.configure("Logout.Unified.TButton", background="#795548")
        style.map("Logout.Unified.TButton", background=[('active', '#6D4C41')])

    def setup_widgets(self):
        main_pane = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = ttk.Frame(main_pane, padding="10")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=0)
        main_pane.add(control_frame, weight=0)
        
        detail_group = ttk.LabelFrame(control_frame, text=" CHI TIẾT TỒN KHO ", padding="15")
        detail_group.grid(row=0, column=0, sticky=N+E+S+W, padx=(0, 10))
        detail_group.grid_columnconfigure(1, weight=1)
        detail_group.grid_columnconfigure(3, weight=1)
        
        ttk.Label(detail_group, text="MÃ SÁCH:", style="Input.TLabel").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        ttk.Entry(detail_group, textvariable=self.book_id_text, state='readonly').grid(row=0, column=1, padx=(0, 10), pady=5, sticky='ew')
        
        ttk.Label(detail_group, text="SỐ LƯỢNG TỒN:", style="Input.TLabel").grid(row=0, column=2, sticky=W, padx=10, pady=5)
        ttk.Entry(detail_group, textvariable=self.quantity_text, state='readonly').grid(row=0, column=3, padx=(0, 10), pady=5, sticky='ew')
        
        ttk.Label(detail_group, text="TÊN SÁCH:", style="Input.TLabel").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        ttk.Entry(detail_group, textvariable=self.book_name_text, state='readonly').grid(row=1, column=1, padx=(0, 10), pady=5, sticky='ew')
        
        ttk.Label(detail_group, text="VỊ TRÍ KHO:", style="Input.TLabel").grid(row=1, column=2, sticky=W, padx=10, pady=5)
        ttk.Entry(detail_group, textvariable=self.location_text, state='readonly').grid(row=1, column=3, padx=(0, 10), pady=5, sticky='ew')
        
        bottom_frame = ttk.Frame(detail_group, padding=(5, 10, 5, 0))
        bottom_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        info_frame = ttk.Frame(bottom_frame)
        info_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(info_frame, text="Tổng số đầu sách đang quản lý:", style="Input.TLabel").pack(side='left', padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.total_inventory_count_var, font=('Arial', 12, 'bold'), foreground="#F44336").pack(side='left', padx=(0, 20))
        ttk.Label(info_frame, textvariable=self.status_var, font=('Arial', 9), foreground="#666666").pack(side='right')
        
        button_group = ttk.Frame(control_frame, padding="10")
        button_group.grid(row=0, column=1, sticky=N+S, padx=(10, 0))
        button_group.grid_columnconfigure(0, weight=1)
        
        buttons_info = [
            ("➕ NHẬP KHO", lambda: self.open_transaction_window("Import"), "Import.Unified.TButton"),
            ("➖ XUẤT KHO", lambda: self.open_transaction_window("Export"), "Export.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("🔍 TÌM KIẾM", self.search_inventory_command, "Search.Unified.TButton"),
            ("🔄 TẢI LẠI", self.view_inventory_command, "ViewInv.Unified.TButton"),
            ("🧹 XÓA FORM", self.clear_form, "Clear.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("⬅️ QUAY LẠI MENU", self.main_menu.close_inventory_manager, "Logout.Unified.TButton")
        ]
        
        row_index = 0
        for text, command, style_name in buttons_info:
            if text == "---":
                ttk.Separator(button_group, orient='horizontal').grid(row=row_index, column=0, sticky='ew', pady=10)
            else:
                ttk.Button(button_group, text=text, command=command, style=style_name).grid(row=row_index, column=0, padx=5, pady=4, sticky='ew')
            row_index += 1
        
        list_frame = ttk.Frame(main_pane, padding="10")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        main_pane.add(list_frame, weight=1)
        
        all_column_ids = ["ID", "MaSach", "TenSach", "SoLuongTon", "ViTriKho"]
        self.inventory_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")
        
        self.inventory_list.column("ID", width=60, anchor='center')
        self.inventory_list.column("MaSach", width=100, anchor='center')
        self.inventory_list.column("TenSach", width=400, anchor='w')
        self.inventory_list.column("SoLuongTon", width=100, anchor='center')
        self.inventory_list.column("ViTriKho", width=150, anchor='w')
        
        self.inventory_list.heading("ID", text="ID CSDL")
        self.inventory_list.heading("MaSach", text="Mã Sách")
        self.inventory_list.heading("TenSach", text="Tên Sách")
        self.inventory_list.heading("SoLuongTon", text="SL Tồn")
        self.inventory_list.heading("ViTriKho", text="Vị Trí Kho")
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.inventory_list.yview)
        self.inventory_list.configure(yscrollcommand=vsb.set)
        self.inventory_list.grid(row=0, column=0, sticky=N+E+S+W)
        vsb.grid(row=0, column=1, sticky='ns')
        
        self.inventory_list.bind('<ButtonRelease-1>', self.get_selected_row)

    def fill_form_with_data(self, inventory_record):
        self.selected_inventory_record = inventory_record
        self.book_id_text.set(inventory_record[1] if inventory_record[1] is not None else "")
        self.book_name_text.set(inventory_record[2] if inventory_record[2] is not None else "")
        self.quantity_text.set(inventory_record[3] if inventory_record[3] is not None else "0")
        self.location_text.set(inventory_record[4] if inventory_record[4] is not None else "")

    def clear_form(self):
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.quantity_text.set("0")
        self.location_text.set("")
        self.selected_inventory_record = None
        if self.inventory_list.selection():
            self.inventory_list.selection_remove(self.inventory_list.selection())

    def get_selected_row(self, event):
        selected_item = self.inventory_list.focus()
        if not selected_item:
            self.inventory_list.selection_remove(self.inventory_list.selection())
            self.clear_form()
            return
        
        self.inventory_list.selection_remove(self.inventory_list.selection())
        self.inventory_list.selection_set(selected_item)
        values = self.inventory_list.item(selected_item, 'values')
        self.fill_form_with_data(values)

    def view_inventory_command(self):
        try:
            self.clear_form()
            for item in self.inventory_list.get_children():
                self.inventory_list.delete(item)
            
            data = self.db.view_inventory()
            for row in data:
                self.inventory_list.insert('', tk.END, values=row)
            
            self.total_inventory_count_var.set(f"{len(data)} đầu sách")
            self.status_var.set("Tải dữ liệu tồn kho hoàn tất.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu tồn kho: {e}")
            self.total_inventory_count_var.set("LỖI KẾT NỐI!")
            self.status_var.set("Kết nối CSDL: Lỗi")

    def search_inventory_command(self):
        search_window = tk.Toplevel(self.master)
        InventorySearchWindow(search_window, self)

    def select_row_by_db_id(self, db_id_to_select):
        db_id_to_select = str(db_id_to_select)
        found_item = None
        if self.inventory_list.selection():
            self.inventory_list.selection_remove(self.inventory_list.selection())
        
        for item in self.inventory_list.get_children():
            if str(self.inventory_list.item(item, 'values')[0]) == db_id_to_select:
                found_item = item
                break
        
        if found_item:
            self.inventory_list.selection_set(found_item)
            self.inventory_list.focus(found_item)
            self.inventory_list.see(found_item)
            self.get_selected_row(None)

    def open_transaction_window(self, transaction_type):
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo", f"Vui lòng chọn một sách để {transaction_type.lower()} kho.")
            return
        
        book_db_id = self.selected_inventory_record[0]
        book_info = self.db.get_book_by_id(book_db_id)
        if not book_info:
            messagebox.showerror("Lỗi Dữ Liệu", "Không tìm thấy thông tin sách đầy đủ.")
            return
        
        transaction_window = tk.Toplevel(self.master)
        InventoryTransactionWindow(transaction_window, self, transaction_type, self.selected_inventory_record, book_info)

# CLASS TÌM KIẾM KHO
class InventorySearchWindow:
    def __init__(self, master, main_app_instance):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db
        master.title("🔍 Tìm Kiếm Sách Trong Kho")
        master.transient(main_app_instance.master)
        master.grab_set()
        center_window(master, 650, 480)
        master.resizable(False, False)
        
        self.search_text = tk.StringVar()
        self.setup_widgets()

    def setup_widgets(self):
        style = ttk.Style()
        style.configure("SearchHeader.TLabel", font=('Arial', 14, 'bold'), foreground="#FBC02D")
        style.configure("Search.TButton", font=('Arial', 11, 'bold'), padding=8)
        
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        ttk.Label(main_frame, text="Tìm Kiếm Nhanh Dữ Liệu Tồn Kho", style="SearchHeader.TLabel").pack(pady=(0, 15))
        ttk.Label(main_frame, text="Nhập từ khóa (Mã, Tên sách):", font=('Arial', 11)).pack(pady=(5, 5), anchor='w')
        
        search_entry = ttk.Entry(main_frame, textvariable=self.search_text, font=('Arial', 12))
        search_entry.pack(pady=(0, 15), fill='x', ipady=3)
        
        self.search_text.trace_add("write", self.update_suggestions)
        self.master.bind('<Return>', lambda event: self.select_first_suggestion())
        
        self.results_tree = ttk.Treeview(main_frame, columns=("BookID", "Title", "Quantity", "Location"), show='headings', height=10)
        self.results_tree.column("BookID", width=100, anchor='center')
        self.results_tree.column("Title", width=250, anchor='w')
        self.results_tree.column("Quantity", width=80, anchor='center')
        self.results_tree.column("Location", width=150, anchor='w')
        
        self.results_tree.heading("BookID", text="Mã Sách")
        self.results_tree.heading("Title", text="Tên Sách")
        self.results_tree.heading("Quantity", text="SL Tồn")
        self.results_tree.heading("Location", text="Vị Trí Kho")
        
        self.results_tree.bind('<<TreeviewSelect>>', self.select_suggestion)
        self.results_tree.pack(pady=10, fill='both', expand=True)
        
        ttk.Button(main_frame, text="ĐÓNG CỬA SỔ", command=self.master.destroy, style="Search.TButton").pack(pady=(15, 5), fill='x')

    def update_suggestions(self, *args):
        query = self.search_text.get().strip()
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        if not query:
            return
        
        results = self.db.search_inventory_for_suggestion(query)
        for row in results[:10]:
            db_id = row[0]
            book_id = row[1]
            title = row[2]
            quantity = row[3]
            location = row[4]
            self.results_tree.insert('', tk.END, values=(book_id, title, quantity, location), tags=(db_id,))

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
        
        inventory_record = self.db.get_inventory_record_by_id(db_id)
        if inventory_record:
            self.main_app.fill_form_with_data(inventory_record)
            self.main_app.select_row_by_db_id(db_id)
            self.master.destroy()

# CLASS NHẬP/XUẤT KHO
class InventoryTransactionWindow:
    def __init__(self, master, main_app_instance, transaction_type, inventory_record, book_info):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db
        self.transaction_type = transaction_type
        self.inventory_record = inventory_record
        self.book_info = book_info
        
        title = f"THỰC HIỆN {'NHẬP' if transaction_type == 'Import' else 'XUẤT'} KHO"
        self.master.title(title)
        self.master.transient(main_app_instance.master)
        self.master.grab_set()
        center_window(master, 550, 400)
        self.master.resizable(False, False)
        
        self.quantity_var = tk.StringVar(value="1")
        self.location_var = tk.StringVar(value=inventory_record[4] if inventory_record[4] else "Chưa xác định")
        
        self.setup_widgets()

    def setup_widgets(self):
        style = ttk.Style()
        style.configure("TransactionHeader.TLabel", font=('Arial', 16, 'bold'), foreground="#00BCD4" if self.transaction_type == 'Import' else "#FF5722")
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("Process.TButton", font=('Arial', 12, 'bold'), padding=10, background="#4CAF50" if self.transaction_type == 'Import' else "#FF9800", foreground="white")
        style.map("Process.TButton", background=[('active', '#43A047' if self.transaction_type == 'Import' else '#FB8C00')])
        
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(1, weight=1)
        
        header_text = f"THỰC HIỆN {'NHẬP' if self.transaction_type == 'Import' else 'XUẤT'} KHO"
        ttk.Label(main_frame, text=header_text, style="TransactionHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="Mã Sách:", style="Input.TLabel").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[1], font=('Arial', 11)).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(main_frame, text="Tên Sách:", style="Input.TLabel").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[2], font=('Arial', 11)).grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(main_frame, text="Tồn Kho Hiện Tại:", style="Input.TLabel").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[3], font=('Arial', 12, 'bold'), foreground="#2196F3").grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        action_label = f"SỐ LƯỢNG {'NHẬP' if self.transaction_type == 'Import' else 'XUẤT'}:"
        ttk.Label(main_frame, text=action_label, style="Input.TLabel").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        ttk.Entry(main_frame, textvariable=self.quantity_var, font=('Arial', 12), width=20).grid(row=4, column=1, padx=10, pady=10, sticky='ew')
        
        location_entry = ttk.Entry(main_frame, textvariable=self.location_var, font=('Arial', 12), width=20)
        if self.transaction_type == 'Export':
            location_entry.config(state='readonly')
        
        ttk.Label(main_frame, text="VỊ TRÍ KHO MỚI:", style="Input.TLabel").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        location_entry.grid(row=5, column=1, padx=10, pady=5, sticky='ew')
        
        button_text = f"THỰC HIỆN {'NHẬP' if self.transaction_type == 'Import' else 'XUẤT'}"
        ttk.Button(main_frame, text=button_text, command=self.process_transaction, style="Process.TButton").grid(row=7, column=0, columnspan=2, pady=20, sticky='ew')

    def process_transaction(self):
        try:
            quantity_change = int(self.quantity_var.get())
            location = self.location_var.get().strip()
            book_db_id = self.inventory_record[0]
            
            if self.transaction_type == 'Export':
                quantity_change = -quantity_change
                location = self.inventory_record[4]
            
            if quantity_change == 0:
                messagebox.showwarning("Cảnh báo", "Số lượng phải lớn hơn 0.")
                return
            
            if self.transaction_type == 'Import' and not location:
                messagebox.showwarning("Cảnh báo", "Vị trí kho không được để trống khi nhập.")
                return
            
            success, result_info = self.db.update_inventory_quantity(book_db_id, quantity_change, location)
            
            if success:
                action = "Nhập" if self.transaction_type == 'Import' else "Xuất"
                messagebox.showinfo("Thành công", f"Đã {action.lower()} {abs(quantity_change)} quyển sách.\nSố lượng tồn mới: {result_info}")
                self.main_app.view_inventory_command()
                self.master.destroy()
            else:
                messagebox.showerror("Lỗi Giao Dịch", result_info)
        except ValueError:
            messagebox.showerror("Lỗi Nhập Liệu", "Số lượng phải là một số nguyên hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi Hệ Thống", f"Đã xảy ra lỗi: {e}")

# CHẠY CHƯƠNG TRÌNH
if __name__ == '__main__':
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow)
    root.mainloop()