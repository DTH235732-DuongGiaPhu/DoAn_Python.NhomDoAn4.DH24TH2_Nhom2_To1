# database/user_manager.py - Quản lý người dùng
import sqlite3
import hashlib
import os
from config import DB_FILE, PASSWORD_MIN_LENGTH, SALT_LENGTH

class UserManager:
    def __init__(self):
        self.db_file = DB_FILE
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database và bảng users"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tạo bảng users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password, salt=None):
        """Mã hóa mật khẩu với salt"""
        if salt is None:
            salt = os.urandom(SALT_LENGTH).hex()
        
        # Sử dụng SHA-256 để hash
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt
    
    def register_user(self, username, password, full_name="", email="", role="user"):
        """Đăng ký người dùng mới"""
        # Kiểm tra độ dài mật khẩu
        if len(password) < PASSWORD_MIN_LENGTH:
            return False, f"Mật khẩu phải có ít nhất {PASSWORD_MIN_LENGTH} ký tự"
        
        # Kiểm tra username đã tồn tại chưa
        if self.check_username_exists(username):
            return False, "Tên đăng nhập đã tồn tại"
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Mã hóa mật khẩu
            password_hash, salt = self.hash_password(password)
            
            # Thêm user vào database
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, full_name, email, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, salt, full_name, email, role))
            
            conn.commit()
            conn.close()
            return True, "Đăng ký thành công"
        
        except sqlite3.IntegrityError:
            return False, "Tên đăng nhập đã tồn tại"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def login(self, username, password):
        """Đăng nhập - xác thực người dùng"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Lấy thông tin user
            cursor.execute('''
                SELECT id, password_hash, salt, full_name, role 
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            
            if result is None:
                conn.close()
                return False, "Tên đăng nhập không tồn tại"
            
            user_id, stored_hash, salt, full_name, role = result
            
            # Kiểm tra mật khẩu
            password_hash, _ = self.hash_password(password, salt)
            
            if password_hash == stored_hash:
                # Cập nhật thời gian đăng nhập
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                conn.commit()
                conn.close()
                
                # Trả về thông tin user
                return True, {
                    "user_id": user_id,
                    "username": username,
                    "full_name": full_name,
                    "role": role
                }
            else:
                conn.close()
                return False, "Mật khẩu không đúng"
        
        except Exception as e:
            return False, f"Lỗi đăng nhập: {str(e)}"
    
    def check_username_exists(self, username):
        """Kiểm tra username đã tồn tại chưa"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            conn.close()
            return result is not None
        
        except Exception:
            return False
    
    def change_password(self, username, old_password, new_password):
        """Đổi mật khẩu"""
        # Xác thực mật khẩu cũ
        success, result = self.login(username, old_password)
        if not success:
            return False, "Mật khẩu cũ không đúng"
        
        # Kiểm tra mật khẩu mới
        if len(new_password) < PASSWORD_MIN_LENGTH:
            return False, f"Mật khẩu mới phải có ít nhất {PASSWORD_MIN_LENGTH} ký tự"
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Tạo hash mới cho mật khẩu mới
            password_hash, salt = self.hash_password(new_password)
            
            # Cập nhật mật khẩu
            cursor.execute('''
                UPDATE users SET password_hash = ?, salt = ?
                WHERE username = ?
            ''', (password_hash, salt, username))
            
            conn.commit()
            conn.close()
            return True, "Đổi mật khẩu thành công"
        
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def get_all_users(self):
        """Lấy danh sách tất cả users (cho admin)"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, full_name, email, role, created_at, last_login
                FROM users
                ORDER BY created_at DESC
            ''')
            
            users = cursor.fetchall()
            conn.close()
            return users
        
        except Exception as e:
            print(f"Lỗi: {e}")
            return []