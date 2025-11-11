# gui/main_menu.py - Menu chính của ứng dụng
import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import center_window

class MainMenuWindow:
    def __init__(self, master, login_window_instance, db_conn, user_info):
        self.master = master
        self.login_window = login_window_instance
        self.db_conn = db_conn
        self.user_info = user_info  # Thông tin user đã đăng nhập
        
        master.title("💡 HỆ THỐNG TRUNG TÂM QUẢN LÝ")
        self.WIDTH = 550
        self.HEIGHT = 480
        center_window(master, self.WIDTH, self.HEIGHT)
        master.resizable(False, False)
        
        self.book_manager_instance = None
        self.inventory_manager_instance = None
        
        self.setup_styles()
        self.setup_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MenuHeader.TLabel", font=('Arial', 28, 'bold'), foreground="#1E88E5", padding=20)
        style.configure("UserInfo.TLabel", font=('Arial', 11), foreground="#666666")
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
        
        # Header
        ttk.Label(main_frame, text="TRUNG TÂM QUẢN LÝ", style="MenuHeader.TLabel").grid(row=0, column=0, pady=(10, 10))
        
        # Thông tin user
        user_text = f"👤 {self.user_info['full_name']}"
        if self.user_info['role'] == 'admin':
            user_text += " (Quản trị viên)"
        ttk.Label(main_frame, text=user_text, style="UserInfo.TLabel").grid(row=1, column=0, pady=(0, 30))
        
        # Buttons
        buttons_info = [
            ("📈 1. Quản lý kinh doanh", "Business.Menu.TButton", self.open_business_manager),
            ("📚 2. Quản lý thông tin sách", "BookInfo.Menu.TButton", self.open_book_manager),
            ("📦 3. Quản lý kho sách", "Stock.Menu.TButton", self.open_inventory_manager),
            ("🚪 Đăng xuất", "Exit.Menu.TButton", self.logout_to_login)
        ]
        
        for i, (text, style_name, command) in enumerate(buttons_info):
            ttk.Button(main_frame, text=text, command=command, style=style_name).grid(row=i + 2, column=0, pady=12, sticky='ew')
    
    def open_business_manager(self):
        """Mở module quản lý kinh doanh"""
        messagebox.showinfo("Thông báo", "Chức năng Quản lý kinh doanh đang được phát triển.\nSẽ có trong phiên bản tiếp theo!")
    
    def open_book_manager(self):
        """Mở cửa sổ quản lý sách"""
        from gui.book_manager import BookManagerApp
        
        self.master.withdraw()
        
        # Ẩn cửa sổ kho nếu đang mở
        if self.inventory_manager_instance:
            if self.inventory_manager_instance.master.winfo_exists():
                self.inventory_manager_instance.master.withdraw()
        
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
        """Mở cửa sổ quản lý kho"""
        from gui.inventory_manager import InventoryManagerApp
        
        self.master.withdraw()
        
        # Ẩn cửa sổ sách nếu đang mở
        if self.book_manager_instance:
            if self.book_manager_instance.master.winfo_exists():
                self.book_manager_instance.master.withdraw()
        
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
        """Đăng xuất và quay lại màn hình đăng nhập"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            if self.book_manager_instance and self.book_manager_instance.master.winfo_exists():
                self.book_manager_instance.master.destroy()
            if self.inventory_manager_instance and self.inventory_manager_instance.master.winfo_exists():
                self.inventory_manager_instance.master.destroy()
            self.master.destroy()
            self.login_window.master.deiconify()
            self.login_window.master.focus_set()