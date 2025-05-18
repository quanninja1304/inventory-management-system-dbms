import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
import subprocess
import sys
import hashlib
import os
from PIL import Image, ImageTk
import io
from config import (
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
    configure_logging
)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("750x450")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.primary_color = "#4287f5"  # Blue accent color
        self.secondary_color = "#f0f5ff"  # Light blue background
        self.text_color = "#333333"  # Dark text
        self.button_color = "#4287f5"  # Button color
        
        self.root.configure(bg="white")
        
        # Database configuration
        self.db_config = {
            'host': DB_HOST,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME
        }
        
        # Font configuration
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=16)
        self.label_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Main container
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Left side - Image area (blue background with illustration)
        self.left_frame = tk.Frame(self.main_frame, bg=self.secondary_color, width=400)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Place for the inventory icon
        self.icon_frame = tk.Frame(self.left_frame, bg=self.secondary_color, width=200, height=200)
        self.icon_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Load the inventory icon (gear with boxes image)
        try:
            # Create a placeholder for the icon
            # In a real application, you would load the image from a file
            # For now, we'll create a label with the text "Inventory System" as a placeholder
            self.inventory_icon_label = tk.Label(
                self.icon_frame,
                text="",  # No text, will be replaced with image
                bg=self.secondary_color
            )
            self.inventory_icon_label.pack(padx=20, pady=20)
            
            # Here you would normally load the image like this:
            icon_path = "ui/ui.png"
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((200,200), Image.LANCZOS)
            self.inventory_icon = ImageTk.PhotoImage(icon_img)
            self.inventory_icon_label.config(image=self.inventory_icon)
            
        except Exception as e:
            print(f"Couldn't load image: {e}")
            # Fallback text if image fails to load
            self.inventory_icon_label.config(
                text="Inventory\nSystem",
                font=self.title_font,
                fg=self.primary_color
            )
        
        # Add illustration description text
        self.illustration_label = tk.Label(
            self.left_frame,
            text="Inventory Management System",
            font=("Helvetica", 14, "bold"),
            fg=self.primary_color,
            bg=self.secondary_color
        )
        self.illustration_label.place(relx=0.5, rely=0.65, anchor="center")
        
        # Right side - Login form
        self.right_frame = tk.Frame(self.main_frame, bg="white", width=400)
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # Login form container
        self.login_container = tk.Frame(self.right_frame, bg="white")
        self.login_container.place(relx=0.5, rely=0.5, anchor="center", width=300)
        
        # Sign in title
        self.sign_in_label = tk.Label(
            self.login_container,
            text="Sign in",
            font=self.title_font,
            fg=self.primary_color,
            bg="white"
        )
        self.sign_in_label.pack(anchor="w", pady=(0, 30))
        
        # Username
        self.username_label = tk.Label(
            self.login_container,
            text="Username",
            font=self.label_font,
            fg=self.text_color,
            bg="white",
            anchor="w"
        )
        self.username_label.pack(anchor="w", pady=(0, 5))
        
        # Style for entry fields - modern underlined look
        self.style = ttk.Style()
        self.style.configure(
            "TEntry",
            fieldbackground="white"
        )
        
        # Custom frame for underlined effect
        # self.username_frame = tk.Frame(self.login_container, bg=self.text_color, height=2)
        self.username_entry = ttk.Entry(
            self.login_container,
            width=30,
            font=self.label_font,
            style="TEntry"
        )
        self.username_entry.pack(fill="x", ipady=5)
        # self.username_frame.pack(fill="x", pady=(0, 20))
        self.username_entry.pack(fill="x", ipady=5, pady=(0, 20))
        
        # Password
        self.password_label = tk.Label(
            self.login_container,
            text="Password",
            font=self.label_font,
            fg=self.text_color,
            bg="white",
            anchor="w"
        )
        self.password_label.pack(anchor="w", pady=(0, 5))
        
        # Password entry with underline
        self.password_entry = ttk.Entry(
            self.login_container,
            width=30,
            font=self.label_font,
            show="•"
        )
        self.password_entry.pack(fill="x", ipady=5, pady=(0, 30))
        
        # self.password_frame = tk.Frame(self.login_container, bg=self.text_color, height=2)
        # self.password_frame.pack(fill="x", pady=(0, 30))
        
        # Login button
        self.style.configure(
            "Blue.TButton",
            font=self.button_font,
            background=self.button_color,
            foreground="white"
        )
        
        self.login_button = tk.Button(
            self.login_container,
            text="Sign in",
            command=self.login,
            font=self.button_font,
            bg=self.primary_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#3a76d6",
            activeforeground="white"
        )
        self.login_button.pack(fill="x", ipady=8)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self.login_container,
            textvariable=self.status_var,
            fg="red",
            bg="white",
            font=self.label_font
        )
        self.status_label.pack(pady=15)
        
        
        # Set focus to username field
        self.username_entry.focus()
        
        # Bind enter key to login function
        self.root.bind("<Return>", lambda event: self.login())
        
    def hash_password(self, password):
        """Hash password using MD5."""
        return hashlib.md5(password.encode()).hexdigest()
        
    def login(self):
        """Handle user login with database authentication."""
        self.status_var.set("")
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_var.set("Username and password are required.")
            return
        
        self.status_var.set("Authenticating...")
        self.root.update()
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            query = "SELECT role FROM User WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()
            
            if result:
                role = result[0]
                messagebox.showinfo("Success", f"Login successful! Welcome, {role}")
                conn.close()
                self.root.destroy()
                subprocess.run([sys.executable, "views/main_view.py", role])
            else:
                self.status_var.set("Invalid username or password")
                
            conn.close()
            
        except mysql.connector.Error as err:
            self.status_var.set(f"Database error. Please try again.")
            print(f"Database error: {err}")

    def load_inventory_icon(self):
        """
        For a real application, you would implement loading the gear/box icon here
        This is a placeholder function showing how to load the external image
        """
        try:
            # Example code for loading an image file
            icon_path = "inventory_icon.png"  # Path to your gear/box icon
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((150, 150), Image.LANCZOS)
                self.inventory_icon = ImageTk.PhotoImage(icon_img)
                self.inventory_icon_label.config(image=self.inventory_icon)
        except Exception as e:
            print(f"Error loading inventory icon: {e}")