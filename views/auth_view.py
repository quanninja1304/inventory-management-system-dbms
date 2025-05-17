import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the form
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(main_frame, text="Inventory Management System", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(main_frame, text="Login", font=("Arial", 12)).pack(pady=5)
        
        # Login form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill="x")
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.password_var, width=30, show="*").grid(row=1, column=1, pady=5)
        
        # Login button
        ttk.Button(main_frame, text="Login", command=self.on_login).pack(pady=10)
        
        # Status message
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, foreground="red").pack(pady=5)
    
    def on_login(self):
        """Will be configured by auth controller later"""
        pass


class UserManagementView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("800x500")
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Left frame for user list
        left_frame = ttk.LabelFrame(main_frame, text="User List")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # User treeview
        self.users_tree = ttk.Treeview(left_frame, columns=("ID", "Username", "Name", "Role", "Active"), show="headings")
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Username", text="Username")
        self.users_tree.heading("Name", text="Full Name")
        self.users_tree.heading("Role", text="Role")
        self.users_tree.heading("Active", text="Active")
        
        self.users_tree.column("ID", width=50)
        self.users_tree.column("Username", width=100)
        self.users_tree.column("Name", width=150)
        self.users_tree.column("Role", width=100)
        self.users_tree.column("Active", width=50)
        
        self.users_tree.pack(fill="both", expand=True)
        
        # Right frame for user details
        right_frame = ttk.LabelFrame(main_frame, text="User Details")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # User form
        ttk.Label(right_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(right_frame, text="Full Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.fullname_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.fullname_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(right_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(right_frame, text="Password:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.password_var, show="*").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(right_frame, text="Role:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.role_var = tk.StringVar()
        role_combo = ttk.Combobox(right_frame, textvariable=self.role_var)
        role_combo['values'] = ('admin', 'inventory_manager', 'warehouse_staff')
        role_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(right_frame, text="Active:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_frame, variable=self.active_var).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        # Button frame
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.add_button = ttk.Button(button_frame, text="Add User")
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(button_frame, text="Update User")
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text="Delete User")
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear")
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Set grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        right_frame.columnconfigure(1, weight=1)
    
    def clear_form(self):
        self.username_var.set("")
        self.fullname_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.role_var.set("")
        self.active_var.set(True)