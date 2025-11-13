# config.py - Cấu hình hệ thống

# ================================================================
# CẤU HÌNH DATABASE - SQL SERVER
# ================================================================

# Loại database
DB_TYPE = "sqlserver"  # sqlserver (không còn dùng sqlite, mysql)

# Cấu hình SQL Server (được quản lý trong connection_manager.py)
# SERVER_NAME, DATABASE_NAME, DRIVER sẽ được cấu hình trong connection_manager.py

# ================================================================
# CẤU HÌNH BẢO MẬT
# ================================================================

# Mật khẩu
PASSWORD_MIN_LENGTH = 6  # Độ dài tối thiểu của mật khẩu
SALT_LENGTH = 32  # Độ dài salt cho mã hóa mật khẩu (bytes)

# Session timeout (phút)
SESSION_TIMEOUT = 30

# ================================================================
# CẤU HÌNH GIAO DIỆN
# ================================================================

# Theme
WINDOW_THEME = "clam"  # clam, alt, default, classic

# Colors
COLORS = {
    'primary': '#1976D2',      # Blue
    'success': '#4CAF50',      # Green
    'warning': '#FF9800',      # Orange
    'danger': '#F44336',       # Red
    'info': '#00BCD4',         # Cyan
    'purple': '#9C27B0',       # Purple
    'light': '#F5F5F5',        # Light Gray
    'dark': '#212121',         # Dark Gray
    'white': '#FFFFFF',        # White
    'border': '#E0E0E0',       # Border Gray
}

# Font settings
FONT_FAMILY = 'Segoe UI'
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_MEDIUM = 11
FONT_SIZE_LARGE = 12
FONT_SIZE_TITLE = 16
FONT_SIZE_HEADER = 18

# ================================================================
# CẤU HÌNH NGHIỆP VỤ
# ================================================================

# Kho hàng
LOW_STOCK_THRESHOLD = 50  # Ngưỡng cảnh báo sắp hết hàng
CRITICAL_STOCK_THRESHOLD = 20  # Ngưỡng nguy hiểm

# Đơn hàng
ORDER_STATUSES = ["Đang xử lý", "Hoàn thành", "Đã hủy"]
DEFAULT_ORDER_STATUS = "Đang xử lý"

# Vị trí kho mặc định
DEFAULT_LOCATIONS = [
    "Kệ A1", "Kệ A2", 
    "Kệ B1", "Kệ B2", 
    "Kệ C1", "Kệ C2", "Kệ C3",
    "Kệ D1", "Kệ D2", "Kệ D3", "Kệ D4"
]

# Loại sách
BOOK_TYPES = ["Sách Nước Ngoài", "Sách Trong Nước"]

# ================================================================
# CẤU HÌNH LOGGING & DEBUG
# ================================================================

# Debug mode
DEBUG_MODE = True  # Bật/tắt chế độ debug

# Log level
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# ================================================================
# CẤU HÌNH PAGINATION & DISPLAY
# ================================================================

# Số dòng hiển thị mặc định trong Treeview
DEFAULT_TREE_HEIGHT = 15

# Số lượng records mỗi trang (cho pagination nếu cần)
RECORDS_PER_PAGE = 50

# ================================================================
# CẤU HÌNH APPLICATION
# ================================================================

# Thông tin ứng dụng
APP_NAME = "Hệ Thống Quản Lý Sách"
APP_VERSION = "2.0"
APP_AUTHOR = "Development Team"

# Window sizes
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# ================================================================
# CẤU HÌNH BÁO CÁO & EXPORT
# ================================================================

# Export formats
EXPORT_FORMATS = ["Excel", "PDF", "CSV"]

# Report types
REPORT_TYPES = [
    "Báo cáo tồn kho",
    "Báo cáo doanh thu",
    "Báo cáo nhập xuất",
    "Báo cáo sách bán chạy"
]

# ================================================================
# CẤU HÌNH EMAIL (TÙY CHỌN - CHO TÍNH NĂNG TƯƠNG LAI)
# ================================================================

# SMTP settings (nếu cần gửi email)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USE_TLS = True
SMTP_USERNAME = ""  # Điền khi cần
SMTP_PASSWORD = ""  # Điền khi cần

# ================================================================
# CẤU HÌNH BACKUP (TÙY CHỌN)
# ================================================================

# Tự động backup
AUTO_BACKUP = False
BACKUP_INTERVAL_DAYS = 7  # Backup mỗi 7 ngày
BACKUP_PATH = "./backups/"

# ================================================================
# GHI CHÚ
# ================================================================
"""
Config này đã được cập nhật để phù hợp với SQL Server database.
Tất cả các cấu hình kết nối SQL Server được quản lý trong connection_manager.py
để đảm bảo tính bảo mật và dễ quản lý.

Các module khác sẽ import các hằng số cần thiết từ file này.
"""