# gui/login_window.py - Cửa sổ đăng nhập
import tkinter as tk
from tkinter import ttk, messagebox
from database.user_manager import UserManager

class LoginWindow:
    def __init__(self, master, main_menu_class, get_db_connection_func):
        self.master = master
        self.master.title("🔐 Đăng Nhập Hệ Thống")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.WIDTH = 520
        self.HEIGHT = 380
        self.center_window(self.WIDTH, self.HEIGHT)
        self.master.resizable(False, False)
        
        self.main_menu_class = main_menu_class
        self.get_db_connection = get_db_connection_func
        self.main_menu_instance = None
        self.user_manager = UserManager()
        self.current_user = None  # Lưu thông tin user đã đăng nhập
        
        # Biến điều khiển
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.BooleanVar(value=False)
        
        self.setup_styles()
        self.setup_widgets()
    
    def center_window(self, w, h):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.master.geometry(f'{w}x{h}+{x}+{y}')
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=('Arial', 11))
        style.configure("TEntry", font=('Arial', 12))
        style.configure("LoginHeader.TLabel", font=('Arial', 22, 'bold'), foreground="#1E88E5")
        style.configure("Login.TButton", font=('Arial', 13, 'bold'), padding=12, background="#4CAF50", foreground="white")
        style.map("Login.TButton", background=[('active', '#43A047')])
        style.configure("Register.TButton", font=('Arial', 11), padding=8, background="#2196F3", foreground="white")
        style.map("Register.TButton", background=[('active', '#1E88E5')])
    
    def setup_widgets(self):
        main_frame = ttk.Frame(self.master, padding="40 30 40 30")
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        ttk.Label(header_frame, text="🔐 ĐĂNG NHẬP HỆ THỐNG", style="LoginHeader.TLabel").pack()
        ttk.Label(header_frame, text="Hệ thống quản lý sách", font=('Arial', 10), foreground="#666").pack(pady=(5, 0))
        
        # Username
        ttk.Label(main_frame, text="👤 Tên đăng nhập:", style="TLabel").grid(row=1, column=0, sticky="w", padx=10, pady=12)
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=1, column=1, padx=10, pady=12, sticky='ew')
        username_entry.focus()
        
        # Password
        ttk.Label(main_frame, text="🔒 Mật khẩu:", style="TLabel").grid(row=2, column=0, sticky="w", padx=10, pady=12)
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show='*', width=30)
        password_entry.grid(row=2, column=1, padx=10, pady=12, sticky='ew')
        
        # Remember me checkbox
        remember_frame = ttk.Frame(main_frame)
        remember_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Checkbutton(remember_frame, text="Ghi nhớ đăng nhập", variable=self.remember_var).pack()
        
        # Login button
        ttk.Button(main_frame, text="🚀 ĐĂNG NHẬP", command=self.login, style="Login.TButton").grid(
            row=4, column=0, columnspan=2, pady=(20, 10), sticky='ew', padx=10
        )
        
        # Register button
        register_frame = ttk.Frame(main_frame)
        register_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Label(register_frame, text="Chưa có tài khoản?", font=('Arial', 10)).pack(side='left', padx=(0, 10))
        ttk.Button(register_frame, text="📝 Đăng ký ngay", command=self.open_register, style="Register.TButton").pack(side='left')
        
        # Bind Enter key
        self.master.bind('<Return>', lambda event: self.login())
    
    def open_register(self):
        """Mở cửa sổ đăng ký"""
        register_window = tk.Toplevel(self.master)
        from gui.register_window import RegisterWindow
        RegisterWindow(register_window, self)
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        # Kiểm tra input
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return
        
        # Xác thực với database
        success, result = self.user_manager.login(username, password)
        
        if success:
            self.current_user = result  # Lưu thông tin user
            
            # Lấy kết nối database
            db_conn = self.get_db_connection()
            if db_conn is None:
                messagebox.showerror("Lỗi CSDL", "Không thể kết nối đến cơ sở dữ liệu.")
                return
            
            # Ẩn cửa sổ đăng nhập
            self.master.withdraw()
            
            # Mở menu chính
            if not self.main_menu_instance or not self.main_menu_instance.master.winfo_exists():
                self.main_window = tk.Toplevel(self.master)
                self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing_menu)
                self.main_menu_instance = self.main_menu_class(
                    self.main_window, 
                    self, 
                    db_conn,
                    self.current_user  # Truyền thông tin user vào menu
                )
                self.main_window.deiconify()
            
            # Hiển thị thông báo chào mừng
            welcome_msg = f"Chào mừng {result['full_name']}!"
            if result['role'] == 'admin':
                welcome_msg += "\n(Quản trị viên)"
            messagebox.showinfo("Đăng nhập thành công", welcome_msg)
        else:
            messagebox.showerror("Lỗi đăng nhập", result)
            self.password_var.set("")  # Xóa mật khẩu đã nhập
    
    def on_closing_menu(self):
        """Xử lý khi đóng menu chính"""
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            if self.main_menu_instance and self.main_menu_instance.db_conn:
                try:
                    self.main_menu_instance.db_conn.close()
                except:
                    pass
            self.master.quit()
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ đăng nhập"""
        if messagebox.askyesno("Xác nhận Thoát", "Bạn có muốn thoát chương trình?"):
            self.master.quit()
