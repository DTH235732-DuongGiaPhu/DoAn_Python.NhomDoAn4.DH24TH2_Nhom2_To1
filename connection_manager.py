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
    Đã thêm 'CharacterSet=UTF-8;' để khắc phục lỗi tiếng Việt/khoảng trắng.
    """
    try:
        # XÓA BỎ MỌI HÀM VÀ CODE VỀ pyodbc.converters HOẶC register_output_converter Ở ĐÂY!
        
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
                f'{utf8_setting}' # <--- Đã thêm
            )
        else:
            # Chế độ Windows Authentication
            conn_string = (
                f'DRIVER={DRIVER};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                'Trusted_Connection=yes;'
                f'{utf8_setting}' # <--- Đã thêm
            )
        
        # Thiết lập kết nối
        conn = pyodbc.connect(conn_string)
        # Thiết lập autocommit mặc định là True cho các thao tác đơn giản
        conn.autocommit = True 
        
        return conn
        
    except Exception as e:
        print(f"Lỗi kết nối CSDL SQL Server: {e}")
        return None