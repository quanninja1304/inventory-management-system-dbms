import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ttkbootstrap as ttk
from controllers.controller import Controller
from tkinter import messagebox

class MainApp:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        
        # Khởi tạo Controller với role
        self.controller = Controller(root, role)
        
        # Xử lý sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    # Nhận role từ tham số dòng lệnh, mặc định là 'user' nếu không có
    role = sys.argv[1] if len(sys.argv) > 1 else 'user'
    
    # Khởi tạo cửa sổ với theme flatly
    root = ttk.Window(themename="flatly")
    app = MainApp(root, role)
    root.mainloop()