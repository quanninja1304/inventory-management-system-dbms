import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.views.auth_view import LoginView, UserManagementView
from app.models.user_model import User
from app.models.audit_log import AuditLog
from datetime import datetime

import hashlib

class AuthController:
    def __init__(self, db_connection):
        self.db = db_connection
        self.user_model = User(db_connection)
        self.audit_log = AuditLog(db_connection)
        self.current_user = None
    
    def show_login(self):
        """Display the login screen and return the logged-in user"""
        login_window = tk.Toplevel()
        login_view = LoginView(login_window)
        login_view.on_login = lambda: self.handle_login(login_view, login_window)
        
        # Make this window modal
        login_window.transient(login_window.master)
        login_window.grab_set()
        login_window.wait_window()
        
        return self.current_user
    
    def handle_login(self, login_view, login_window):
        """Handle login attempt"""
        username = login_view.username_var.get()
        password = login_view.password_var.get()
        
        if not username or not password:
            login_view.status_var.set("Please enter username and password")
            return
        
        user = self.user_model.authenticate(username, password)
        
        if user:
            if not user['Active']:
                login_view.status_var.set("This account is deactivated")
                self.audit_log.log_action(username, "Failed Login", "Account deactivated")
                return
                
            self.current_user = user
            # Log successful login
            self.audit_log.log_action(username, "Login", "Successful login")
            login_window.destroy()
        else:
            # Log failed login attempt
            self.audit_log.log_action(username, "Failed Login", "Invalid username or password")
            login_view.status_var.set("Invalid username or password")
    
    def logout(self):
        """Handle logout"""
        if self.current_user:
            # Log logout
            self.audit_log.log_action(self.current_user['Username'], "Logout", "User logged out")
        self.current_user = None
    
    def check_permission(self, required_role):
        """Check if current user has the required role"""
        if not self.current_user:
            return False
            
        if required_role == 'admin' and self.current_user['Role'] == 'admin':
            return True
        elif required_role == 'inventory_manager' and self.current_user['Role'] in ['admin', 'inventory_manager']:
            return True
        elif required_role == 'warehouse_staff' and self.current_user['Role'] in ['admin', 'inventory_manager', 'warehouse_staff']:
            return True
            
        return False
    
    def get_role_permissions(self, role):
        """Get the permissions for a specific role"""
        permissions = {
            'admin': {
                'can_manage_users': True,
                'can_manage_products': True,
                'can_manage_suppliers': True,
                'can_manage_warehouses': True,
                'can_manage_inventory': True,
                'can_view_reports': True,
                'can_backup': True
            },
            'inventory_manager': {
                'can_manage_users': False,
                'can_manage_products': True,
                'can_manage_suppliers': False,
                'can_manage_warehouses': False,
                'can_manage_inventory': True,
                'can_view_reports': True,
                'can_backup': False
            },
            'warehouse_staff': {
                'can_manage_users': False,
                'can_manage_products': False,
                'can_manage_suppliers': False,
                'can_manage_warehouses': False,
                'can_manage_inventory': False,
                'can_manage_stock': True,
                'can_view_reports': False,
                'can_backup': False
            }
        }
        return permissions.get(role, {})
    
    def has_permission(self, permission):
        """Check if the current user has a specific permission"""
        if not self.current_user:
            return False
        
        role = self.current_user['Role']
        permissions = self.get_role_permissions(role)
        return permissions.get(permission, False)
    
    def show_user_management(self, parent):
        """Show user management window"""
        if not self.check_permission('admin'):
            messagebox.showerror("Permission Denied", "You don't have permission to access this feature")
            return
            
        user_mgmt_view = UserManagementView(parent)
        
        # Set up event handlers
        user_mgmt_view.add_button.config(command=lambda: self.add_user(user_mgmt_view))
        user_mgmt_view.update_button.config(command=lambda: self.update_user(user_mgmt_view))
        user_mgmt_view.delete_button.config(command=lambda: self.delete_user(user_mgmt_view))
        user_mgmt_view.clear_button.config(command=user_mgmt_view.clear_form)
        user_mgmt_view.users_tree.bind('<<TreeviewSelect>>', lambda event: self.on_user_select(event, user_mgmt_view))
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "Access User Management",
            "Opened user management screen"
        )
        
        # Load user data
        self.load_users(user_mgmt_view)
    
    def load_users(self, view):
        """Load users into the treeview"""
        for item in view.users_tree.get_children():
            view.users_tree.delete(item)
            
        users = self.user_model.get_all_users()
        for user in users:
            view.users_tree.insert("", "end", values=(
                user['UserID'],
                user['Username'],
                user['FullName'] or "",
                user['Role'],
                "Yes" if user['Active'] else "No"
            ))
    
    def on_user_select(self, event, view):
        """Handle user selection in treeview"""
        selected = view.users_tree.selection()
        if selected:
            item = view.users_tree.item(selected[0])
            user_id = item['values'][0]
            user = self.user_model.get_user_by_id(user_id)
            
            if user:
                view.username_var.set(user['Username'])
                view.fullname_var.set(user['FullName'] or '')
                view.email_var.set(user['Email'] or '')
                view.role_var.set(user['Role'])
                view.active_var.set(user['Active'])
                view.password_var.set("")  # Clear password field
    
    def add_user(self, view):
        """Add a new user"""
        username = view.username_var.get()
        fullname = view.fullname_var.get()
        email = view.email_var.get()
        password = view.password_var.get()
        role = view.role_var.get()
        
        if not username or not password or not role:
            messagebox.showerror("Error", "Username, password and role are required")
            return
            
        success, message = self.user_model.create_user(username, password, fullname, email, role)
        
        if success:
            # Log the action
            self.audit_log.log_action(
                self.current_user['Username'],
                "Add User",
                f"Added user '{username}' with role '{role}'"
            )
            
            messagebox.showinfo("Success", message)
            view.clear_form()
            self.load_users(view)
        else:
            messagebox.showerror("Error", message)
    
    def update_user(self, view):
        """Update an existing user"""
        selected = view.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to update")
            return
            
        item = view.users_tree.item(selected[0])
        user_id = item['values'][0]
        username = view.username_var.get()
        
        fullname = view.fullname_var.get()
        email = view.email_var.get()
        role = view.role_var.get()
        active = view.active_var.get()
        password = view.password_var.get()
        
        # Update user details
        success = self.user_model.update_user(user_id, fullname, email, role, active)
        
        # If password provided, update it too
        if password and success:
            success = self.user_model.change_password(user_id, password)
            
        if success:
            # Log the action
            self.audit_log.log_action(
                self.current_user['Username'],
                "Update User",
                f"Updated user '{username}' (ID: {user_id})"
            )
            
            messagebox.showinfo("Success", "User updated successfully")
            view.clear_form()
            self.load_users(view)
        else:
            messagebox.showerror("Error", "Failed to update user")
                
    def delete_user(self, view):
        """Delete a user"""
        selected = view.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete")
            return
            
        item = view.users_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # Prevent deleting yourself
        if username == self.current_user['Username']:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            if self.user_model.delete_user(user_id):
                # Log the action
                self.audit_log.log_action(
                    self.current_user['Username'],
                    "Delete User",
                    f"Deleted user '{username}' (ID: {user_id})"
                )
                
                messagebox.showinfo("Success", "User deleted successfully")
                view.clear_form()
                self.load_users(view)
            else:
                messagebox.showerror("Error", "Failed to delete user")