# database/book_database.py - Quản lý dữ liệu sách và kho NÂNG CẤP
import time
from datetime import datetime

class DatabaseManager:
    """Quản lý dữ liệu sách và kho với tính năng nâng cao."""
    
    def __init__(self, conn):
        self.conn = conn
        
        # Dữ liệu mẫu Sách (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        self.mock_data = [
            (1, 'MS001', 'Nhà Giả Kim', 'Paulo Coelho', 'Tâm Lý', 'Sách Nước Ngoài', 'NXB Văn Học', 80000, 100000, 5, '1988'),
            (2, 'MS002', 'Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Trẻ', 95500, 120000, 10, '1936'),
            (3, 'MS003', 'Toán Cao Cấp A1', 'Nhiều Tác Giả', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 120000, 150000, 1, '2023'),
            (4, 'MS004', 'Lập Trình Python Cơ Bản', 'Nguyễn Văn A', 'CNTT', 'Sách Trong Nước', 'NXB Khoa Học', 250000, 300000, 2, '2022'),
            (5, 'MS005', 'Nghệ Thuật Bán Hàng', 'Jeffrey Gitomer', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Lao Động', 90000, 130000, 3, '2019'),
            (6, 'MS006', 'Vật Lý Đại Cương', 'Trần Văn B', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 110000, 140000, 1, '2023'),
            (7, 'MS007', 'Marketing Căn Bản', 'Philip Kotler', 'Kinh Doanh', 'Sách Nước Ngoài', 'NXB Thống Kê', 180000, 220000, 14, '2015'),
            (8, 'MS008', 'Tiếng Anh Giao Tiếp', 'Oxford', 'Ngoại Ngữ', 'Sách Nước Ngoài', 'NXB Tổng Hợp', 150000, 180000, 3, '2021'),
        ]
        
        # Dữ liệu mẫu Tồn Kho: {IdSachDB: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)}
        self.mock_inventory = {
            1: (1, 'MS001', 'Nhà Giả Kim', 45, 'Kệ A1'),
            2: (2, 'MS002', 'Đắc Nhân Tâm', 150, 'Kệ A1'),
            3: (3, 'MS003', 'Toán Cao Cấp A1', 200, 'Kệ B2'),
            4: (4, 'MS004', 'Lập Trình Python Cơ Bản', 80, 'Kệ C3'),
            5: (5, 'MS005', 'Nghệ Thuật Bán Hàng', 100, 'Kệ D4'),
            6: (6, 'MS006', 'Vật Lý Đại Cương', 120, 'Kệ B2'),
            7: (7, 'MS007', 'Marketing Căn Bản', 30, 'Kệ C3'),
            8: (8, 'MS008', 'Tiếng Anh Giao Tiếp', 65, 'Kệ A1'),
        }
        
        # Lịch sử giao dịch: [(datetime, book_id, loai_gd, so_luong, gia_tri, nguoi_thuc_hien, ghi_chu)]
        self.transaction_history = [
            (datetime.now(), 1, 'Nhập kho', 50, 4000000, 'Admin', 'Nhập đợt đầu'),
            (datetime.now(), 1, 'Xuất kho', -5, -400000, 'Nhân viên 1', 'Bán lẻ'),
            (datetime.now(), 2, 'Nhập kho', 150, 14325000, 'Admin', 'Nhập đợt đầu'),
        ]
        
        self.last_book_id = len(self.mock_data)
    
    # ===== BOOK INFO OPERATIONS =====
    
    def view_all(self):
        """Xem tất cả sách"""
        time.sleep(0.05)
        return self.mock_data
    
    def search_for_suggestion(self, query):
        """Tìm kiếm sách"""
        q = query.lower()
        results = [
            row for row in self.mock_data
            if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()
        ]
        return results
    
    def get_book_by_id(self, db_id):
        """Lấy thông tin sách theo ID"""
        try:
            db_id = int(db_id)
            for row in self.mock_data:
                if row[0] == db_id:
                    return row
            return None
        except:
            return None
    
    def get_inventory_stats(self):
        """Thống kê sách"""
        total_books = len(self.mock_data)
        total_quantity = sum(inv[3] for inv in self.mock_inventory.values())
        low_stock_count = sum(1 for inv in self.mock_inventory.values() if inv[3] < 50)
        
        # Tính giá trị kho (số lượng * giá mua)
        total_value = 0
        for book_id, inv in self.mock_inventory.items():
            book = self.get_book_by_id(book_id)
            if book:
                total_value += inv[3] * book[7]  # SoLuongTon * GiaMua
        
        return {
            "TotalCount": total_books,
            "TotalQuantity": total_quantity,
            "LowStockCount": low_stock_count,
            "TotalValue": total_value
        }
    
    def insert_book_full(self, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban, nam_xb):
        """Thêm sách mới"""
        self.last_book_id += 1
        new_book_db_id = self.last_book_id
        
        new_book_row = (
            new_book_db_id, ma_sach, ten_sach, tac_gia, linh_vuc, 
            loai_sach, nxb, float(gia_mua), float(gia_bia), 
            int(lan_tai_ban), nam_xb
        )
        
        self.mock_data.append(new_book_row)
        
        # Tự động thêm vào kho với số lượng = 0
        self.mock_inventory[new_book_db_id] = (new_book_db_id, ma_sach, ten_sach, 0, 'Chưa xác định')
        
        print(f"✅ Thêm sách mới ID {new_book_db_id}: {ma_sach} - {ten_sach}")
        return new_book_db_id
    
    def update_book_full(self, db_id, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban, nam_xb):
        """Cập nhật thông tin sách"""
        print(f"🔄 Cập nhật sách ID {db_id}")
        
        # Cập nhật trong mock_data
        for i, row in enumerate(self.mock_data):
            if row[0] == db_id:
                self.mock_data[i] = (
                    db_id, ma_sach, ten_sach, tac_gia, linh_vuc,
                    loai_sach, nxb, float(gia_mua), float(gia_bia),
                    int(lan_tai_ban), nam_xb
                )
                break
        
        # Đồng bộ Mã Sách và Tên Sách trong mock_inventory
        if db_id in self.mock_inventory:
            current_inv = list(self.mock_inventory[db_id])
            current_inv[1] = ma_sach  # MaSach
            current_inv[2] = ten_sach  # TenSach
            self.mock_inventory[db_id] = tuple(current_inv)
            print(f"✅ Đã đồng bộ tồn kho cho sách ID {db_id}")
    
    def delete_book(self, db_id):
        """Xóa sách"""
        print(f"🗑️ Xóa sách ID {db_id}")
        
        # Xóa khỏi mock_data
        self.mock_data = [row for row in self.mock_data if row[0] != db_id]
        
        # Xóa khỏi mock_inventory
        if db_id in self.mock_inventory:
            del self.mock_inventory[db_id]
            print(f"✅ Đã xóa khỏi tồn kho")
    
    # ===== INVENTORY OPERATIONS =====
    
    def view_inventory(self):
        """Xem tồn kho"""
        time.sleep(0.05)
        return list(self.mock_inventory.values())
    
    def search_inventory_for_suggestion(self, query):
        """Tìm kiếm sách trong kho"""
        q = query.lower()
        results = []
        for row in self.mock_inventory.values():
            if q in str(row[1]).lower() or q in str(row[2]).lower():
                results.append(row)
        return results
    
    def filter_inventory_by_location(self, location):
        """Lọc tồn kho theo vị trí"""
        if location == "Tất cả":
            return list(self.mock_inventory.values())
        
        results = [inv for inv in self.mock_inventory.values() if inv[4] == location]
        return results
    
    def sort_inventory(self, sort_by="Mã sách"):
        """Sắp xếp tồn kho"""
        data = list(self.mock_inventory.values())
        
        if sort_by == "Mã sách":
            data.sort(key=lambda x: x[1])
        elif sort_by == "Tên sách":
            data.sort(key=lambda x: x[2])
        elif sort_by == "SL Tăng dần":
            data.sort(key=lambda x: x[3])
        elif sort_by == "SL Giảm dần":
            data.sort(key=lambda x: x[3], reverse=True)
        
        return data
    
    def update_inventory_quantity(self, book_db_id, quantity_change, location, nguoi_thuc_hien="System"):
        """Cập nhật số lượng tồn kho"""
        try:
            book_db_id = int(book_db_id)
            quantity_change = int(quantity_change)
        except ValueError:
            return False, "ID sách hoặc số lượng không hợp lệ."
        
        if book_db_id not in self.mock_inventory:
            return False, f"Không tìm thấy sách với ID: {book_db_id} trong kho."
        
        current_inventory = list(self.mock_inventory[book_db_id])
        current_quantity = current_inventory[3]
        new_quantity = current_quantity + quantity_change
        
        if new_quantity < 0:
            return False, f"Số lượng tồn kho không đủ ({current_quantity} < {-quantity_change})."
        
        # Cập nhật tồn kho
        current_inventory[3] = new_quantity
        if location:
            current_inventory[4] = location
        self.mock_inventory[book_db_id] = tuple(current_inventory)
        
        # Ghi lại lịch sử giao dịch
        loai_gd = "Nhập kho" if quantity_change > 0 else "Xuất kho"
        book = self.get_book_by_id(book_db_id)
        gia_tri = abs(quantity_change) * book[7] if book else 0  # GiaMua
        
        self.transaction_history.append((
            datetime.now(),
            book_db_id,
            loai_gd,
            abs(quantity_change),
            gia_tri,
            nguoi_thuc_hien,
            f"Thay đổi từ {current_quantity} → {new_quantity}"
        ))
        
        print(f"{'📥' if quantity_change > 0 else '📤'} {loai_gd} ID {book_db_id}: {abs(quantity_change)} quyển, Tồn mới: {new_quantity}")
        return True, new_quantity
    
    def get_inventory_record_by_id(self, db_id):
        """Lấy bản ghi tồn kho theo ID"""
        try:
            db_id = int(db_id)
            return self.mock_inventory.get(db_id)
        except:
            return None
    
    def get_transaction_history(self, limit=20):
        """Lấy lịch sử giao dịch"""
        return self.transaction_history[-limit:][::-1]  # Lấy 20 giao dịch gần nhất, đảo ngược
    
    def get_low_stock_books(self, threshold=50):
        """Lấy danh sách sách sắp hết (tồn kho < threshold)"""
        low_stock = []
        for book_id, inv in self.mock_inventory.items():
            if inv[3] < threshold:
                book = self.get_book_by_id(book_id)
                if book:
                    low_stock.append({
                        'id': book_id,
                        'ma_sach': inv[1],
                        'ten_sach': inv[2],
                        'so_luong': inv[3],
                        'vi_tri': inv[4]
                    })
        return low_stock


def getDbConnection():
    """Mock function for DB connection."""
    class MockConnection:
        def close(self): 
            pass
    return MockConnection()