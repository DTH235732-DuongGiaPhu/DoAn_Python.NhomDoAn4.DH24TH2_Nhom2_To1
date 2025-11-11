# gui/inventory_manager.py - Quản lý kho sách
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import N, E, S, W
from database.book_database import DatabaseManager
from utils.helpers import center_window
from gui.search_windows import InventorySearchWindow

class InventoryManagerApp:
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📦 HỆ THỐNG QUẢN LÝ KHO SÁCH")
        self.apply_styles()
        self.selected_inventory_record = None # (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        # Biến điều khiển cho Form chi tiết kho (để hiển thị sách được chọn)
        self.book_id_text = tk.StringVar()
        self.book_name_text = tk.StringVar()
        self.quantity_text = tk.StringVar(value="0")
        self.location_text = tk.StringVar()
        # Biến cho khu vực Thông tin Tổng quan
        self.total_inventory_count_var = tk.StringVar(value="Đang tải...")
        self.status_var = tk.StringVar(value="Kết nối CSDL: Đã sẵn sàng (Mockup)")

        self.setup_widgets()
        # Không gọi view_inventory_command() ở đây vì nó được gọi từ MainMenuWindow khi mở cửa sổ.
    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#FFB300", foreground="#333333", padding=[5, 5])
        style.configure("Treeview",
            font=('Arial', 10),
            rowheight=25,
            bordercolor="#E0E0E0",
            borderwidth=1,
            relief="flat",
            fieldbackground="#FFF8E1" # Light yellow background
        )
        style.map('Treeview', background=[('selected', '#FFD740')]) # Darker yellow when selected
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("TSeparator", background="#CCCCCC")
        # Styles cho Buttons (Đồng bộ, có thêm styles riêng cho Nhập/Xuất)
        style.configure("Unified.TButton", font=('Arial', 11, 'bold'), padding=(10, 8), foreground="white")
        style.configure("Import.Unified.TButton", background="#00BCD4") # Cyan
        style.map("Import.Unified.TButton", background=[('active', '#00ACC1')])
        style.configure("Export.Unified.TButton", background="#FF5722") # Deep Orange
        style.map("Export.Unified.TButton", background=[('active', '#F4511E')])

        # [THÊM] Style cho nút Tìm Kiếm (giống BookManagerApp)
        style.configure("Search.Unified.TButton", background="#FFC107")
        style.map("Search.Unified.TButton", background=[('active', '#FFB300')])
        style.configure("ViewInv.Unified.TButton", background="#9E9E9E")
        style.map("ViewInv.Unified.TButton", background=[('active', '#757575')])

        style.configure("Clear.Unified.TButton", background="#BDBDBD")
        style.map("Clear.Unified.TButton", background=[('active', '#A0A0A0')])
        style.configure("Logout.Unified.TButton", background="#795548")
        style.map("Logout.Unified.TButton", background=[('active', '#6D4C41')])
        # --- KẾT THÚC ĐIỀU CHỈNH ---

    def setup_widgets(self):
        # 1. PanedWindow Chính
        main_pane = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # 1A. Khu vực Điều khiển và Nhập liệu/Thông tin (Control Frame)
        control_frame = ttk.Frame(main_pane, padding="10")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=0)
        main_pane.add(control_frame, weight=0)
        # --- KHU VỰC 1: CHI TIẾT SÁCH TRONG KHO VÀ TỔNG QUAN ---
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

        # --- KHU VỰC THÔNG TIN TỔNG QUAN VÀ BUTTONS CHỨC NĂNG CHÍNH ---
        bottom_frame = ttk.Frame(detail_group, padding=(5, 10, 5, 0))
        bottom_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        bottom_frame.grid_columnconfigure(0, weight=1)
        # Khu vực Thông tin Tổng quan (Layout ngang)
        info_frame = ttk.Frame(bottom_frame)
        info_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(info_frame, text="Tổng số đầu sách đang quản lý:", style="Input.TLabel").pack(side='left', padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.total_inventory_count_var, font=('Arial', 12, 'bold'), foreground="#F44336").pack(side='left', padx=(0, 20))

        ttk.Label(info_frame, textvariable=self.status_var, font=('Arial', 9), foreground="#666666").pack(side='right')
        # --- KHU VỰC 2: BUTTONS ---
        button_group = ttk.Frame(control_frame, padding="10")
        button_group.grid(row=0, column=1, sticky=N+S, padx=(10, 0))
        button_group.grid_columnconfigure(0, weight=1)
        buttons_info = [
            ("➕ NHẬP KHO", lambda: self.open_transaction_window("Import"), "Import.Unified.TButton"),
            ("➖ XUẤT KHO", lambda: self.open_transaction_window("Export"), "Export.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("🔍 TÌM KIẾM", self.search_inventory_command, "Search.Unified.TButton"), # [THÊM] Nút Tìm Kiếm
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
        # 1B. Khu vực Bảng hiển thị Tồn Kho (Treeview)
        list_frame = ttk.Frame(main_pane, padding="10")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        main_pane.add(list_frame, weight=1)
        # CỘT CSDL trả về: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        all_column_ids = ["ID", "MaSach", "TenSach", "SoLuongTon", "ViTriKho"]
        self.inventory_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")

        # Cấu hình cột
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
        # inventory_record: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
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
        # values: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        self.fill_form_with_data(values)

    # --- START CHANGE (CHỈNH SỬA INVENTORYMANAGER) ---
    def view_inventory_command(self):
        # Tải lại danh sách tồn kho
        try:
            # THÊM MỚI: Reset form (xóa input và bỏ chọn)
            self.clear_form()

            # Xóa dữ liệu cũ
            for item in self.inventory_list.get_children():
                self.inventory_list.delete(item)

            data = self.db.view_inventory()

            # CỘT CSDL trả về: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
            for row in data:
                self.inventory_list.insert('', tk.END, values=row)

            self.total_inventory_count_var.set(f"{len(data)} đầu sách")
            self.status_var.set("Tải dữ liệu tồn kho hoàn tất.")

        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu tồn kho: {e}")
            self.total_inventory_count_var.set("LỖI KẾT NỐI!")
            self.status_var.set("Kết nối CSDL: Lỗi")
    # --- END CHANGE ---

    # [THÊM] Hàm mở cửa sổ tìm kiếm kho
    def search_inventory_command(self):
        search_window = tk.Toplevel(self.master)
        InventorySearchWindow(search_window, self)
    # [THÊM] Hàm chọn dòng trong treeview chính (dùng cho tìm kiếm)
    def select_row_by_db_id(self, db_id_to_select):
        # Hàm này được gọi từ cửa sổ tìm kiếm để chọn dòng tương ứng trong treeview chính
        db_id_to_select = str(db_id_to_select)
        found_item = None

        # Xóa chọn cũ
        if self.inventory_list.selection():
            self.inventory_list.selection_remove(self.inventory_list.selection())
        for item in self.inventory_list.get_children():
            # Giá trị đầu tiên trong values là Id sách
            if str(self.inventory_list.item(item, 'values')[0]) == db_id_to_select:
                found_item = item
                break

        if found_item:
            self.inventory_list.selection_set(found_item)
            self.inventory_list.focus(found_item)
            self.inventory_list.see(found_item)
            self.get_selected_row(None) # Kích hoạt việc điền form
    def open_transaction_window(self, transaction_type):
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo", f"Vui lòng chọn một sách để {transaction_type.lower()} kho.")
            return
        book_db_id = self.selected_inventory_record[0]
        book_info = self.db.get_book_by_id(book_db_id)
        if not book_info:
            messagebox.showerror("Lỗi Dữ Liệu", "Không tìm thấy thông tin sách đầy đủ.")
            return
        # book_info: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)

        transaction_window = tk.Toplevel(self.master)
        InventoryTransactionWindow(transaction_window, self, transaction_type, self.selected_inventory_record, book_info)
# ----------------------------------------------------
#               CLASS CỬA SỔ NHẬP/XUẤT KHO (Không thay đổi)
# ----------------------------------------------------


class InventoryTransactionWindow:
    def __init__(self, master, main_app_instance, transaction_type, inventory_record, book_info):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db
        self.transaction_type = transaction_type # 'Import' hoặc 'Export'
        self.inventory_record = inventory_record # (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        self.book_info = book_info

        title = f"THỰC HIỆN {'NHẬP' if transaction_type == 'Import' else 'XUẤT'} KHO"
        self.master.title(title)
        self.master.transient(main_app_instance.master)
        self.master.grab_set()
        center_window(master, 550, 400)
        self.master.resizable(False, False)
        self.quantity_var = tk.StringVar(value="1")
        # Nếu là NHẬP, cho phép thay đổi vị trí.
        # Nếu là XUẤT, vị trí bị khóa theo vị trí hiện tại.
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
        # Hiển thị thông tin sách
        ttk.Label(main_frame, text="Mã Sách:", style="Input.TLabel").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[1], font=('Arial', 11)).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(main_frame, text="Tên Sách:", style="Input.TLabel").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[2], font=('Arial', 11)).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(main_frame, text="Tồn Kho Hiện Tại:", style="Input.TLabel").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(main_frame, text=self.inventory_record[3], font=('Arial', 12, 'bold'), foreground="#2196F3").grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Nhập số lượng
        action_label = f"SỐ LƯỢNG {'NHẬP' if self.transaction_type == 'Import' else 'XUẤT'}:"
        ttk.Label(main_frame, text=action_label, style="Input.TLabel").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        ttk.Entry(main_frame, textvariable=self.quantity_var, font=('Arial', 12), width=20).grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        # Vị trí kho
        location_entry = ttk.Entry(main_frame, textvariable=self.location_var, font=('Arial', 12), width=20)

        if self.transaction_type == 'Export':
            location_entry.config(state='readonly') # Không được thay đổi vị trí khi xuất

        ttk.Label(main_frame, text="VỊ TRÍ KHO MỚI:", style="Input.TLabel").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        location_entry.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

        # Nút thực hiện
        button_text = f"THỰC HIỆN {'NHẬP' if self.transaction_type == 'Import' else 'XUẤT'}"
        ttk.Button(main_frame, text=button_text, command=self.process_transaction, style="Process.TButton").grid(row=7, column=0, columnspan=2, pady=20, sticky='ew')
    def process_transaction(self):
        try:
            quantity_change = int(self.quantity_var.get())
            location = self.location_var.get().strip()
            book_db_id = self.inventory_record[0]

            if self.transaction_type == 'Export':
                quantity_change = -quantity_change # Xuất kho là trừ đi
                location = self.inventory_record[4] # Giữ nguyên vị trí kho khi xuất

            if quantity_change == 0:
                messagebox.showwarning("Cảnh báo", "Số lượng phải lớn hơn 0.")
                return
            if self.transaction_type == 'Import' and not location:
                messagebox.showwarning("Cảnh báo", "Vị trí kho không được để trống khi nhập.")
                return
            # Thực hiện cập nhật DB
            success, result_info = self.db.update_inventory_quantity(book_db_id, quantity_change, location)

            if success:
                action = "Nhập" if self.transaction_type == 'Import' else "Xuất"
                messagebox.showinfo("Thành công", f"Đã {action.lower()} {abs(quantity_change)} quyển sách.\nSố lượng tồn mới: {result_info}")
                self.main_app.view_inventory_command() # Tải lại dữ liệu ở cửa sổ chính
                self.master.destroy()
            else:
                messagebox.showerror("Lỗi Giao Dịch", result_info)

        except ValueError:
            messagebox.showerror("Lỗi Nhập Liệu", "Số lượng phải là một số nguyên hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi Hệ Thống", f"Đã xảy ra lỗi: {e}")
# ----------------------------------------------------
#               PHẦN CHẠY CHƯƠNG TRÌNH
# ----------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow)
    root.mainloop()
