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
from views.login_view import LoginApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()