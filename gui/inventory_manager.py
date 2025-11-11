# gui/inventory_manager.py - QUẢN LÝ KHO SÁCH CHUYÊN NGHIỆP
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import N, E, S, W
from database.book_database import DatabaseManager
from utils.helpers import center_window, format_currency

class InventoryManagerApp:
    """Ứng dụng quản lý kho sách chuyên nghiệp với giao diện đẹp"""
    
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📦 HỆ THỐNG QUẢN LÝ KHO SÁCH - PRO VERSION")
        
        # Biến điều khiển
        self.selected_inventory_record = None
        self.book_id_text = tk.StringVar()
        self.book_name_text = tk.StringVar()
        self.quantity_text = tk.StringVar(value="0")
        self.location_text = tk.StringVar()
        
        # Biến thống kê
        self.total_books_var = tk.StringVar(value="0")
        self.total_quantity_var = tk.StringVar(value="0")
        self.low_stock_var = tk.StringVar(value="0")
        self.total_value_var = tk.StringVar(value="0 đ")
        self.status_var = tk.StringVar(value="✅ Sẵn sàng")
        
        # Biến lọc
        self.filter_location_var = tk.StringVar(value="Tất cả")
        self.sort_by_var = tk.StringVar(value="Mã sách")
        
        self.apply_professional_styles()
        self.setup_professional_widgets()
    
    def apply_professional_styles(self):
        """Áp dụng theme chuyên nghiệp cao cấp"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # === COLORS - Bảng màu chuyên nghiệp ===
        self.colors = {
            'primary': '#1976D2',      # Blue - Màu chủ đạo
            'success': '#4CAF50',      # Green - Thành công
            'warning': '#FF9800',      # Orange - Cảnh báo
            'danger': '#F44336',       # Red - Nguy hiểm
            'info': '#00BCD4',         # Cyan - Thông tin
            'light': '#F5F5F5',        # Light Gray - Nền sáng
            'dark': '#212121',         # Dark Gray - Text tối
            'white': '#FFFFFF',        # White
            'border': '#E0E0E0',       # Border
        }
        
        # === HEADER STYLES ===
        style.configure("HeaderTitle.TLabel",
            font=('Segoe UI', 18, 'bold'),
            foreground=self.colors['primary'],
            background=self.colors['white'])
        
        style.configure("SectionHeader.TLabel",
            font=('Segoe UI', 12, 'bold'),
            foreground=self.colors['dark'],
            background=self.colors['light'],
            padding=10)
        
        # === STAT CARD STYLES ===
        style.configure("StatLabel.TLabel",
            font=('Segoe UI', 10),
            foreground='#666666',
            background=self.colors['white'])
        
        style.configure("StatValue.TLabel",
            font=('Segoe UI', 20, 'bold'),
            background=self.colors['white'])
        
        # === TREEVIEW - Bảng dữ liệu chuyên nghiệp ===
        style.configure("Professional.Treeview",
            font=('Segoe UI', 10),
            rowheight=35,
            borderwidth=0,
            relief="flat",
            fieldbackground=self.colors['white'])
        
        style.configure("Professional.Treeview.Heading",
            font=('Segoe UI', 11, 'bold'),
            background=self.colors['primary'],
            foreground=self.colors['white'],
            borderwidth=0,
            relief="flat")
        
        style.map('Professional.Treeview',
            background=[('selected', self.colors['info'])],
            foreground=[('selected', self.colors['white'])])
        
        # === BUTTON STYLES - Nút bấm đẹp ===
        button_config = {
            'font': ('Segoe UI', 10, 'bold'),
            'borderwidth': 0,
            'relief': 'flat',
            'padding': (15, 10)
        }
        
        # Primary Button
        style.configure("Primary.TButton",
            **button_config,
            background=self.colors['primary'],
            foreground=self.colors['white'])
        style.map("Primary.TButton",
            background=[('active', '#1565C0'), ('pressed', '#0D47A1')])
        
        # Success Button (Nhập kho)
        style.configure("Success.TButton",
            **button_config,
            background=self.colors['success'],
            foreground=self.colors['white'])
        style.map("Success.TButton",
            background=[('active', '#388E3C'), ('pressed', '#2E7D32')])
        
        # Danger Button (Xuất kho)
        style.configure("Danger.TButton",
            **button_config,
            background=self.colors['danger'],
            foreground=self.colors['white'])
        style.map("Danger.TButton",
            background=[('active', '#E53935'), ('pressed', '#C62828')])
        
        # Warning Button
        style.configure("Warning.TButton",
            **button_config,
            background=self.colors['warning'],
            foreground=self.colors['white'])
        style.map("Warning.TButton",
            background=[('active', '#F57C00'), ('pressed', '#E65100')])
        
        # Info Button
        style.configure("Info.TButton",
            **button_config,
            background=self.colors['info'],
            foreground=self.colors['white'])
        style.map("Info.TButton",
            background=[('active', '#00ACC1'), ('pressed', '#0097A7')])
        
        # Secondary Button
        style.configure("Secondary.TButton",
            **button_config,
            background='#757575',
            foreground=self.colors['white'])
        style.map("Secondary.TButton",
            background=[('active', '#616161'), ('pressed', '#424242')])
        
        # === ENTRY & COMBOBOX ===
        style.configure("Professional.TEntry",
            font=('Segoe UI', 10),
            fieldbackground=self.colors['white'],
            borderwidth=1,
            relief='solid')
        
        style.configure("Professional.TCombobox",
            font=('Segoe UI', 10),
            fieldbackground=self.colors['white'])
        
        # === LABELFRAME ===
        style.configure("Professional.TLabelframe",
            background=self.colors['white'],
            borderwidth=2,
            relief='solid')
        
        style.configure("Professional.TLabelframe.Label",
            font=('Segoe UI', 11, 'bold'),
            foreground=self.colors['primary'],
            background=self.colors['white'])
    
    def setup_professional_widgets(self):
        """Thiết lập giao diện chuyên nghiệp"""
        # Main Container với padding
        main_container = tk.Frame(self.master, bg=self.colors['light'], padx=20, pady=15)
        main_container.pack(fill='both', expand=True)
        
        # ========== HEADER SECTION ==========
        header_frame = tk.Frame(main_container, bg=self.colors['white'], padx=20, pady=15)
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Title với icon
        title_frame = tk.Frame(header_frame, bg=self.colors['white'])
        title_frame.pack(side='left')
        
        ttk.Label(title_frame, 
            text="📦 QUẢN LÝ KHO SÁCH", 
            style="HeaderTitle.TLabel").pack(side='left')
        
        # Status
        status_frame = tk.Frame(header_frame, bg=self.colors['white'])
        status_frame.pack(side='right')
        
        ttk.Label(status_frame, 
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            foreground=self.colors['success'],
            background=self.colors['white']).pack()
        
        # ========== STATISTICS DASHBOARD ==========
        stats_container = tk.Frame(main_container, bg=self.colors['light'])
        stats_container.pack(fill='x', pady=(0, 15))
        
        # 4 stat cards
        stat_cards = [
            ("📚", "Tổng đầu sách", self.total_books_var, self.colors['primary']),
            ("📦", "Tổng số lượng", self.total_quantity_var, self.colors['success']),
            ("⚠️", "Sách sắp hết", self.low_stock_var, self.colors['danger']),
            ("💰", "Giá trị kho", self.total_value_var, self.colors['warning'])
        ]
        
        for i, (icon, label, var, color) in enumerate(stat_cards):
            card = self.create_stat_card(stats_container, icon, label, var, color)
            card.grid(row=0, column=i, padx=8, sticky='ew')
            stats_container.columnconfigure(i, weight=1)
        
        # ========== FILTER & SEARCH TOOLBAR ==========
        toolbar_frame = tk.Frame(main_container, bg=self.colors['white'], padx=15, pady=12)
        toolbar_frame.pack(fill='x', pady=(0, 15))
        
        # Left side - Filters
        left_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        left_toolbar.pack(side='left', fill='x', expand=True)
        
        # Location filter
        tk.Label(left_toolbar, 
            text="📍 Vị trí:", 
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark']).pack(side='left', padx=(0, 8))
        
        location_combo = ttk.Combobox(left_toolbar,
            textvariable=self.filter_location_var,
            values=["Tất cả", "Kệ A1", "Kệ B2", "Kệ C3", "Kệ D4"],
            state='readonly',
            width=12,
            font=('Segoe UI', 10))
        location_combo.pack(side='left', padx=(0, 20))
        location_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filter())
        
        # Sort filter
        tk.Label(left_toolbar,
            text="🔽 Sắp xếp:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark']).pack(side='left', padx=(0, 8))
        
        sort_combo = ttk.Combobox(left_toolbar,
            textvariable=self.sort_by_var,
            values=["Mã sách", "Tên sách", "SL Tăng dần", "SL Giảm dần"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10))
        sort_combo.pack(side='left')
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filter())
        
        # Right side - Action buttons
        right_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        right_toolbar.pack(side='right')
        
        ttk.Button(right_toolbar,
            text="🔍 Tìm kiếm",
            command=self.search_inventory_command,
            style="Warning.TButton").pack(side='left', padx=4)
        
        ttk.Button(right_toolbar,
            text="🔄 Làm mới",
            command=self.view_inventory_command,
            style="Info.TButton").pack(side='left', padx=4)
        
        # ========== DATA TABLE ==========
        table_container = tk.Frame(main_container, bg=self.colors['white'], padx=2, pady=2)
        table_container.pack(fill='both', expand=True, pady=(0, 15))
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_container, orient='vertical')
        scroll_x = ttk.Scrollbar(table_container, orient='horizontal')
        
        # Treeview
        self.inventory_tree = ttk.Treeview(table_container,
            columns=("ID", "MaSach", "TenSach", "SoLuong", "ViTri", "TrangThai"),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse',
            style="Professional.Treeview")
        
        scroll_y.config(command=self.inventory_tree.yview)
        scroll_x.config(command=self.inventory_tree.xview)
        
        # Column configuration
        columns_config = {
            "ID": (60, 'center', 'ID'),
            "MaSach": (100, 'center', 'Mã Sách'),
            "TenSach": (300, 'w', 'Tên Sách'),
            "SoLuong": (120, 'center', 'Số Lượng Tồn'),
            "ViTri": (120, 'center', 'Vị Trí Kho'),
            "TrangThai": (100, 'center', 'Trạng Thái')
        }
        
        for col, (width, anchor, heading) in columns_config.items():
            self.inventory_tree.heading(col, text=heading)
            self.inventory_tree.column(col, width=width, anchor=anchor)
        
        # Grid layout
        self.inventory_tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)
        
        # Bind events
        self.inventory_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.inventory_tree.bind('<Double-1>', self.on_double_click)
        
        # ========== DETAIL FORM ==========
        form_frame = ttk.LabelFrame(main_container,
            text="  📝 THÔNG TIN NHẬP/XUẤT KHO  ",
            style="Professional.TLabelframe",
            padding=20)
        form_frame.pack(fill='x', pady=(0, 15))
        
        # Form grid
        form_grid = tk.Frame(form_frame, bg=self.colors['white'])
        form_grid.pack(fill='x')
        
        # Row 0
        self.create_form_field(form_grid, "Mã sách:", self.book_id_text, 0, 0, readonly=True)
        self.create_form_field(form_grid, "Số lượng tồn:", self.quantity_text, 0, 2)
        
        # Row 1
        self.create_form_field(form_grid, "Tên sách:", self.book_name_text, 1, 0, readonly=True, width=30)
        self.create_form_field(form_grid, "Vị trí kho:", self.location_text, 1, 2)
        
        # ========== ACTION BUTTONS ==========
        action_frame = tk.Frame(main_container, bg=self.colors['light'])
        action_frame.pack(fill='x')
        
        buttons = [
            ("➕ NHẬP KHO", self.stock_in_command, "Success.TButton"),
            ("➖ XUẤT KHO", self.stock_out_command, "Danger.TButton"),
            ("🔍 TÌM KIẾM", self.search_inventory_command, "Warning.TButton"),
            ("🔄 TẢI LẠI", self.view_inventory_command, "Info.TButton"),
            ("🗑️ XÓA FORM", self.clear_form, "Secondary.TButton"),
            ("↩️ QUAY LẠI", self.return_to_menu, "Secondary.TButton")
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(action_frame, text=text, command=command, style=style, width=18)
            btn.pack(side='left', padx=5)
    
    def create_stat_card(self, parent, icon, label, value_var, color):
        """Tạo card thống kê đẹp mắt"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card_inner = tk.Frame(card, bg=self.colors['white'], padx=15, pady=12)
        card_inner.pack(fill='both', expand=True)
        
        # Icon với màu
        icon_label = tk.Label(card_inner,
            text=icon,
            font=('Segoe UI', 24),
            bg=self.colors['white'],
            fg=color)
        icon_label.pack()
        
        # Value
        value_label = tk.Label(card_inner,
            textvariable=value_var,
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=color)
        value_label.pack()
        
        # Label
        label_widget = tk.Label(card_inner,
            text=label,
            font=('Segoe UI', 9),
            bg=self.colors['white'],
            fg='#666666')
        label_widget.pack()
        
        return card
    
    def create_form_field(self, parent, label_text, var, row, col, readonly=False, width=20):
        """Tạo field trong form"""
        # Label
        tk.Label(parent,
            text=label_text,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark']).grid(row=row, column=col, sticky='w', padx=(0, 10), pady=8)
        
        # Entry
        entry = ttk.Entry(parent,
            textvariable=var,
            state='readonly' if readonly else 'normal',
            width=width,
            font=('Segoe UI', 10))
        entry.grid(row=row, column=col+1, sticky='w', pady=8, padx=(0, 30))
        
        return entry
    
    def update_statistics(self):
        """Cập nhật thống kê"""
        stats = self.db.get_inventory_stats()
        
        self.total_books_var.set(str(stats.get('TotalCount', 0)))
        self.total_quantity_var.set(f"{stats.get('TotalQuantity', 0):,}")
        self.low_stock_var.set(str(stats.get('LowStockCount', 0)))
        self.total_value_var.set(format_currency(stats.get('TotalValue', 0)))
    
    def populate_tree_with_colors(self, data):
        """Hiển thị dữ liệu với màu sắc cảnh báo"""
        # Clear existing
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add data with colors
        for row in data:
            book_id, ma_sach, ten_sach, so_luong, vi_tri = row
            
            # Xác định trạng thái và màu
            if so_luong < 50:
                status = "🔴 Sắp hết"
                tag = 'danger'
            elif so_luong < 100:
                status = "🟡 Cảnh báo"
                tag = 'warning'
            else:
                status = "🟢 Tốt"
                tag = 'success'
            
            self.inventory_tree.insert('', 'end',
                values=(book_id, ma_sach, ten_sach, f"{so_luong:,}", vi_tri, status),
                tags=(tag,))
        
        # Configure tags
        self.inventory_tree.tag_configure('danger', foreground=self.colors['danger'])
        self.inventory_tree.tag_configure('warning', foreground=self.colors['warning'])
        self.inventory_tree.tag_configure('success', foreground=self.colors['success'])
    
    # ========== EVENT HANDLERS ==========
    
    def view_inventory_command(self):
        """Xem toàn bộ tồn kho"""
        self.status_var.set("⏳ Đang tải...")
        self.master.update()
        
        try:
            data = self.db.view_inventory()
            self.populate_tree_with_colors(data)
            self.update_statistics()
            self.status_var.set(f"✅ Đã tải {len(data)} sản phẩm")
        except Exception as e:
            self.status_var.set(f"❌ Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def apply_filter(self):
        """Áp dụng bộ lọc"""
        location = self.filter_location_var.get()
        sort_by = self.sort_by_var.get()
        
        # Get data
        if location == "Tất cả":
            data = self.db.view_inventory()
        else:
            data = self.db.filter_inventory_by_location(location)
        
        # Sort data
        data = self.db.sort_inventory(sort_by) if hasattr(self.db, 'sort_inventory') else data
        
        self.populate_tree_with_colors(data)
        self.status_var.set(f"✅ Hiển thị {len(data)} sản phẩm")
    
    def on_tree_select(self, event):
        """Khi chọn dòng trong bảng"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            values = item['values']
            
            self.selected_inventory_record = (values[0], values[1], values[2], 
                                             int(str(values[3]).replace(',', '')), values[4])
            
            self.book_id_text.set(values[1])
            self.book_name_text.set(values[2])
            self.quantity_text.set(str(values[3]).replace(',', ''))
            self.location_text.set(values[4])
    
    def on_double_click(self, event):
        """Double click để xem chi tiết"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            values = item['values']
            
            # Lấy thông tin sách đầy đủ
            book = self.db.get_book_by_id(values[0])
            if book:
                detail_msg = f"""
╔══════════════════════════════════════╗
║        CHI TIẾT SÁCH TRONG KHO       ║
╚══════════════════════════════════════╝

📚 Mã sách: {values[1]}
📖 Tên sách: {values[2]}
✍️ Tác giả: {book[3]}
📂 Lĩnh vực: {book[4]}
🏢 NXB: {book[6]}
💵 Giá bìa: {format_currency(book[8])}
📦 Số lượng tồn: {values[3]} quyển
📍 Vị trí: {values[4]}
📊 Trạng thái: {values[5]}
                """
                messagebox.showinfo("Thông tin chi tiết", detail_msg)
    
    def stock_in_command(self):
        """Nhập kho"""
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách từ danh sách!")
            return
        
        try:
            quantity = int(self.quantity_text.get().replace(',', ''))
            if quantity <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải > 0!")
                return
            
            location = self.location_text.get().strip()
            if not location:
                messagebox.showerror("Lỗi", "Vui lòng nhập vị trí kho!")
                return
            
            book_id = self.selected_inventory_record[0]
            success, result = self.db.update_inventory_quantity(book_id, quantity, location, "Admin")
            
            if success:
                messagebox.showinfo("Thành công", 
                    f"✅ Đã nhập {quantity:,} quyển vào kho!\n"
                    f"📦 Tồn kho mới: {result:,} quyển")
                self.view_inventory_command()
                self.clear_form()
            else:
                messagebox.showerror("Lỗi", f"❌ {result}")
        
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ!")
    
    def stock_out_command(self):
        """Xuất kho"""
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách từ danh sách!")
            return
        
        try:
            quantity = int(self.quantity_text.get().replace(',', ''))
            if quantity <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải > 0!")
                return
            
            location = self.location_text.get().strip()
            book_id = self.selected_inventory_record[0]
            
            # Confirm
            if not messagebox.askyesno("Xác nhận", 
                f"Bạn có chắc muốn xuất {quantity:,} quyển?\n"
                f"📚 {self.book_name_text.get()}"):
                return
            
            success, result = self.db.update_inventory_quantity(book_id, -quantity, location, "Admin")
            
            if success:
                messagebox.showinfo("Thành công",
                    f"✅ Đã xuất {quantity:,} quyển khỏi kho!\n"
                    f"📦 Tồn kho còn: {result:,} quyển")
                self.view_inventory_command()
                self.clear_form()
            else:
                messagebox.showerror("Lỗi", f"❌ {result}")
        
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ!")
    
    def search_inventory_command(self):
        """Tìm kiếm nhanh"""
        from tkinter import simpledialog
        
        query = simpledialog.askstring("Tìm kiếm", 
            "Nhập từ khóa tìm kiếm:\n(Mã sách hoặc Tên sách)",
            parent=self.master)
        
        if query:
            self.status_var.set("🔍 Đang tìm kiếm...")
            self.master.update()
            
            results = self.db.search_inventory_for_suggestion(query)
            
            if results:
                self.populate_tree_with_colors(results)
                self.status_var.set(f"✅ Tìm thấy {len(results)} kết quả")
            else:
                self.populate_tree_with_colors([])
                self.status_var.set("❌ Không tìm thấy kết quả")
                messagebox.showinfo("Kết quả", f"Không tìm thấy sách với từ khóa: '{query}'")
    
    def clear_form(self):
        """Xóa form"""
        self.selected_inventory_record = None
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.quantity_text.set("0")
        self.location_text.set("")
        self.status_var.set("✅ Đã xóa form")
    
    def return_to_menu(self):
        """Quay lại menu"""
        self.master.withdraw()
        self.main_menu.master.deiconify()
