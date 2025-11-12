import time
from datetime import datetime

class DatabaseManager:
    """
    Quản lý dữ liệu sách với SQL SERVER - Phiên bản hoàn chỉnh.
    
    ✅ Tất cả thao tác LƯU THẬT vào SQL Server
    ✅ Tương thích 100% với GUI hiện tại
    """
    
    def __init__(self, conn):
        """Khởi tạo với SQL Server connection"""
        self.conn = conn
        self.cursor = conn.cursor() if conn else None
        
        if not self.cursor:
            print("⚠️  WARNING: Không có kết nối database!")
    
    # ============================================================
    # BOOK INFO OPERATIONS
    # ============================================================
    
    def view_all(self):
        """Xem tất cả sách từ SQL Server"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return []
        
        try:
            query = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia,
                    ISNULL(lv.TenLinhVuc, N'') AS TenLinhVuc,
                    ISNULL(s.LoaiSach, N'') AS LoaiSach,
                    ISNULL(nxb.TenNXB, N'') AS TenNXB,
                    ISNULL(s.GiaMua, 0) AS GiaMua,
                    ISNULL(s.GiaBia, 0) AS GiaBia,
                    ISNULL(s.LanTaiBan, 0) AS LanTaiBan,
                    ISNULL(s.NamXB, '') AS NamXB
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                LEFT JOIN LinhVuc lv ON s.IdLinhVuc = lv.Id
                LEFT JOIN NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
                ORDER BY s.Id
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            # Convert to list of lists
            result = []
            for row in rows:
                result.append([
                    row[0],  # Id
                    row[1],  # MaSach
                    row[2],  # TenSach
                    row[3],  # TenTacGia
                    row[4],  # TenLinhVuc
                    row[5],  # LoaiSach
                    row[6],  # TenNXB
                    float(row[7]),  # GiaMua
                    float(row[8]),  # GiaBia
                    int(row[9]),    # LanTaiBan
                    str(row[10])    # NamXB
                ])
            
            print(f"✅ Đã tải {len(result)} sách từ database")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi view_all: {e}")
            return []
    
    def search_for_suggestion(self, query):
        """Tìm kiếm sách (autocomplete)"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                WHERE s.MaSach LIKE ? 
                   OR s.TenSach LIKE ? 
                   OR tg.TenTacGia LIKE ?
                ORDER BY s.Id
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term, search_term))
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                result.append([row[0], row[1], row[2], row[3]])
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search: {e}")
            return []
    
    def get_book_by_id(self, book_id):
        """Lấy thông tin sách theo ID"""
        if not self.cursor:
            return None
        
        try:
            query = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia,
                    ISNULL(lv.TenLinhVuc, N'') AS TenLinhVuc,
                    ISNULL(s.LoaiSach, N'') AS LoaiSach,
                    ISNULL(nxb.TenNXB, N'') AS TenNXB,
                    ISNULL(s.GiaMua, 0) AS GiaMua,
                    ISNULL(s.GiaBia, 0) AS GiaBia,
                    ISNULL(s.LanTaiBan, 0) AS LanTaiBan,
                    ISNULL(s.NamXB, '') AS NamXB
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                LEFT JOIN LinhVuc lv ON s.IdLinhVuc = lv.Id
                LEFT JOIN NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
                WHERE s.Id = ?
            """
            self.cursor.execute(query, (book_id,))
            row = self.cursor.fetchone()
            
            if row:
                return [
                    row[0], row[1], row[2], row[3], row[4],
                    row[5], row[6], float(row[7]), float(row[8]),
                    int(row[9]), str(row[10])
                ]
            return None
            
        except Exception as e:
            print(f"❌ Lỗi get_book_by_id: {e}")
            return None
    
    def get_inventory_stats(self):
        """Thống kê sách"""
        if not self.cursor:
            return {'TotalCount': 0, 'TotalQuantity': 0, 'LowStockCount': 0, 'TotalValue': 0}
        
        try:
            # Tổng số sách
            self.cursor.execute("SELECT COUNT(*) FROM Sach")
            total_count = self.cursor.fetchone()[0]
            
            # Tổng tồn kho
            self.cursor.execute("SELECT ISNULL(SUM(SoLuongTon), 0) FROM TonKho")
            total_quantity = self.cursor.fetchone()[0]
            
            # Sách sắp hết (< 50)
            self.cursor.execute("SELECT COUNT(*) FROM TonKho WHERE SoLuongTon < 50")
            low_stock = self.cursor.fetchone()[0]
            
            # Giá trị kho
            self.cursor.execute("""
                SELECT ISNULL(SUM(tk.SoLuongTon * s.GiaMua), 0)
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
            """)
            total_value = self.cursor.fetchone()[0]
            
            return {
                'TotalCount': total_count,
                'TotalQuantity': int(total_quantity),
                'LowStockCount': low_stock,
                'TotalValue': float(total_value)
            }
            
        except Exception as e:
            print(f"❌ Lỗi stats: {e}")
            return {'TotalCount': 0, 'TotalQuantity': 0, 'LowStockCount': 0, 'TotalValue': 0}
    
    def _get_or_create_id(self, table, name_column, name_value):
        """Helper: Lấy hoặc tạo ID cho bảng phụ"""
        if not name_value or not name_value.strip():
            return None
        
        try:
            # Tìm xem đã tồn tại chưa
            self.cursor.execute(f"SELECT Id FROM {table} WHERE {name_column} = ?", (name_value,))
            row = self.cursor.fetchone()
            
            if row:
                return row[0]
            
            # Chưa có → Thêm mới
            self.cursor.execute(f"INSERT INTO {table} ({name_column}) VALUES (?)", (name_value,))
            self.conn.commit()
            
            # Lấy ID vừa insert
            self.cursor.execute("SELECT @@IDENTITY")
            new_id = int(self.cursor.fetchone()[0])
            print(f"   ➕ Đã tạo {table}: {name_value} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Lỗi _get_or_create_id [{table}]: {e}")
            return None
    
    def insert_book_full(self, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban, nam_xb):
        """Thêm sách mới vào SQL Server"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return None
        
        try:
            # Lấy/Tạo ID cho các bảng phụ
            id_tac_gia = self._get_or_create_id('TacGia', 'TenTacGia', tac_gia)
            id_linh_vuc = self._get_or_create_id('LinhVuc', 'TenLinhVuc', linh_vuc)
            id_nxb = self._get_or_create_id('NhaXuatBan', 'TenNXB', nxb)
            
            # Insert sách
            query = """
                INSERT INTO Sach (MaSach, TenSach, IdTacGia, IdLinhVuc, IdNhaXuatBan, 
                                  LoaiSach, GiaMua, GiaBia, LanTaiBan, NamXB)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                ma_sach, ten_sach, id_tac_gia, id_linh_vuc, id_nxb,
                loai_sach, float(gia_mua), float(gia_bia), int(lan_tai_ban), nam_xb
            ))
            
            # Lấy ID vừa insert
            self.cursor.execute("SELECT @@IDENTITY")
            new_id = int(self.cursor.fetchone()[0])
            
            # Tự động tạo dòng tồn kho
            self.cursor.execute("""
                INSERT INTO TonKho (IdSach, SoLuongTon, ViTri)
                VALUES (?, 0, N'Chưa xác định')
            """, (new_id,))
            
            self.conn.commit()
            
            print(f"✅ Thêm sách mới ID {new_id}: {ma_sach} - {ten_sach}")
            return new_id
            
        except Exception as e:
            print(f"❌ Lỗi insert_book: {e}")
            self.conn.rollback()
            return None
    
    def update_book_full(self, book_id, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban, nam_xb):
        """Cập nhật thông tin sách"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return
        
        try:
            # Lấy/Tạo ID cho các bảng phụ
            id_tac_gia = self._get_or_create_id('TacGia', 'TenTacGia', tac_gia)
            id_linh_vuc = self._get_or_create_id('LinhVuc', 'TenLinhVuc', linh_vuc)
            id_nxb = self._get_or_create_id('NhaXuatBan', 'TenNXB', nxb)
            
            # Update sách
            query = """
                UPDATE Sach 
                SET MaSach = ?, TenSach = ?, IdTacGia = ?, IdLinhVuc = ?, 
                    IdNhaXuatBan = ?, LoaiSach = ?, GiaMua = ?, GiaBia = ?, 
                    LanTaiBan = ?, NamXB = ?, NgayCapNhat = GETDATE()
                WHERE Id = ?
            """
            self.cursor.execute(query, (
                ma_sach, ten_sach, id_tac_gia, id_linh_vuc, id_nxb,
                loai_sach, float(gia_mua), float(gia_bia), int(lan_tai_ban), nam_xb,
                book_id
            ))
            self.conn.commit()
            
            print(f"✅ Cập nhật sách ID {book_id} thành công!")
            
        except Exception as e:
            print(f"❌ Lỗi update_book: {e}")
            self.conn.rollback()
    
    def delete_book(self, book_id):
        """Xóa sách (CASCADE delete tồn kho tự động)"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return
        
        try:
            query = "DELETE FROM Sach WHERE Id = ?"
            self.cursor.execute(query, (book_id,))
            self.conn.commit()
            
            print(f"✅ Xóa sách ID {book_id} thành công!")
            
        except Exception as e:
            print(f"❌ Lỗi delete_book: {e}")
            self.conn.rollback()
    
    # ============================================================
    # INVENTORY OPERATIONS
    # ============================================================
    
    def view_inventory(self):
        """Xem tồn kho"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    tk.IdSach,
                    s.MaSach,
                    s.TenSach,
                    tk.SoLuongTon,
                    ISNULL(tk.ViTri, N'Chưa xác định') AS ViTri
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
                ORDER BY s.MaSach
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                result.append((row[0], row[1], row[2], row[3], row[4]))
            
            print(f"✅ Đã tải {len(result)} dòng tồn kho")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi view_inventory: {e}")
            return []
    
    def search_inventory_for_suggestion(self, query):
        """Tìm kiếm trong kho"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    tk.IdSach, s.MaSach, s.TenSach, tk.SoLuongTon,
                    ISNULL(tk.ViTri, N'') AS ViTri
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
                WHERE s.MaSach LIKE ? OR s.TenSach LIKE ?
                ORDER BY s.MaSach
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term))
            
            result = []
            for row in self.cursor.fetchall():
                result.append((row[0], row[1], row[2], row[3], row[4]))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_inventory: {e}")
            return []
    
    def add_stock(self, book_id, quantity, note=""):
        """Nhập kho sử dụng stored procedure"""
        if not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                EXEC sp_NhapKho 
                    @IdSach = ?, 
                    @SoLuong = ?, 
                    @NguoiThucHien = N'System',
                    @GhiChu = ?
            """, (book_id, quantity, note))
            
            result = self.cursor.fetchone()
            self.conn.commit()
            
            if result and result[0] == 1:
                print(f"✅ Nhập kho: +{quantity} quyển cho sách ID {book_id}")
                return True
            else:
                print(f"❌ Nhập kho thất bại!")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi add_stock: {e}")
            self.conn.rollback()
            return False
    
    def remove_stock(self, book_id, quantity, note=""):
        """Xuất kho sử dụng stored procedure"""
        if not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                EXEC sp_XuatKho 
                    @IdSach = ?, 
                    @SoLuong = ?, 
                    @NguoiThucHien = N'System',
                    @GhiChu = ?
            """, (book_id, quantity, note))
            
            result = self.cursor.fetchone()
            self.conn.commit()
            
            if result and result[0] == 1:
                print(f"✅ Xuất kho: -{quantity} quyển cho sách ID {book_id}")
                return True
            else:
                msg = result[1] if result else "Lỗi không xác định"
                print(f"❌ Xuất kho thất bại: {msg}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi remove_stock: {e}")
            self.conn.rollback()
            return False
    
    def update_inventory(self, book_id, new_quantity, new_location):
        """Cập nhật tồn kho thủ công"""
        if not self.cursor:
            return
        
        try:
            self.cursor.execute("""
                UPDATE TonKho 
                SET SoLuongTon = ?, ViTri = ?, NgayCapNhat = GETDATE()
                WHERE IdSach = ?
            """, (new_quantity, new_location, book_id))
            self.conn.commit()
            
            print(f"✅ Cập nhật tồn kho cho sách ID {book_id}")
            
        except Exception as e:
            print(f"❌ Lỗi update_inventory: {e}")
            self.conn.rollback()
    
    def get_transactions(self, book_id=None, limit=100):
        """Lấy lịch sử giao dịch"""
        if not self.cursor:
            return []
        
        try:
            if book_id:
                query = """
                    SELECT TOP (?) 
                        NgayGiaoDich, IdSach, LoaiGiaoDich, SoLuong, 
                        GiaTri, NguoiThucHien, GhiChu
                    FROM LichSuGiaoDich
                    WHERE IdSach = ?
                    ORDER BY NgayGiaoDich DESC
                """
                self.cursor.execute(query, (limit, book_id))
            else:
                query = """
                    SELECT TOP (?) 
                        NgayGiaoDich, IdSach, LoaiGiaoDich, SoLuong, 
                        GiaTri, NguoiThucHien, GhiChu
                    FROM LichSuGiaoDich
                    ORDER BY NgayGiaoDich DESC
                """
                self.cursor.execute(query, (limit,))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi get_transactions: {e}")
            return []
    
    # ============================================================
    # BUSINESS / ORDER OPERATIONS
    # ============================================================
    
    def get_all_orders(self):
        """Lấy tất cả đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                ORDER BY NgayDat DESC, Id DESC
            """
            self.cursor.execute(query)
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi get_all_orders: {e}")
            return []
    
    def search_orders(self, query):
        """Tìm kiếm đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                WHERE MaDonHang LIKE ? OR TenKhachHang LIKE ?
                ORDER BY NgayDat DESC
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_orders: {e}")
            return []
    
    def get_order_details(self, order_id):
        """Lấy chi tiết đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    ct.IdSach,
                    s.MaSach,
                    s.TenSach,
                    ct.SoLuong,
                    ct.DonGia,
                    ct.ThanhTien
                FROM ChiTietDonHang ct
                JOIN Sach s ON ct.IdSach = s.Id
                WHERE ct.IdDonHang = ?
            """
            self.cursor.execute(query, (order_id,))
            
            details = []
            for row in self.cursor.fetchall():
                details.append({
                    'BookID': row[0],
                    'BookCode': row[1],
                    'BookName': row[2],
                    'Quantity': row[3],
                    'UnitPrice': float(row[4]),
                    'Subtotal': float(row[5])
                })
            
            return details
            
        except Exception as e:
            print(f"❌ Lỗi get_order_details: {e}")
            return []
    
    def update_order_status(self, order_id, new_status):
        """Cập nhật trạng thái đơn"""
        if not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                UPDATE DonHang 
                SET TrangThai = ?, NgayCapNhat = GETDATE()
                WHERE Id = ?
            """, (new_status, order_id))
            self.conn.commit()
            
            print(f"✅ Cập nhật trạng thái đơn {order_id}: {new_status}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi update_order_status: {e}")
            self.conn.rollback()
            return False
    
    def get_revenue_stats(self):
        """Thống kê doanh thu chi tiết"""
        if not self.cursor:
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'TotalRevenue': 0,
                'AvgRevenue': 0
            }
        
        try:
            query = """
                SELECT 
                    COUNT(*) AS TotalOrders,
                    SUM(CASE WHEN TrangThai = N'Hoàn thành' THEN 1 ELSE 0 END) AS Completed,
                    SUM(CASE WHEN TrangThai = N'Đang xử lý' THEN 1 ELSE 0 END) AS Processing,
                    ISNULL(SUM(CASE WHEN TrangThai = N'Hoàn thành' THEN TongTien ELSE 0 END), 0) AS Revenue
                FROM DonHang
            """
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            
            total = row[0] or 0
            completed = row[1] or 0
            processing = row[2] or 0
            revenue = float(row[3] or 0)
            avg = revenue / completed if completed > 0 else 0
            
            return {
                'TotalOrders': total,
                'CompletedOrders': completed,
                'ProcessingOrders': processing,
                'TotalRevenue': revenue,
                'AvgRevenue': avg
            }
            
        except Exception as e:
            print(f"❌ Lỗi get_revenue_stats: {e}")
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'TotalRevenue': 0,
                'AvgRevenue': 0
            }
    
    def get_top_selling_books(self, limit=5):
        """Lấy sách bán chạy nhất"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT TOP (?)
                    s.Id,
                    s.MaSach,
                    s.TenSach,
                    SUM(ct.SoLuong) AS TotalSold,
                    SUM(ct.ThanhTien) AS TotalRevenue
                FROM ChiTietDonHang ct
                JOIN Sach s ON ct.IdSach = s.Id
                JOIN DonHang dh ON ct.IdDonHang = dh.Id
                WHERE dh.TrangThai = N'Hoàn thành'
                GROUP BY s.Id, s.MaSach, s.TenSach
                ORDER BY SUM(ct.SoLuong) DESC
            """
            self.cursor.execute(query, (limit,))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'BookID': row[0],
                    'BookCode': row[1],
                    'BookName': row[2],
                    'QuantitySold': int(row[3]),
                    'Revenue': float(row[4])
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Lỗi get_top_selling_books: {e}")
            return []


# Backward compatibility - import từ connection_manager
def getDbConnection():
    """Import connection từ connection_manager"""
    try:
        from connection_manager import getDbConnection as get_conn
        return get_conn()
    except:
        return None