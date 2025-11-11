# utils/__init__.py - Export các hàm từ helpers

from .helpers import (
    center_window,
    format_currency,
    format_number,
    validate_positive_number,
    validate_year,
    validate_not_empty,
    get_stock_status,
    truncate_text,
    calculate_profit,
    calculate_profit_margin,
    format_phone_number,
    validate_email,
    get_color_scheme,
    show_success,
    show_error,
    show_warning,
    show_info
)

# Hàm validate_number để tương thích ngược với code cũ
def validate_number(value):
    """Kiểm tra số hợp lệ (backward compatibility)"""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

__all__ = [
    'center_window',
    'format_currency',
    'format_number',
    'validate_number',
    'validate_positive_number',
    'validate_year',
    'validate_not_empty',
    'get_stock_status',
    'validate_email'
]