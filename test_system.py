#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script kiểm tra hệ thống sau khi cài đặt
Chạy file này để đảm bảo mọi thứ hoạt động đúng
"""

import sys
import os

def print_header(text):
    """In header đẹp"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """In thông báo thành công"""
    print(f"✅ {text}")

def print_error(text):
    """In thông báo lỗi"""
    print(f"❌ {text}")

def print_info(text):
    """In thông tin"""
    print(f"ℹ️  {text}")

def test_imports():
    """Test import các thư viện cần thiết"""
    print_header("KIỂM TRA THƯ VIỆN")
    
    errors = []
    
    # Test pyodbc
    try:
        import pyodbc
        print_success(f"pyodbc - Version: {pyodbc.version}")
    except ImportError:
        print_error("pyodbc chưa được cài đặt")
        errors.append("Cài đặt: pip install pyodbc")
    
    # Test tkinter
    try:
        import tkinter as tk
        print_success(f"tkinter - Version: {tk.TkVersion}")
    except ImportError:
        print_error("tkinter chưa được cài đặt")
        errors.append("tkinter thường đi kèm Python, cài lại Python nếu thiếu")
    
    # Test hashlib
    try:
        import hashlib
        print_success("hashlib - OK")
    except ImportError:
        print_error("hashlib chưa có")
        errors.append("hashlib là thư viện chuẩn Python")
    
    return len(errors) == 0, errors

def test_connection():
    """Test kết nối SQL Server"""
    print_header("KIỂM TRA KẾT NỐI SQL SERVER")
    
    try:
        from connection_manager import getDbConnection
        
        print_info("Đang thử kết nối...")
        conn = getDbConnection()
        
        if conn:
            print_success("Kết nối SQL Server thành công!")
            
            # Test query
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print_info(f"SQL Server Version: {version[:80]}...")
            
            conn.close()
            return True, []
        else:
            print_error("Không thể kết nối SQL Server")
            return False, ["Kiểm tra connection_manager.py và SQL Server"]
    
    except Exception as e:
        print_error(f"Lỗi kết nối: {str(e)}")
        return False, [str(e)]

def test_database():
    """Test database QuanLySach"""
    print_header("KIỂM TRA DATABASE QUANLYSACH")
    
    try:
        from connection_manager import getDbConnection
        
        conn = getDbConnection()
        if not conn:
            print_error("Không có kết nối")
            return False, ["Không thể kết nối database"]
        
        cursor = conn.cursor()
        errors = []
        
        # Kiểm tra các bảng chính
        tables_to_check = [
            'TacGia', 'LinhVuc', 'NhaXuatBan', 'Sach', 
            'TonKho', 'LichSuGiaoDich', 'DonHang', 'ChiTietDonHang',
            'Users'  # Bảng mới
        ]
        
        print_info("Kiểm tra các bảng:")
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print_success(f"Bảng {table}: {count} dòng")
            except Exception as e:
                print_error(f"Bảng {table}: KHÔNG TỒN TẠI")
                errors.append(f"Bảng {table} chưa được tạo")
        
        # Kiểm tra stored procedures
        print_info("\nKiểm tra Stored Procedures:")
        sp_to_check = [
            'sp_NhapKho', 'sp_XuatKho',
            'sp_GetUserByUsername', 'sp_UpdateLastLogin', 'sp_CreateUser'
        ]
        
        for sp in sp_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM sys.procedures WHERE name = '{sp}'")
            exists = cursor.fetchone()[0]
            if exists:
                print_success(f"SP {sp}: OK")
            else:
                print_error(f"SP {sp}: KHÔNG TỒN TẠI")
                errors.append(f"Stored Procedure {sp} chưa được tạo")
        
        conn.close()
        return len(errors) == 0, errors
    
    except Exception as e:
        print_error(f"Lỗi: {str(e)}")
        return False, [str(e)]

def test_user_manager():
    """Test UserManager"""
    print_header("KIỂM TRA USER MANAGER")
    
    try:
        from database.user_manager import UserManager
        
        print_info("Khởi tạo UserManager...")
        user_mgr = UserManager()
        print_success("UserManager khởi tạo thành công")
        
        # Test check username exists
        print_info("Test kiểm tra username 'admin'...")
        exists = user_mgr.check_username_exists('admin')
        if exists:
            print_success("Tài khoản admin đã tồn tại")
        else:
            print_error("Tài khoản admin chưa tồn tại")
            return False, ["Chạy script 02_add_users_table.sql để tạo tài khoản admin"]
        
        return True, []
    
    except Exception as e:
        print_error(f"Lỗi UserManager: {str(e)}")
        return False, [str(e)]

def test_file_structure():
    """Test cấu trúc thư mục"""
    print_header("KIỂM TRA CẤU TRÚC THƯ MỤC")
    
    required_files = [
        'main.py',
        'config.py',
        'connection_manager.py',
        'database/user_manager.py',
        'database/book_database.py',
        'database/__init__.py',
        'gui/login_window.py',
        'gui/main_menu.py',
        'gui/__init__.py',
        'utils/helpers.py',
        'utils/__init__.py'
    ]
    
    errors = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - KHÔNG TỒN TẠI")
            errors.append(f"Thiếu file: {file_path}")
    
    return len(errors) == 0, errors

def main():
    """Hàm chính"""
    print("\n" + "🔍"*30)
    print("   SCRIPT KIỂM TRA HỆ THỐNG QUẢN LÝ SÁCH")
    print("🔍"*30)
    
    all_passed = True
    all_errors = []
    
    # Test 1: Thư viện
    passed, errors = test_imports()
    all_passed = all_passed and passed
    all_errors.extend(errors)
    
    # Test 2: File structure
    passed, errors = test_file_structure()
    all_passed = all_passed and passed
    all_errors.extend(errors)
    
    # Test 3: Kết nối
    passed, errors = test_connection()
    all_passed = all_passed and passed
    all_errors.extend(errors)
    
    # Test 4: Database
    if passed:  # Chỉ test nếu kết nối OK
        passed, errors = test_database()
        all_passed = all_passed and passed
        all_errors.extend(errors)
    
    # Test 5: UserManager
    if passed:  # Chỉ test nếu database OK
        passed, errors = test_user_manager()
        all_passed = all_passed and passed
        all_errors.extend(errors)
    
    # Tổng kết
    print_header("KẾT QUẢ TỔNG THỂ")
    
    if all_passed:
        print("\n🎉 " + "="*56)
        print("   HOÀN HẢO! TẤT CẢ KIỂM TRA ĐỀU THÀNH CÔNG!")
        print("   Hệ thống sẵn sàng sử dụng!")
        print("   Chạy: python main.py")
        print("="*60 + " 🎉\n")
        return 0
    else:
        print("\n⚠️  " + "="*56)
        print("   CÓ LỖI XẢY RA! VUI LÒNG KIỂM TRA LẠI!")
        print("="*60 + " ⚠️\n")
        
        print("📋 DANH SÁCH LỖI VÀ GIẢI PHÁP:")
        for i, error in enumerate(all_errors, 1):
            print(f"   {i}. {error}")
        
        print("\n💡 HƯỚNG DẪN KHẮC PHỤC:")
        print("   1. Đọc kỹ file README.md")
        print("   2. Đảm bảo đã chạy cả 2 script SQL")
        print("   3. Kiểm tra connection_manager.py")
        print("   4. Đảm bảo SQL Server đang chạy")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
