# config.py - Cấu hình hệ thống

# Cấu hình Database
DB_TYPE = "sqlite"  # sqlite, mysql, sqlserver
DB_FILE = "bookstore.db"  # Cho SQLite

# Cấu hình bảo mật
PASSWORD_MIN_LENGTH = 6
SALT_LENGTH = 32  # Độ dài salt cho mã hóa mật khẩu

# Cấu hình giao diện
WINDOW_THEME = "clam"
