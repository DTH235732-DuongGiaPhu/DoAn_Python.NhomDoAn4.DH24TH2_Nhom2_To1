# main.py - File chạy chính của ứng dụng
import tkinter as tk
from gui.login_window import LoginWindow
from gui.main_menu import MainMenuWindow
from connection_manager import getDbConnection  # ← SỬA: Import đúng từ connection_manager

if __name__ == '__main__':
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow, getDbConnection)
    root.mainloop()