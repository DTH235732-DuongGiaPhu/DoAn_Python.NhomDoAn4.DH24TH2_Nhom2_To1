import pyodbc
from connection_manager import getDbConnection 
 
class DatabaseManager:
    """Quản lý các thao tác CSDL cho ứng dụng quản lý sách, 
        hỗ trợ mô hình chuẩn hóa 4 bảng."""
    
    def __init__(self, conn=None):
        if conn is None:
            # Nếu conn là None, thử tạo kết nối mới
            self.conn = getDbConnection()
        else:
            self.conn = conn
 
        if self.conn is None:
            raise ConnectionError("Không thể tạo kết nối CSDL.")
        
        self.cursor = self.conn.cursor()
 
    # ----------------------------------------------------------------------
    # --- HÀM HỖ TRỢ CHUYỂN ĐỔI TÊN -> ID (DÙNG CHO INSERT/UPDATE) ---
    # ----------------------------------------------------------------------
 
    def get_id_from_name(self, table_name, name_column, name_value):
        """Hàm chung để tìm ID từ tên, nếu chưa có thì tạo mới."""
        name_value = name_value.strip()
        if not name_value:
             return None # Trả về None nếu tên trống
 
        # Ngăn chặn SQL Injection
        if table_name not in ['TacGia', 'NhaXuatBan', 'LinhVuc']:
            raise ValueError("Tên bảng không hợp lệ.")
             
        # 1. Tìm ID hiện tại
        find_sql = f"SELECT Id FROM {table_name} WHERE {name_column} = ?"
        self.cursor.execute(find_sql, (name_value,))
        result = self.cursor.fetchone()
         
        if result:
            return result[0]
        else:
            # 2. Nếu không tìm thấy, tạo mới và lấy ID
            insert_sql = f"INSERT INTO {table_name} ({name_column}) VALUES (?)"
            self.cursor.execute(insert_sql, (name_value,))
            self.conn.commit()
             
            # Lấy ID của dòng vừa được chèn (áp dụng cho SQL Server)
            return self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
 
    # ----------------------------------------------------------------------
    # --- LOGIC THAO TÁC CSDL (ĐÃ DÙNG JOIN VÀ ID) ---
    # ----------------------------------------------------------------------
             
    def view_all(self):
        """
        Lấy tất cả dữ liệu sách, đã thêm logic để loại bỏ dấu nháy đơn và khoảng trắng thừa
        từ các chuỗi kết quả (khắc phục lỗi hiển thị Treeview).
        """
        query = """
        SELECT 
            S.Id, S.MaSach, S.TenSach, 
            ISNULL(TG.TenTacGia, '') AS TenTacGia,      
            ISNULL(LV.TenLinhVuc, '') AS TenLinhVuc,  
            S.LoaiSach, 
            ISNULL(NXB.TenNXB, '') AS TenNXB,           
            S.GiaMua, S.GiaBia, S.LanTaiBan, S.NamXB 
        FROM Sach S
        LEFT JOIN TacGia TG ON S.IdTacGia = TG.Id
        LEFT JOIN LinhVuc LV ON S.IdLinhVuc = LV.Id
        LEFT JOIN NhaXuatBan NXB ON S.IdNhaXuatBan = NXB.Id
        ORDER BY S.TenSach
        """
        try:
            self.cursor.execute(query)
            raw_results = self.cursor.fetchall()
            
            # --- CHUẨN HÓA KẾT QUẢ TRẢ VỀ ---
            clean_results = []
            for row in raw_results:
                clean_row = []
                for value in row:
                    if isinstance(value, str):
                        # Loại bỏ dấu nháy đơn ở đầu và cuối, sau đó loại bỏ khoảng trắng thừa
                        clean_value = value.strip().strip("'")
                        clean_row.append(clean_value)
                    else:
                        # Giữ nguyên giá trị số (Id, Giá Mua, Giá Bìa, Lần TB)
                        clean_row.append(value)
                clean_results.append(tuple(clean_row)) # Chuyển lại thành tuple
                
            return clean_results # Trả về kết quả đã được làm sạch
            
        except pyodbc.Error as e:
            raise Exception(f"Lỗi khi tải dữ liệu từ CSDL: {e}")
            
    def insert_book_full(self, MaSach, TenSach, TacGiaName, LinhVucName, LoaiSach, NXBName, GiaMua, GiaBia, LanTaiBan, NamXB):
        """Thêm một cuốn sách mới, chuyển tên thành ID trước khi lưu."""
        # LƯU Ý LỖI: Cần đảm bảo MaSach không trùng lặp (UNIQUE KEY)
        try:
            # Chuyển tên thành ID
            id_tg = self.get_id_from_name('TacGia', 'TenTacGia', TacGiaName)
            id_lv = self.get_id_from_name('LinhVuc', 'TenLinhVuc', LinhVucName)
            id_nxb = self.get_id_from_name('NhaXuatBan', 'TenNXB', NXBName)
            
            sql = """
            INSERT INTO Sach (MaSach, TenSach, IdTacGia, IdLinhVuc, IdNhaXuatBan, LoaiSach, GiaMua, GiaBia, LanTaiBan, NamXB)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            data = (MaSach, TenSach, id_tg, id_lv, id_nxb, LoaiSach, float(GiaMua), float(GiaBia), int(LanTaiBan), NamXB)
            
            self.cursor.execute(sql, data)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            # Lỗi UNIQUE KEY sẽ hiển thị ở đây
            raise Exception(f"Lỗi SQL Server: {e}")
 
    def update_book_full(self, db_id, MaSach, TenSach, TacGiaName, LinhVucName, LoaiSach, NXBName, GiaMua, GiaBia, LanTaiBan, NamXB):
        """Cập nhật thông tin sách, chuyển tên thành ID trước khi lưu."""
        # LƯU Ý LỖI: Cần đảm bảo MaSach không trùng lặp (UNIQUE KEY) với sách khác
        try:
            # Chuyển tên thành ID
            id_tg = self.get_id_from_name('TacGia', 'TenTacGia', TacGiaName)
            id_lv = self.get_id_from_name('LinhVuc', 'TenLinhVuc', LinhVucName)
            id_nxb = self.get_id_from_name('NhaXuatBan', 'TenNXB', NXBName)
            
            sql = """
            UPDATE Sach SET MaSach=?, TenSach=?, IdTacGia=?, IdLinhVuc=?, IdNhaXuatBan=?, LoaiSach=?, GiaMua=?, GiaBia=?, LanTaiBan=?, NamXB=?
            WHERE Id=?
            """
            data = (MaSach, TenSach, id_tg, id_lv, id_nxb, LoaiSach, float(GiaMua), float(GiaBia), int(LanTaiBan), NamXB, db_id)
            
            self.cursor.execute(sql, data)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            raise Exception(f"Lỗi SQL Server: {e}")
 
    def delete_book(self, db_id):
        """Xóa một cuốn sách dựa trên Id (Primary Key trong DB)."""
        sql = "DELETE FROM Sach WHERE Id=?"
        try:
            self.cursor.execute(sql, (db_id,))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            raise Exception(f"Lỗi SQL Server: {e}")
            
    def search_for_suggestion(self, query):
        """Tìm kiếm sách có gợi ý, sử dụng JOIN để tìm kiếm theo tên Tác giả."""
        search_pattern = '%' + query + '%'
        sql = """
        SELECT TOP 10 S.Id, S.MaSach, S.TenSach, ISNULL(TG.TenTacGia, '') 
        FROM Sach S
        LEFT JOIN TacGia TG ON S.IdTacGia = TG.Id
        WHERE S.TenSach LIKE ? OR TG.TenTacGia LIKE ? OR S.MaSach LIKE ?
        ORDER BY S.TenSach
        """
        try:
            self.cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            return []
            
    def get_book_by_id(self, db_id):
        """Lấy thông tin sách chi tiết theo Id, sử dụng JOIN để lấy TÊN. (Đã tối ưu truy vấn)"""
        sql = """
        SELECT 
            S.Id, S.MaSach, S.TenSach, 
            ISNULL(TG.TenTacGia, '') AS TenTacGia,      
            ISNULL(LV.TenLinhVuc, '') AS TenLinhVuc,  
            S.LoaiSach, 
            ISNULL(NXB.TenNXB, '') AS TenNXB,           
            S.GiaMua, S.GiaBia, S.LanTaiBan, S.NamXB 
        FROM Sach S
        LEFT JOIN TacGia TG ON S.IdTacGia = TG.Id
        LEFT JOIN LinhVuc LV ON S.IdLinhVuc = LV.Id
        LEFT JOIN NhaXuatBan NXB ON S.IdNhaXuatBan = NXB.Id
        WHERE S.Id = ?
        """
        try:
            self.cursor.execute(sql, (db_id,))
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            return None