# utils/helpers.py - Các hàm tiện ích NÂNG CẤP

def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def format_currency(amount):
    """
    Format số tiền theo chuẩn Việt Nam
    
    Args:
        amount: Số tiền (int hoặc float)
    
    Returns:
        str: Số tiền đã format (vd: "1,234,567 đ")
    
    Examples:
        >>> format_currency(1234567)
        '1,234,567 đ'
        >>> format_currency(0)
        '0 đ'
    """
    try:
        amount = float(amount)
        if amount == 0:
            return "0 đ"
        return f"{amount:,.0f} đ".replace(',', '.')
    except (ValueError, TypeError):
        return "0 đ"


def format_number(number):
    """
    Format số với dấu phân cách hàng nghìn
    
    Args:
        number: Số cần format
    
    Returns:
        str: Số đã format
    
    Examples:
        >>> format_number(1234567)
        '1,234,567'
    """
    try:
        number = int(number)
        return f"{number:,}"
    except (ValueError, TypeError):
        return "0"


def validate_positive_number(value, field_name="Số"):
    """
    Kiểm tra số dương
    
    Args:
        value: Giá trị cần kiểm tra
        field_name: Tên trường (để hiển thị lỗi)
    
    Returns:
        tuple: (is_valid: bool, message: str, parsed_value: float/int)
    
    Examples:
        >>> validate_positive_number("100", "Giá")
        (True, "", 100.0)
        >>> validate_positive_number("-10", "Giá")
        (False, "Giá phải là số dương!", None)
    """
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} phải là số dương!", None
        return True, "", num
    except ValueError:
        return False, f"{field_name} không hợp lệ!", None


def validate_year(year_str):
    """
    Kiểm tra năm hợp lệ
    
    Args:
        year_str: Chuỗi năm
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        year = int(year_str)
        if year < 1800 or year > 2100:
            return False, "Năm phải từ 1800 đến 2100!"
        return True, ""
    except ValueError:
        return False, "Năm không hợp lệ!"


def validate_not_empty(value, field_name="Trường"):
    """
    Kiểm tra không để trống
    
    Args:
        value: Giá trị cần kiểm tra
        field_name: Tên trường
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not value or not value.strip():
        return False, f"{field_name} không được để trống!"
    return True, ""


def get_stock_status(quantity):
    """
    Xác định trạng thái tồn kho
    
    Args:
        quantity: Số lượng tồn
    
    Returns:
        tuple: (status: str, color: str, icon: str)
    
    Examples:
        >>> get_stock_status(30)
        ('Sắp hết', '#F44336', '🔴')
        >>> get_stock_status(75)
        ('Cảnh báo', '#FF9800', '🟡')
        >>> get_stock_status(150)
        ('Tốt', '#4CAF50', '🟢')
    """
    try:
        qty = int(quantity)
        if qty < 50:
            return "Sắp hết", "#F44336", "🔴"
        elif qty < 100:
            return "Cảnh báo", "#FF9800", "🟡"
        else:
            return "Tốt", "#4CAF50", "🟢"
    except (ValueError, TypeError):
        return "Không xác định", "#9E9E9E", "⚪"


def truncate_text(text, max_length=50):
    """
    Cắt ngắn văn bản
    
    Args:
        text: Văn bản cần cắt
        max_length: Độ dài tối đa
    
    Returns:
        str: Văn bản đã cắt
    """
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def calculate_profit(gia_mua, gia_ban, so_luong=1):
    """
    Tính lợi nhuận
    
    Args:
        gia_mua: Giá mua
        gia_ban: Giá bán
        so_luong: Số lượng
    
    Returns:
        float: Lợi nhuận
    """
    try:
        return (float(gia_ban) - float(gia_mua)) * int(so_luong)
    except (ValueError, TypeError):
        return 0.0


def calculate_profit_margin(gia_mua, gia_ban):
    """
    Tính tỷ suất lợi nhuận (%)
    
    Args:
        gia_mua: Giá mua
        gia_ban: Giá bán
    
    Returns:
        float: Tỷ suất lợi nhuận (%)
    """
    try:
        gia_mua = float(gia_mua)
        gia_ban = float(gia_ban)
        if gia_mua == 0:
            return 0.0
        return ((gia_ban - gia_mua) / gia_mua) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def format_phone_number(phone):
    """
    Format số điện thoại
    
    Args:
        phone: Số điện thoại
    
    Returns:
        str: Số điện thoại đã format
    
    Examples:
        >>> format_phone_number("0123456789")
        '012-345-6789'
    """
    phone = str(phone).replace(" ", "").replace("-", "")
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone


def validate_email(email):
    """
    Kiểm tra email hợp lệ
    
    Args:
        email: Địa chỉ email
    
    Returns:
        bool: True nếu hợp lệ
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_color_scheme():
    """
    Trả về bảng màu chuẩn chuyên nghiệp
    
    Returns:
        dict: Bảng màu
    """
    return {
        'primary': '#1976D2',      # Blue
        'success': '#4CAF50',      # Green
        'warning': '#FF9800',      # Orange
        'danger': '#F44336',       # Red
        'info': '#00BCD4',         # Cyan
        'light': '#F5F5F5',        # Light Gray
        'dark': '#212121',         # Dark Gray
        'white': '#FFFFFF',        # White
        'border': '#E0E0E0',       # Border Gray
    }


def show_loading_message(parent, message="Đang xử lý..."):
    """
    Hiển thị loading message
    
    Args:
        parent: Widget cha
        message: Thông báo
    
    Returns:
        Label widget (để có thể destroy sau)
    """
    import tkinter as tk
    loading = tk.Label(parent,
        text=f"⏳ {message}",
        font=('Segoe UI', 11),
        bg='#FFF8E1',
        fg='#F57C00',
        padx=20,
        pady=10)
    return loading


def confirm_action(title, message):
    """
    Hiển thị dialog xác nhận
    
    Args:
        title: Tiêu đề
        message: Nội dung
    
    Returns:
        bool: True nếu Yes
    """
    from tkinter import messagebox
    return messagebox.askyesno(title, message)


def show_success(message):
    """Hiển thị thông báo thành công"""
    from tkinter import messagebox
    messagebox.showinfo("Thành công", f"✅ {message}")


def show_error(message):
    """Hiển thị thông báo lỗi"""
    from tkinter import messagebox
    messagebox.showerror("Lỗi", f"❌ {message}")


def show_warning(message):
    """Hiển thị cảnh báo"""
    from tkinter import messagebox
    messagebox.showwarning("Cảnh báo", f"⚠️ {message}")


def show_info(message):
    """Hiển thị thông tin"""
    from tkinter import messagebox
    messagebox.showinfo("Thông tin", f"ℹ️ {message}")