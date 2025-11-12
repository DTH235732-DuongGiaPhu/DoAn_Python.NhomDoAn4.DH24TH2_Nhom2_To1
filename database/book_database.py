import time
from datetime import datetime

class DatabaseManager:
    """Quản lý dữ liệu sách và kho với tính năng nâng cao."""
    
    # CLASS VARIABLES - Chia sẻ giữa tất cả instances
    mock_data = [
        [1, 'MS001', 'Nhà Giả Kim', 'Paulo Coelho', 'Tâm Lý', 'Sách Nước Ngoài', 'NXB Văn Học', 80000, 100000, 5, '1988'],
        [2, 'MS002', 'Đắc Nhân Tâm', 'Dale Carnegie', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Trẻ', 95500, 120000, 10, '1936'],
        [3, 'MS003', 'Toán Cao Cấp A1', 'Nhiều Tác Giả', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 120000, 150000, 1, '2023'],
        [4, 'MS004', 'Lập Trình Python Cơ Bản', 'Nguyễn Văn A', 'CNTT', 'Sách Trong Nước', 'NXB Khoa Học', 250000, 300000, 2, '2022'],
        [5, 'MS005', 'Nghệ Thuật Bán Hàng', 'Jeffrey Gitomer', 'Kỹ Năng Sống', 'Sách Nước Ngoài', 'NXB Lao Động', 90000, 130000, 3, '2019'],
        [6, 'MS006', 'Vật Lý Đại Cương', 'Trần Văn B', 'Giáo Trình', 'Sách Trong Nước', 'NXB Giáo Dục', 110000, 140000, 1, '2023'],
        [7, 'MS007', 'Marketing Căn Bản', 'Philip Kotler', 'Kinh Doanh', 'Sách Nước Ngoài', 'NXB Thống Kê', 180000, 220000, 14, '2015'],
        [8, 'MS008', 'Tiếng Anh Giao Tiếp', 'Oxford', 'Ngoại Ngữ', 'Sách Nước Ngoài', 'NXB Tổng Hợp', 150000, 180000, 3, '2021'],
    ]
    
    mock_inventory = {
        1: (1, 'MS001', 'Nhà Giả Kim', 45, 'Kệ A1'),
        2: (2, 'MS002', 'Đắc Nhân Tâm', 150, 'Kệ A1'),
        3: (3, 'MS003', 'Toán Cao Cấp A1', 200, 'Kệ B2'),
        4: (4, 'MS004', 'Lập Trình Python Cơ Bản', 80, 'Kệ C3'),
        5: (5, 'MS005', 'Nghệ Thuật Bán Hàng', 100, 'Kệ D4'),
        6: (6, 'MS006', 'Vật Lý Đại Cương', 120, 'Kệ B2'),
        7: (7, 'MS007', 'Marketing Căn Bản', 30, 'Kệ C3'),
        8: (8, 'MS008', 'Tiếng Anh Giao Tiếp', 65, 'Kệ A1'),
    }
    
    transaction_history = [
        (datetime.now(), 1, 'Nhập kho', 50, 4000000, 'Admin', 'Nhập đợt đầu'),
        (datetime.now(), 1, 'Xuất kho', -5, -400000, 'Nhân viên 1', 'Bán lẻ'),
        (datetime.now(), 2, 'Nhập kho', 150, 14325000, 'Admin', 'Nhập đợt đầu'),
    ]
    
    last_book_id = 8
    
    mock_orders = [
        (1, 'DH001', 'Nguyễn Văn A', '0901234567', 'nguyenvana@gmail.com', '123 Đường ABC, TP.HCM', '2025-11-10', 500000, 'Hoàn thành', 'Admin'),
        (2, 'DH002', 'Trần Thị B', '0912345678', 'tranthib@gmail.com', '456 Đường XYZ, Hà Nội', '2025-11-10', 350000, 'Đang xử lý', 'Admin'),
        (3, 'DH003', 'Lê Văn C', '0923456789', 'levanc@gmail.com', '789 Đường DEF, Đà Nẵng', '2025-11-09', 1200000, 'Hoàn thành', 'Admin'),
        (4, 'DH004', 'Phạm Thị D', '0934567890', 'phamthid@gmail.com', '321 Đường GHI, TP.HCM', '2025-11-09', 800000, 'Hoàn thành', 'Admin'),
        (5, 'DH005', 'Hoàng Văn E', '0945678901', 'hoangvane@gmail.com', '654 Đường JKL, Huế', '2025-11-08', 450000, 'Đang xử lý', 'Admin'),
    ]
    
    mock_order_details = [
        (1, 1, 1, 2, 100000, 200000),
        (2, 1, 2, 3, 100000, 300000),
        (3, 2, 3, 2, 150000, 300000),
        (4, 2, 1, 1, 50000, 50000),
        (5, 3, 4, 4, 300000, 1200000),
        (6, 4, 5, 2, 130000, 260000),
        (7, 4, 6, 4, 135000, 540000),
        (8, 5, 7, 2, 220000, 440000),
        (9, 5, 8, 1, 10000, 10000),
    ]
    
    last_order_id = 5
    last_detail_id = 9
    
    def __init__(self, conn):
        self.conn = conn
    
    # ===== BOOK INFO OPERATIONS =====
    
    def view_all(self):
        """Xem tất cả sách"""
        time.sleep(0.05)
        return DatabaseManager.mock_data
    
    def search_for_suggestion(self, query):
        """Tìm kiếm sách"""
        q = query.lower()
        results = [
            row for row in DatabaseManager.mock_data
            if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()
        ]
        return results
    
    def get_book_by_id(self, db_id):
        """Lấy thông tin sách theo ID"""
        try:
            db_id = int(db_id)
            for row in DatabaseManager.mock_data:
                if row[0] == db_id:
                    return row
            return None
        except:
            return None
    
    def get_inventory_stats(self):
        """Thống kê sách"""
        total_books = len(DatabaseManager.mock_data)
        total_quantity = sum(inv[3] for inv in DatabaseManager.mock_inventory.values())
        low_stock_count = sum(1 for inv in DatabaseManager.mock_inventory.values() if inv[3] < 50)
        
        # Tính giá trị kho (số lượng * giá mua)
        total_value = 0
        for book_id, inv in DatabaseManager.mock_inventory.items():
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
        DatabaseManager.last_book_id += 1
        new_book_db_id = DatabaseManager.last_book_id
        
        new_book_row = [
            new_book_db_id, ma_sach, ten_sach, tac_gia, linh_vuc, 
            loai_sach, nxb, float(gia_mua), float(gia_bia), 
            int(lan_tai_ban), nam_xb
        ]
        
        DatabaseManager.mock_data.append(new_book_row)
        
        # Tự động thêm vào kho với số lượng = 0
        DatabaseManager.mock_inventory[new_book_db_id] = (new_book_db_id, ma_sach, ten_sach, 0, 'Chưa xác định')
        
        print(f"✅ Thêm sách mới ID {new_book_db_id}: {ma_sach} - {ten_sach}")
        return new_book_db_id
    
    def update_book_full(self, db_id, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban, nam_xb):
        """Cập nhật thông tin sách"""
        print(f"🔄 Cập nhật sách ID {db_id}")
        
        # Cập nhật trong mock_data (class variable)
        for i, row in enumerate(DatabaseManager.mock_data):
            if row[0] == db_id:
                DatabaseManager.mock_data[i] = [
                    db_id, ma_sach, ten_sach, tac_gia, linh_vuc,
                    loai_sach, nxb, float(gia_mua), float(gia_bia),
                    int(lan_tai_ban), nam_xb
                ]
                print(f"✅ Đã cập nhật thông tin sách ID {db_id}")
                break
        
        # Đồng bộ Mã Sách và Tên Sách trong mock_inventory
        if db_id in DatabaseManager.mock_inventory:
            current_inv = list(DatabaseManager.mock_inventory[db_id])
            current_inv[1] = ma_sach
            current_inv[2] = ten_sach
            DatabaseManager.mock_inventory[db_id] = tuple(current_inv)
            print(f"✅ Đã đồng bộ tồn kho cho sách ID {db_id}")
    
    def delete_book(self, db_id):
        """Xóa sách"""
        print(f"🗑️ Xóa sách ID {db_id}")
        
        # Xóa khỏi mock_data
        DatabaseManager.mock_data = [row for row in DatabaseManager.mock_data if row[0] != db_id]
        
        # Xóa khỏi mock_inventory
        if db_id in DatabaseManager.mock_inventory:
            del DatabaseManager.mock_inventory[db_id]
            print(f"✅ Đã xóa khỏi tồn kho")
    
    # ===== INVENTORY OPERATIONS =====
    
    def view_inventory(self):
        """Xem tồn kho"""
        time.sleep(0.05)
        return list(DatabaseManager.mock_inventory.values())
    
    def search_inventory_for_suggestion(self, query):
        """Tìm kiếm sách trong kho"""
        q = query.lower()
        results = []
        for row in DatabaseManager.mock_inventory.values():
            if q in str(row[1]).lower() or q in str(row[2]).lower():
                results.append(row)
        return results
    
    def filter_inventory_by_location(self, location):
        """Lọc tồn kho theo vị trí"""
        if location == "Tất cả":
            return list(DatabaseManager.mock_inventory.values())
        
        results = [inv for inv in DatabaseManager.mock_inventory.values() if inv[4] == location]
        return results
    
    def sort_inventory(self, sort_by="Mã sách"):
        """Sắp xếp tồn kho"""
        data = list(DatabaseManager.mock_inventory.values())
        
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
        
        if book_db_id not in DatabaseManager.mock_inventory:
            return False, f"Không tìm thấy sách với ID: {book_db_id} trong kho."
        
        current_inventory = list(DatabaseManager.mock_inventory[book_db_id])
        current_quantity = current_inventory[3]
        new_quantity = current_quantity + quantity_change
        
        if new_quantity < 0:
            return False, f"Số lượng tồn kho không đủ ({current_quantity} < {-quantity_change})."
        
        # Cập nhật tồn kho
        current_inventory[3] = new_quantity
        if location:
            current_inventory[4] = location
        DatabaseManager.mock_inventory[book_db_id] = tuple(current_inventory)
        
        # Ghi lại lịch sử giao dịch
        loai_gd = "Nhập kho" if quantity_change > 0 else "Xuất kho"
        book = self.get_book_by_id(book_db_id)
        gia_tri = abs(quantity_change) * book[7] if book else 0  # GiaMua
        
        DatabaseManager.transaction_history.append((
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
            return DatabaseManager.mock_inventory.get(db_id)
        except:
            return None
    
    def get_transaction_history(self, limit=20):
        """Lấy lịch sử giao dịch"""
        return DatabaseManager.transaction_history[-limit:][::-1]  # Lấy 20 giao dịch gần nhất, đảo ngược
    
    def get_low_stock_books(self, threshold=50):
        """Lấy danh sách sách sắp hết (tồn kho < threshold)"""
        low_stock = []
        for book_id, inv in DatabaseManager.mock_inventory.items():
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
    
    # ===== ORDER MANAGEMENT OPERATIONS =====
    
    def get_all_orders(self):
        """Lấy tất cả đơn hàng"""
        time.sleep(0.05)
        return list(DatabaseManager.mock_orders)
    
    def get_order_by_id(self, order_id):
        """Lấy đơn hàng theo ID"""
        for order in DatabaseManager.mock_orders:
            if order[0] == order_id:
                return order
        return None
    
    def get_order_details(self, order_id):
        """Lấy chi tiết đơn hàng"""
        details = []
        for detail in DatabaseManager.mock_order_details:
            if detail[1] == order_id:  # detail[1] là OrderID
                # Lấy thông tin sách
                book = self.get_book_by_id(detail[2])
                if book:
                    details.append({
                        'DetailID': detail[0],
                        'BookID': detail[2],
                        'BookCode': book[1],
                        'BookName': book[2],
                        'Quantity': detail[3],
                        'UnitPrice': detail[4],
                        'Subtotal': detail[5]
                    })
        return details
    
    def create_order(self, customer_name, phone, email, address, order_items, created_by='Admin'):
        """
        Tạo đơn hàng mới
        order_items: [(book_id, quantity, unit_price), ...]
        """
        try:
            # Tạo mã đơn hàng
            DatabaseManager.last_order_id += 1
            order_code = f"DH{DatabaseManager.last_order_id:03d}"
            
            # Tính tổng tiền
            total_amount = sum(item[1] * item[2] for item in order_items)
            
            # Tạo đơn hàng
            order_date = datetime.now().strftime('%Y-%m-%d')
            new_order = (
                DatabaseManager.last_order_id,
                order_code,
                customer_name,
                phone,
                email or '',
                address or '',
                order_date,
                total_amount,
                'Đang xử lý',
                created_by
            )
            
            # Thêm vào mock_orders
            DatabaseManager.mock_orders = list(DatabaseManager.mock_orders) + [new_order]
            
            # Tạo chi tiết đơn hàng
            for book_id, quantity, unit_price in order_items:
                DatabaseManager.last_detail_id += 1
                subtotal = quantity * unit_price
                
                new_detail = (
                    DatabaseManager.last_detail_id,
                    DatabaseManager.last_order_id,
                    book_id,
                    quantity,
                    unit_price,
                    subtotal
                )
                DatabaseManager.mock_order_details = list(DatabaseManager.mock_order_details) + [new_detail]
                
                # Trừ kho
                if book_id in DatabaseManager.mock_inventory:
                    inv = list(DatabaseManager.mock_inventory[book_id])
                    inv[3] -= quantity  # Trừ số lượng tồn
                    DatabaseManager.mock_inventory[book_id] = tuple(inv)
            
            return True, order_code
        
        except Exception as e:
            return False, str(e)
    
    def update_order_status(self, order_id, new_status):
        """Cập nhật trạng thái đơn hàng"""
        try:
            updated_orders = []
            for order in DatabaseManager.mock_orders:
                if order[0] == order_id:
                    # Tạo tuple mới với status mới
                    updated_order = list(order)
                    updated_order[8] = new_status  # Index 8 là Status
                    updated_orders.append(tuple(updated_order))
                else:
                    updated_orders.append(order)
            
            DatabaseManager.mock_orders = tuple(updated_orders)
            return True, "Cập nhật thành công"
        except Exception as e:
            return False, str(e)
    
    def delete_order(self, order_id):
        """Xóa/Hủy đơn hàng"""
        try:
            # Cập nhật trạng thái thành "Đã hủy"
            return self.update_order_status(order_id, "Đã hủy")
        except Exception as e:
            return False, str(e)
    
    def search_orders(self, keyword):
        """Tìm kiếm đơn hàng"""
        results = []
        keyword_lower = keyword.lower()
        
        for order in DatabaseManager.mock_orders:
            if (keyword_lower in order[1].lower() or  # OrderCode
                keyword_lower in order[2].lower() or  # CustomerName
                keyword_lower in order[3].lower()):   # Phone
                results.append(order)
        
        return results
    
    def filter_orders_by_date(self, start_date, end_date):
        """Lọc đơn hàng theo ngày"""
        results = []
        for order in DatabaseManager.mock_orders:
            order_date = order[6]  # Index 6 là OrderDate
            if start_date <= order_date <= end_date:
                results.append(order)
        return results
    
    def filter_orders_by_status(self, status):
        """Lọc đơn hàng theo trạng thái"""
        if status == "Tất cả":
            return list(DatabaseManager.mock_orders)
        
        results = []
        for order in DatabaseManager.mock_orders:
            if order[8] == status:  # Index 8 là Status
                results.append(order)
        return results
    
    def get_revenue_stats(self, start_date=None, end_date=None):
        """Lấy thống kê doanh thu"""
        orders = DatabaseManager.mock_orders
        
        # Lọc theo ngày nếu có
        if start_date and end_date:
            orders = self.filter_orders_by_date(start_date, end_date)
        
        total_orders = len(orders)
        completed_orders = len([o for o in orders if o[8] == 'Hoàn thành'])
        processing_orders = len([o for o in orders if o[8] == 'Đang xử lý'])
        cancelled_orders = len([o for o in orders if o[8] == 'Đã hủy'])
        
        # Tính doanh thu (chỉ tính đơn hoàn thành)
        total_revenue = sum(o[7] for o in orders if o[8] == 'Hoàn thành')
        avg_revenue = total_revenue / completed_orders if completed_orders > 0 else 0
        
        return {
            'TotalOrders': total_orders,
            'CompletedOrders': completed_orders,
            'ProcessingOrders': processing_orders,
            'CancelledOrders': cancelled_orders,
            'TotalRevenue': total_revenue,
            'AvgRevenue': avg_revenue
        }
    
    def get_top_selling_books(self, limit=5):
        """Lấy sách bán chạy"""
        # Đếm số lượng sách đã bán
        book_sales = {}
        
        for detail in DatabaseManager.mock_order_details:
            order_id = detail[1]
            book_id = detail[2]
            quantity = detail[3]
            
            # Chỉ tính đơn hoàn thành
            order = self.get_order_by_id(order_id)
            if order and order[8] == 'Hoàn thành':
                if book_id not in book_sales:
                    book_sales[book_id] = {
                        'quantity': 0,
                        'revenue': 0
                    }
                book_sales[book_id]['quantity'] += quantity
                book_sales[book_id]['revenue'] += detail[5]  # Subtotal
        
        # Sắp xếp theo số lượng bán
        sorted_books = sorted(book_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)
        
        # Lấy thông tin chi tiết
        results = []
        for book_id, sales in sorted_books[:limit]:
            book = self.get_book_by_id(book_id)
            if book:
                results.append({
                    'BookCode': book[1],
                    'BookName': book[2],
                    'QuantitySold': sales['quantity'],
                    'Revenue': sales['revenue']
                })
        
        return results
    
    def get_daily_revenue(self, start_date, end_date):
        """Lấy doanh thu theo ngày"""
        from collections import defaultdict
        
        daily_revenue = defaultdict(float)
        
        orders = self.filter_orders_by_date(start_date, end_date)
        
        for order in orders:
            if order[8] == 'Hoàn thành':  # Chỉ tính đơn hoàn thành
                order_date = order[6]
                daily_revenue[order_date] += order[7]
        
        # Chuyển thành list [(date, revenue), ...]
        return sorted(daily_revenue.items())


def getDbConnection():
    """Mock function for DB connection."""
    class MockConnection:
        def close(self): 
            pass
    return MockConnection()