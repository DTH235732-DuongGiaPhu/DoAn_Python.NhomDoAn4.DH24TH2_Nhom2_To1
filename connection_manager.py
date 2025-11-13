import pyodbc

# ----------------------------------------------------------------------
# --- CẤU HÌNH KẾT NỐI CSDL ---
# ----------------------------------------------------------------------
SERVER_NAME = r'LAPTOP-H1KTCC7N'
DATABASE_NAME = 'QuanLySach'
DRIVER = '{ODBC Driver 17 for SQL Server}'
# ----------------------------------------------------------------------

def getDbConnection(user=None, password=None):
    """
    Tạo và trả về đối tượng kết nối CSDL SQL Server.
    
    ✅ ĐÃ SỬA: Tắt autocommit để có thể dùng transaction
    ✅ Thêm CharacterSet=UTF-8 để hỗ trợ tiếng Việt
    """
    try:
        # Thêm 'CharacterSet=UTF-8;' vào cuối chuỗi kết nối.
        utf8_setting = 'CharacterSet=UTF-8;' 
        
        if user and password:
            # Chế độ SQL Server Authentication
            conn_string = (
                f'DRIVER={DRIVER};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                f'UID={user};'
                f'PWD={password};'
                f'{utf8_setting}'
            )
        else:
            # Chế độ Windows Authentication
            conn_string = (
                f'DRIVER={DRIVER};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                'Trusted_Connection=yes;'
                f'{utf8_setting}'
            )
        
        # Thiết lập kết nối
        conn = pyodbc.connect(conn_string)
        
        # ✅ QUAN TRỌNG: TẮT autocommit để có thể dùng transaction và rollback
        conn.autocommit = False
        
        print("✅ Kết nối SQL Server thành công!")
        return conn
        
    except Exception as e:
        print(f"❌ Lỗi kết nối CSDL SQL Server: {e}")
        return None