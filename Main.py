# main.py - File chạy chính của ứng dụng
import tkinter as tk
from gui.login_window import LoginWindow
from gui.main_menu import MainMenuWindow
from database.book_database import getDbConnection

if __name__ == '__main__':
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow, getDbConnection)
    root.mainloop()
