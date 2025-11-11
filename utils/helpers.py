# utils/helpers.py - Các hàm tiện ích
import tkinter as tk

def center_window(win, w, h):
    """Căn giữa cửa sổ trên màn hình"""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

def validate_number(value, allow_decimal=True):
    """Kiểm tra giá trị có phải là số không"""
    if not value:
        return False
    try:
        if allow_decimal:
            float(value)
        else:
            int(value)
        return True
    except ValueError:
        return False

def format_currency(amount):
    """Format số tiền"""
    try:
        return f"{float(amount):,.0f} đ"
    except:
        return "0 đ"

def validate_email(email):
    """Kiểm tra email hợp lệ (đơn giản)"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None if email else True