# database/book_database.py - Quản lý dữ liệu sách và kho
import time

class DatabaseManager:
    """Quản lý dữ liệu sách và kho (Mockup dùng list)."""
    
    def __init__(self, conn):
        self.conn = conn
        # Dữ liệu mẫu Sách (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        self.mock_data = [
            (1, 'MS001', 'Nhà Giả Kim', 'Paulo Coelho', 'Tâm Lý', 'Sách Nước Ngoài', 'NXB Văn Học', 80.0, 100.0, 5, '1988'),
            (2, 'MS002', 'Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Trẻ', 95.5, 120.0, 10, '1936'),
            (3, 'MS003', 'Toán Cao Cấp A1', 'Nhiều Tác Giả', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 120.0, 150.0, 1, '2023'),
            (4, 'MS004', 'Lập Trình Python Cơ Bản', 'Nguyễn Văn A', 'CNTT', 'Sách Trong Nước', 'NXB Khoa Học', 250.0, 300.0, 2, '2022'),
            (5, 'MS005', 'Nghệ Thuật Bán Hàng', 'Jeffrey Gitomer', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Lao Động', 90.0, 130.0, 3, '2019'),
            (6, 'MS006', 'Vật Lý Đại Cương', 'Trần Văn B', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 110.0, 140.0, 1, '2023'),
        ]
        # Dữ liệu mẫu Tồn Kho: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        self.mock_inventory = {
            1: (1, 'MS001', 'Nhà Giả Kim', 50, 'Kệ A1'),
            2: (2, 'MS002', 'Đắc Nhân Tâm', 150, 'Kệ A1'),
            3: (3, 'MS003', 'Toán Cao Cấp A1', 200, 'Kệ B2'),
            4: (4, 'MS004', 'Lập Trình Python Cơ Bản', 80, 'Kệ C3'),
            5: (5, 'MS005', 'Nghệ Thuật Bán Hàng', 100, 'Kệ D4'),
        }
        self.last_book_id = len(self.mock_data)
    
    # --- BOOK INFO OPERATIONS ---
    def view_all(self):
        time.sleep(0.1)
        return self.mock_data
    
    def search_for_suggestion(self, query):
        q = query.lower()
        results = [
            row for row in self.mock_data
            if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()
        ]
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
    
    def get_inventory_stats(self):
        return {
            "TotalCount": len(self.mock_data)
        }
    
    # Mock DB operations
    def insert_book_full(self, *values):
        self.last_book_id += 1
        new_book_db_id = self.last_book_id
        # Mô phỏng thêm sách mới vào cả danh sách sách và tồn kho
        new_book_row = (new_book_db_id, values[0], values[1], values[2], values[3], values[4], values[5], float(values[6]), float(values[7]), int(values[8]), values[9])
        self.mock_data.append(new_book_row)
        self.mock_inventory[new_book_db_id] = (new_book_db_id, values[0], values[1], 0, 'Chưa xác định')
        print(f"Mock Insert: {new_book_row}")
        return new_book_db_id
    
    def update_book_full(self, db_id, *values):
        print(f"Mock Update ID {db_id}: {values}")
        # Cập nhật sách trong mock_data
        for i, row in enumerate(self.mock_data):
            if row[0] == db_id:
                self.mock_data[i] = (db_id, values[0], values[1], values[2], values[3], values[4], values[5], float(values[6]), float(values[7]), int(values[8]), values[9])
                break
        # Cập nhật Mã Sách và Tên Sách trong mock_inventory (nếu có)
        if db_id in self.mock_inventory:
            current_inv = list(self.mock_inventory[db_id])
            current_inv[1] = values[0] # MaSach
            current_inv[2] = values[1] # TenSach
            self.mock_inventory[db_id] = tuple(current_inv)
    
    def delete_book(self, db_id):
        print(f"Mock Delete ID {db_id}")
        # Xóa khỏi mock_data
        self.mock_data = [row for row in self.mock_data if row[0] != db_id]
        # Xóa khỏi mock_inventory
        if db_id in self.mock_inventory:
            del self.mock_inventory[db_id]
    
    # --- INVENTORY OPERATIONS ---
    def view_inventory(self):
        time.sleep(0.1)
        # Chuyển đổi từ dict sang list of tuples để dễ hiển thị trong Treeview
        # Trả về: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)
        return list(self.mock_inventory.values())

    def search_inventory_for_suggestion(self, query):
        """Tìm kiếm sách trong kho theo Mã, Tên sách."""
        q = query.lower()
        results = []
        # self.mock_inventory is a dict: {IdSachDB: (IdSachDB, MaSach, TenSach, SoLuongTon, ViTriKho)}
        for row in self.mock_inventory.values():
            # row[1] is MaSach, row[2] is TenSach
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
            return False, f"Số lượng tồn kho không đủ để xuất ({current_quantity} < {-quantity_change})."
        
        current_inventory[3] = new_quantity
        current_inventory[4] = location if location else current_inventory[4] # Cập nhật vị trí nếu có
        self.mock_inventory[book_db_id] = tuple(current_inventory)
        print(f"Mock Inventory Update ID {book_db_id}: Change {quantity_change}, New Qty {new_quantity}")
        return True, new_quantity
    
    def get_inventory_record_by_id(self, db_id):
        try:
            db_id = int(db_id)
            return self.mock_inventory.get(db_id)
        except:
            return None


def getDbConnection():
    """Mock function for DB connection."""
    class MockConnection:
        def close(self): 
            pass
    return MockConnection()