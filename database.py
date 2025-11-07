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
            s.Id, s.TieuDe, tg.TenTacGia, nxb.TenNhaXuatBan, lv.TenLinhVuc, s.NamXuatBan, s.SoLuong
        FROM 
            Sach s
        JOIN 
            TacGia tg ON s.IdTacGia = tg.Id
        JOIN 
            NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
        JOIN 
            LinhVuc lv ON s.IdLinhVuc = lv.Id
        ORDER BY 
            s.Id
        """
        # Thêm phần còn thiếu để hoàn thành phương thức view_all
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        # Xử lý kết quả để loại bỏ khoảng trắng và dấu nháy thừa (thường do pyodbc/SQL Server trả về)
        cleaned_rows = []
        for row in rows:
            cleaned_row = tuple(
                item.strip() if isinstance(item, str) else item 
                for item in row
            )
            cleaned_rows.append(cleaned_row)
            
        return cleaned_rows