# gui/search_windows.py - Cửa sổ tìm kiếm
import tkinter as tk
from tkinter import ttk
from utils.helpers import center_window

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
            self.main_app.select_row_by_db_id(db_id) # Sửa thêm: Đảm bảo chọn dòng trong treeview chính
            self.master.destroy()
# ----------------------------------------------------
#               CLASS CỬA SỔ TÌM KIẾM KHO (Không thay đổi)
# ----------------------------------------------------


class InventorySearchWindow:
    def __init__(self, master, main_app_instance):
        self.master = master
        self.main_app = main_app_instance # Sẽ là InventoryManagerApp
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
        # Dùng style riêng cho tìm kiếm kho
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
        # CỘT Tồn Kho: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
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
        # Sử dụng hàm tìm kiếm mới cho kho
        results = self.db.search_inventory_for_suggestion(query)
        # CỘT Tồn Kho: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
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
            # Lấy db_id (thẻ tag)
            db_id = self.results_tree.item(item_id, 'tags')[0]
        except IndexError:
            return
        # Lấy bản ghi tồn kho đầy đủ
        inventory_record = self.db.get_inventory_record_by_id(db_id)
        if inventory_record:
            # Gọi hàm để điền dữ liệu vào form của InventoryManagerApp
            self.main_app.fill_form_with_data(inventory_record)
            # Sau khi chọn, tự động chọn dòng đó trong Treeview chính của InventoryManagerApp
            self.main_app.select_row_by_db_id(db_id)
            self.master.destroy()
# ----------------------------------------------------
#               CLASS ỨNG DỤNG QUẢN LÝ SÁCH
# ----------------------------------------------------