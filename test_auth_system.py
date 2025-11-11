#!/usr/bin/env python3
# test_auth_system.py - Script test hệ thống đăng nhập/đăng ký

from database.user_manager import UserManager

def test_registration():
    """Test chức năng đăng ký"""
    print("=" * 60)
    print("TEST HỆ THỐNG ĐĂNG KÝ NGƯỜI DÙNG")
    print("=" * 60)
    
    user_manager = UserManager()
    
    # Test 1: Đăng ký user admin
    print("\n1. Đăng ký user admin...")
    success, message = user_manager.register_user(
        username="admin",
        password="admin123",
        full_name="Quản Trị Viên",
        email="admin@bookstore.com",
        role="admin"
    )
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Test 2: Đăng ký user thường
    print("\n2. Đăng ký user thường...")
    success, message = user_manager.register_user(
        username="nhanvien1",
        password="123456",
        full_name="Nguyễn Văn A",
        email="nhanvien1@bookstore.com",
        role="user"
    )
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Test 3: Đăng ký user thường khác
    print("\n3. Đăng ký user khác...")
    success, message = user_manager.register_user(
        username="nhanvien2",
        password="123456",
        full_name="Trần Thị B",
        email="nhanvien2@bookstore.com"
    )
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Test 4: Đăng ký trùng username (phải lỗi)
    print("\n4. Test đăng ký trùng username...")
    success, message = user_manager.register_user(
        username="admin",
        password="password",
        full_name="Test User"
    )
    print(f"   {'✅' if not success else '❌'} {message}")
    
    # Test 5: Mật khẩu quá ngắn (phải lỗi)
    print("\n5. Test mật khẩu quá ngắn...")
    success, message = user_manager.register_user(
        username="test",
        password="123",
        full_name="Test User"
    )
    print(f"   {'✅' if not success else '❌'} {message}")

def test_login():
    """Test chức năng đăng nhập"""
    print("\n" + "=" * 60)
    print("TEST HỆ THỐNG ĐĂNG NHẬP")
    print("=" * 60)
    
    user_manager = UserManager()
    
    # Test 1: Đăng nhập thành công với admin
    print("\n1. Đăng nhập với admin...")
    success, result = user_manager.login("admin", "admin123")
    if success:
        print(f"   ✅ Đăng nhập thành công!")
        print(f"      - User ID: {result['user_id']}")
        print(f"      - Username: {result['username']}")
        print(f"      - Họ tên: {result['full_name']}")
        print(f"      - Vai trò: {result['role']}")
    else:
        print(f"   ❌ {result}")
    
    # Test 2: Đăng nhập thành công với user thường
    print("\n2. Đăng nhập với nhanvien1...")
    success, result = user_manager.login("nhanvien1", "123456")
    if success:
        print(f"   ✅ Đăng nhập thành công!")
        print(f"      - Họ tên: {result['full_name']}")
    else:
        print(f"   ❌ {result}")
    
    # Test 3: Sai mật khẩu (phải lỗi)
    print("\n3. Test sai mật khẩu...")
    success, result = user_manager.login("admin", "wrongpassword")
    print(f"   {'✅' if not success else '❌'} {result}")
    
    # Test 4: Username không tồn tại (phải lỗi)
    print("\n4. Test username không tồn tại...")
    success, result = user_manager.login("khongtontai", "123456")
    print(f"   {'✅' if not success else '❌'} {result}")

def test_change_password():
    """Test chức năng đổi mật khẩu"""
    print("\n" + "=" * 60)
    print("TEST ĐỔI MẬT KHẨU")
    print("=" * 60)
    
    user_manager = UserManager()
    
    # Test 1: Đổi mật khẩu thành công
    print("\n1. Đổi mật khẩu cho nhanvien1...")
    success, message = user_manager.change_password("nhanvien1", "123456", "newpass123")
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Test 2: Đăng nhập với mật khẩu mới
    if success:
        print("\n2. Đăng nhập với mật khẩu mới...")
        success, result = user_manager.login("nhanvien1", "newpass123")
        print(f"   {'✅' if success else '❌'} {'Đăng nhập thành công!' if success else result}")
    
    # Test 3: Sai mật khẩu cũ (phải lỗi)
    print("\n3. Test sai mật khẩu cũ...")
    success, message = user_manager.change_password("admin", "wrongpass", "newpass")
    print(f"   {'✅' if not success else '❌'} {message}")

def show_all_users():
    """Hiển thị tất cả users trong hệ thống"""
    print("\n" + "=" * 60)
    print("DANH SÁCH TẤT CẢ NGƯỜI DÙNG TRONG HỆ THỐNG")
    print("=" * 60)
    
    user_manager = UserManager()
    users = user_manager.get_all_users()
    
    if users:
        print(f"\nTổng số: {len(users)} người dùng\n")
        for i, user in enumerate(users, 1):
            user_id, username, full_name, email, role, created_at, last_login = user
            print(f"{i}. {username}")
            print(f"   - Họ tên: {full_name}")
            print(f"   - Email: {email if email else 'Chưa có'}")
            print(f"   - Vai trò: {role}")
            print(f"   - Ngày tạo: {created_at}")
            print(f"   - Đăng nhập lần cuối: {last_login if last_login else 'Chưa đăng nhập'}")
            print()
    else:
        print("Không có user nào trong hệ thống!")

if __name__ == '__main__':
    print("\n🚀 BẮT ĐẦU TEST HỆ THỐNG XÁC THỰC\n")
    
    # Chạy các test
    test_registration()
    test_login()
    test_change_password()
    show_all_users()
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH TẤT CẢ CÁC TEST")
    print("=" * 60)
    print("\n📌 Thông tin đăng nhập mặc định:")
    print("   - Admin: username='admin', password='admin123'")
    print("   - User: username='nhanvien1', password='newpass123'")
    print("   - User: username='nhanvien2', password='123456'")
    print("\n💡 Bây giờ bạn có thể chạy: python3 main.py")
    print("   để test giao diện đăng nhập/đăng ký\n")