import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database.database import DatabaseConnection
from app.models.models import Product, Supplier, Warehouse, Inventory, StockEntry, InventoryHistory
from app.models.user_model import User  # Fixed "smodels" to "models"
from app.views.view import MainView
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from datetime import datetime
from app.controllers.auth_controller import AuthController
from app.models.audit_log import AuditLog
from app.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import subprocess

class Controller:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseConnection()
        self.view = MainView(root)
        
        # Initialize auth controller and audit log
        self.auth_controller = AuthController(self.db)
        self.audit_log = AuditLog(self.db)
        
        # Show login screen and get user
        self.current_user = self.auth_controller.show_login()
        
        # If login failed or was canceled, exit the application
        if not self.current_user:
            root.destroy()
            return
        
        # Update the UI with the logged-in user
        self.view.set_user(self.current_user)
        
        # Initialize models
        self.product_model = Product(self.db)
        self.supplier_model = Supplier(self.db)
        self.warehouse_model = Warehouse(self.db)
        self.inventory_model = Inventory(self.db)
        self.stock_entry_model = StockEntry(self.db)
        self.history_model = InventoryHistory(self.db)
        
        # Set up role-based UI
        self.setup_permissions()
        
        # Configure the logout button
        self.view.logout_button.config(command=self.logout)
        
        # Continue with normal setup
        self.setup_event_handlers()
        self.load_initial_data()
    
    def setup_permissions(self):
        """Apply role-based permissions to the interface"""
        user_role = self.current_user['Role']
        
        # Add admin menu for administrators
        if user_role == 'admin':
            admin_menu = self.view.add_admin_menu(self.root)
            admin_menu.entryconfig("User Management", 
                                  command=lambda: self.auth_controller.show_user_management(self.root))
            admin_menu.entryconfig("Database Backup", 
                                  command=self.backup_database)
        
        # Disable parts of the UI based on user role
        if user_role == 'warehouse_staff':
            # Warehouse staff can only use stock entries tab
            for tab_id in range(self.view.notebook.index("end")):
                if tab_id != 4:  # Stock entries tab index
                    self.view.notebook.tab(tab_id, state="disabled")
        
        # Inventory managers can't modify suppliers or warehouses
        elif user_role == 'inventory_manager':
            self.view.notebook.tab(1, state="disabled")  # Suppliers tab
            self.view.notebook.tab(2, state="disabled")  # Warehouses tab
    
    def backup_database(self):
        """Create a database backup"""
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to perform database backups")
            return
            
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = os.path.join(backup_dir, f"inventory_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
        
        try:
            # For Windows
            if os.name == 'nt':
                cmd = f'mysqldump -u{self.db.user} -p{self.db.password} {self.db.database} > "{backup_file}"'
            # For Linux/Mac
            else:
                cmd = f'mysqldump -u {self.db.user} -p{self.db.password} {self.db.database} > "{backup_file}"'
            
            subprocess.run(cmd, shell=True)
            self.view.show_info("Backup Complete", f"Database backup saved to {backup_file}")
            
            # Log the action
            self.audit_log.log_action(
                self.current_user['Username'],
                "Database Backup",
                f"Created database backup: {backup_file}"
            )
        except Exception as e:
            self.view.show_error("Backup Failed", f"Error: {str(e)}")
    
    def logout(self):
        """Handle logout and restart the application"""
        # Log the logout action
        self.audit_log.log_action(
            self.current_user['Username'],
            "Logout",
            "User logged out"
        )
        
        self.auth_controller.logout()
        
        # Restart the application
        self.root.destroy()
        new_root = ttk.Window()
        new_app = Controller(new_root)
        new_root.mainloop()
    
    def setup_event_handlers(self):
        self.view.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        self.view.products_tab.children['!labelframe2'].children['!frame'].children['!button'].configure(command=self.add_product)
        self.view.products_tab.children['!labelframe2'].children['!frame'].children['!button2'].configure(command=self.update_product)
        self.view.products_tab.children['!labelframe2'].children['!frame'].children['!button3'].configure(command=self.delete_product)
        self.view.products_tab.children['!labelframe2'].children['!frame'].children['!button4'].configure(command=self.view.clear_product_fields)

        self.view.suppliers_tree.bind('<<TreeviewSelect>>', self.on_supplier_select)
        self.view.suppliers_tab.children['!labelframe2'].children['!frame'].children['!button'].configure(command=self.add_supplier)
        self.view.suppliers_tab.children['!labelframe2'].children['!frame'].children['!button2'].configure(command=self.update_supplier)
        self.view.suppliers_tab.children['!labelframe2'].children['!frame'].children['!button3'].configure(command=self.delete_supplier)
        self.view.suppliers_tab.children['!labelframe2'].children['!frame'].children['!button4'].configure(command=self.view.clear_supplier_fields)

        self.view.warehouses_tree.bind('<<TreeviewSelect>>', self.on_warehouse_select)
        self.view.warehouses_tab.children['!labelframe2'].children['!frame'].children['!button'].configure(command=self.add_warehouse)
        self.view.warehouses_tab.children['!labelframe2'].children['!frame'].children['!button2'].configure(command=self.update_warehouse)
        self.view.warehouses_tab.children['!labelframe2'].children['!frame'].children['!button3'].configure(command=self.delete_warehouse)
        self.view.warehouses_tab.children['!labelframe2'].children['!frame'].children['!button4'].configure(command=self.view.clear_warehouse_fields)

        self.view.inventory_tree.bind('<<TreeviewSelect>>', self.on_inventory_select)
        self.view.inventory_tab.children['!labelframe'].children['!button'].configure(command=self.search_inventory)
        self.view.inventory_tab.children['!labelframe'].children['!button2'].configure(command=self.show_all_inventory)
        self.view.inventory_tab.children['!labelframe'].children['!button3'].configure(command=self.show_low_stock)

        self.view.stock_entry_tab.children['!labelframe'].children['!frame'].children['!button'].configure(command=self.add_stock_entry)
        self.view.stock_entry_tab.children['!labelframe'].children['!frame'].children['!button2'].configure(command=self.view.clear_stock_entry_fields)

        self.view.reports_tab.children['!labelframe'].children['!button'].configure(command=self.show_low_stock_report)
        self.view.reports_tab.children['!labelframe'].children['!button2'].configure(command=self.show_stock_value_report)
        self.view.reports_tab.children['!labelframe'].children['!button3'].configure(command=self.show_stock_per_warehouse)
        self.view.reports_tab.children['!labelframe'].children['!button4'].configure(command=self.show_supplier_delivery_history)
        self.view.reports_tab.children['!labelframe'].children['!button5'].configure(command=self.show_transaction_history)
        self.view.reports_tab.children['!labelframe'].children['!labelframe'].children['!button'].configure(command=self.apply_date_range)

    def load_initial_data(self):
        self.load_products()
        self.load_suppliers()
        self.load_warehouses()
        self.load_inventory()
        self.load_stock_entries()
        self.load_comboboxes()

    def load_comboboxes(self):
        products = self.product_model.get_all_products()
        warehouses = self.warehouse_model.get_all_warehouses()
        suppliers = self.supplier_model.get_all_suppliers()
        self.view.supplier_combobox['values'] = [f"{s['SupplierID']}: {s['SupplierName']}" for s in suppliers]
        self.view.inventory_product_combo['values'] = [f"{p['ProductID']}: {p['ProductName']}" for p in products]
        self.view.inventory_warehouse_combo['values'] = [f"{w['WarehouseID']}: {w['WarehouseName']}" for w in warehouses]
        self.view.entry_product_combo['values'] = [f"{p['ProductID']}: {p['ProductName']}" for p in products]
        self.view.entry_warehouse_combo['values'] = [f"{w['WarehouseID']}: {w['WarehouseName']}" for w in warehouses]

    def load_products(self):
        for item in self.view.products_tree.get_children():
            self.view.products_tree.delete(item)
        products = self.product_model.get_all_products()
        for p in products:
            self.view.products_tree.insert("", "end", values=(p['ProductID'], p['ProductName'], p['UnitPrice'], p['SupplierName']))

    def load_suppliers(self):
        for item in self.view.suppliers_tree.get_children():
            self.view.suppliers_tree.delete(item)
        suppliers = self.supplier_model.get_all_suppliers()
        for s in suppliers:
            self.view.suppliers_tree.insert("", "end", values=(s['SupplierID'], s['SupplierName'], s['Address'], s['PhoneNumber']))

    def load_warehouses(self):
        for item in self.view.warehouses_tree.get_children():
            self.view.warehouses_tree.delete(item)
        warehouses = self.warehouse_model.get_all_warehouses()
        for w in warehouses:
            self.view.warehouses_tree.insert("", "end", values=(w['WarehouseID'], w['WarehouseName'], w['Address']))

    def load_inventory(self):
        for item in self.view.inventory_tree.get_children():
            self.view.inventory_tree.delete(item)
        inventory = self.inventory_model.get_inventory_levels()
        for i in inventory:
            self.view.inventory_tree.insert("", "end", values=(i['ProductName'], i['WarehouseName'], i['Quantity'], i['MinStockLevel']))

    def load_stock_entries(self):
        for item in self.view.stock_entry_tree.get_children():
            self.view.stock_entry_tree.delete(item)
        entries = self.stock_entry_model.get_all_entries()
        for e in entries:
            self.view.stock_entry_tree.insert("", "end", values=(e['EntryID'], e['ProductName'], e['WarehouseName'], e['Quantity'], e['EntryDate']))

    def on_product_select(self, event):
        selected = self.view.products_tree.selection()
        if selected:
            item = self.view.products_tree.item(selected[0])
            product_id = item['values'][0]
            product = self.product_model.get_product_by_id(product_id)
            if product:
                self.view.product_name_var.set(product['ProductName'])
                self.view.product_desc_var.set(product['Description'] or '')
                self.view.product_price_var.set(product['UnitPrice'])
                supplier = self.supplier_model.get_supplier_by_id(product['SupplierID'])
                self.view.product_supplier_var.set(f"{supplier['SupplierID']}: {supplier['SupplierName']}")

    def on_supplier_select(self, event):
        selected = self.view.suppliers_tree.selection()
        if selected:
            item = self.view.suppliers_tree.item(selected[0])
            supplier_id = item['values'][0]
            supplier = self.supplier_model.get_supplier_by_id(supplier_id)
            if supplier:
                self.view.supplier_name_var.set(supplier['SupplierName'])
                self.view.supplier_address_var.set(supplier['Address'] or '')
                self.view.supplier_phone_var.set(supplier['PhoneNumber'] or '')

    def on_warehouse_select(self, event):
        selected = self.view.warehouses_tree.selection()
        if selected:
            item = self.view.warehouses_tree.item(selected[0])
            warehouse_id = item['values'][0]
            warehouse = self.warehouse_model.get_warehouse_by_id(warehouse_id)
            if warehouse:
                self.view.warehouse_name_var.set(warehouse['WarehouseName'])
                self.view.warehouse_address_var.set(warehouse['Address'] or '')

    def on_inventory_select(self, event):
        selected = self.view.inventory_tree.selection()
        if selected:
            item = self.view.inventory_tree.item(selected[0])
            values = item['values']
            self.view.inventory_product_var.set(values[0])
            self.view.inventory_warehouse_var.set(values[1])

    def add_product(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to add products")
            return
            
        name = self.view.product_name_var.get()
        desc = self.view.product_desc_var.get()
        price = self.view.product_price_var.get()
        supplier = self.view.product_supplier_var.get()
        if name and price and supplier:
            try:
                supplier_id = int(supplier.split(":")[0])
                if self.product_model.add_product(name, desc, float(price), supplier_id):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Add Product",
                        f"Added product '{name}' with price {price}"
                    )
                    
                    self.load_products()
                    self.load_comboboxes()
                    self.view.clear_product_fields()
                    self.view.show_info("Success", "Product added")
                else:
                    self.view.show_error("Error", "Failed to add product")
            except ValueError:
                self.view.show_error("Error", "Invalid input")
        else:
            self.view.show_error("Error", "Missing required fields")

    def update_product(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to update products")
            return
            
        selected = self.view.products_tree.selection()
        if selected:
            item = self.view.products_tree.item(selected[0])
            product_id = item['values'][0]
            name = self.view.product_name_var.get()
            desc = self.view.product_desc_var.get()
            price = self.view.product_price_var.get()
            supplier = self.view.product_supplier_var.get()
            if name and price and supplier:
                try:
                    supplier_id = int(supplier.split(":")[0])
                    if self.product_model.update_product(product_id, name, desc, float(price), supplier_id):
                        # Log the action
                        self.audit_log.log_action(
                            self.current_user['Username'],
                            "Update Product",
                            f"Updated product '{name}' (ID: {product_id})"
                        )
                        
                        self.load_products()
                        self.load_comboboxes()
                        self.view.clear_product_fields()
                        self.view.show_info("Success", "Product updated")
                    else:
                        self.view.show_error("Error", "Failed to update product")
                except ValueError:
                    self.view.show_error("Error", "Invalid input")
            else:
                self.view.show_error("Error", "Missing required fields")

    def delete_product(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to delete products")
            return
            
        selected = self.view.products_tree.selection()
        if selected:
            item = self.view.products_tree.item(selected[0])
            product_id = item['values'][0]
            product_name = item['values'][1]
            
            if self.view.ask_yes_no("Confirm", "Delete this product?"):
                if self.product_model.delete_product(product_id):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Delete Product",
                        f"Deleted product '{product_name}' (ID: {product_id})"
                    )
                    
                    self.load_products()
                    self.load_comboboxes()
                    self.view.clear_product_fields()
                    self.view.show_info("Success", "Product deleted")
                else:
                    self.view.show_error("Error", "Failed to delete product")

    def add_supplier(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to add suppliers")
            return
            
        name = self.view.supplier_name_var.get()
        address = self.view.supplier_address_var.get()
        phone = self.view.supplier_phone_var.get()
        if name:
            if self.supplier_model.add_supplier(name, address, phone):
                # Log the action
                self.audit_log.log_action(
                    self.current_user['Username'],
                    "Add Supplier",
                    f"Added supplier '{name}'"
                )
                
                self.load_suppliers()
                self.load_comboboxes()
                self.view.clear_supplier_fields()
                self.view.show_info("Success", "Supplier added")
            else:
                self.view.show_error("Error", "Failed to add supplier")
        else:
            self.view.show_error("Error", "Missing required fields")

    def update_supplier(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to update suppliers")
            return
            
        selected = self.view.suppliers_tree.selection()
        if selected:
            item = self.view.suppliers_tree.item(selected[0])
            supplier_id = item['values'][0]
            name = self.view.supplier_name_var.get()
            address = self.view.supplier_address_var.get()
            phone = self.view.supplier_phone_var.get()
            if name:
                if self.supplier_model.update_supplier(supplier_id, name, address, phone):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Update Supplier",
                        f"Updated supplier '{name}' (ID: {supplier_id})"
                    )
                    
                    self.load_suppliers()
                    self.load_comboboxes()
                    self.view.clear_supplier_fields()
                    self.view.show_info("Success", "Supplier updated")
                else:
                    self.view.show_error("Error", "Failed to update supplier")
            else:
                self.view.show_error("Error", "Missing required fields")

    def delete_supplier(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to delete suppliers")
            return
            
        selected = self.view.suppliers_tree.selection()
        if selected:
            item = self.view.suppliers_tree.item(selected[0])
            supplier_id = item['values'][0]
            supplier_name = item['values'][1]
            
            if self.view.ask_yes_no("Confirm", "Delete this supplier?"):
                if self.supplier_model.delete_supplier(supplier_id):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Delete Supplier",
                        f"Deleted supplier '{supplier_name}' (ID: {supplier_id})"
                    )
                    
                    self.load_suppliers()
                    self.load_comboboxes()
                    self.view.clear_supplier_fields()
                    self.view.show_info("Success", "Supplier deleted")
                else:
                    self.view.show_error("Error", "Failed to delete supplier")

    def add_warehouse(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to add warehouses")
            return
            
        name = self.view.warehouse_name_var.get()
        address = self.view.warehouse_address_var.get()
        if name:
            if self.warehouse_model.add_warehouse(name, address):
                # Log the action
                self.audit_log.log_action(
                    self.current_user['Username'],
                    "Add Warehouse",
                    f"Added warehouse '{name}'"
                )
                
                self.load_warehouses()
                self.load_comboboxes()
                self.view.clear_warehouse_fields()
                self.view.show_info("Success", "Warehouse added")
            else:
                self.view.show_error("Error", "Failed to add warehouse")
        else:
            self.view.show_error("Error", "Missing required fields")

    def update_warehouse(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to update warehouses")
            return
            
        selected = self.view.warehouses_tree.selection()
        if selected:
            item = self.view.warehouses_tree.item(selected[0])
            warehouse_id = item['values'][0]
            name = self.view.warehouse_name_var.get()
            address = self.view.warehouse_address_var.get()
            if name:
                if self.warehouse_model.update_warehouse(warehouse_id, name, address):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Update Warehouse",
                        f"Updated warehouse '{name}' (ID: {warehouse_id})"
                    )
                    
                    self.load_warehouses()
                    self.load_comboboxes()
                    self.view.clear_warehouse_fields()
                    self.view.show_info("Success", "Warehouse updated")
                else:
                    self.view.show_error("Error", "Failed to update warehouse")
            else:
                self.view.show_error("Error", "Missing required fields")

    def delete_warehouse(self):
        if not self.auth_controller.check_permission('admin'):
            self.view.show_error("Permission Denied", "You don't have permission to delete warehouses")
            return
            
        selected = self.view.warehouses_tree.selection()
        if selected:
            item = self.view.warehouses_tree.item(selected[0])
            warehouse_id = item['values'][0]
            warehouse_name = item['values'][1]
            
            if self.view.ask_yes_no("Confirm", "Delete this warehouse?"):
                if self.warehouse_model.delete_warehouse(warehouse_id):
                    # Log the action
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        "Delete Warehouse",
                        f"Deleted warehouse '{warehouse_name}' (ID: {warehouse_id})"
                    )
                    
                    self.load_warehouses()
                    self.load_comboboxes()
                    self.view.clear_warehouse_fields()
                    self.view.show_info("Success", "Warehouse deleted")
                else:
                    self.view.show_error("Error", "Failed to delete warehouse")

    def search_inventory(self):
        if not self.auth_controller.check_permission('warehouse_staff'):
            self.view.show_error("Permission Denied", "You don't have permission to search inventory")
            return
            
        product = self.view.inventory_product_var.get()
        warehouse = self.view.inventory_warehouse_var.get()
        inventory = self.inventory_model.get_inventory_levels()
        for item in self.view.inventory_tree.get_children():
            self.view.inventory_tree.delete(item)
        if product or warehouse:
            product_id = int(product.split(":")[0]) if product else None
            warehouse_id = int(warehouse.split(":")[0]) if warehouse else None
            filtered = [i for i in inventory if 
                      (not product_id or i['ProductID'] == product_id) and
                      (not warehouse_id or i['WarehouseID'] == warehouse_id)]
            for i in filtered:
                self.view.inventory_tree.insert("", "end", values=(i['ProductName'], i['WarehouseName'], i['Quantity'], i['MinStockLevel']))
        else:
            self.load_inventory()

    def show_all_inventory(self):
        if not self.auth_controller.check_permission('warehouse_staff'):
            self.view.show_error("Permission Denied", "You don't have permission to view inventory")
            return
            
        self.view.inventory_product_var.set("")
        self.view.inventory_warehouse_var.set("")
        self.load_inventory()

    def show_low_stock(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view low stock")
            return
            
        for item in self.view.inventory_tree.get_children():
            self.view.inventory_tree.delete(item)
        low_stock = self.inventory_model.check_low_stock()
        for item in low_stock:
            self.view.inventory_tree.insert("", "end", values=(
                item['ProductName'], 
                item['WarehouseName'], 
                item['Quantity'], 
                item['MinStockLevel']
            ))
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Low Stock",
            f"Viewed low stock items"
        )

    def add_stock_entry(self):
        if not self.auth_controller.check_permission('warehouse_staff'):
            self.view.show_error("Permission Denied", "You don't have permission to add stock entries")
            return
            
        product = self.view.entry_product_var.get()
        warehouse = self.view.entry_warehouse_var.get()
        quantity = self.view.entry_quantity_var.get()
        date = self.view.entry_date_var.get()
        trans_type = self.view.entry_type_var.get()
        
        if product and warehouse and quantity:
            try:
                product_id = int(product.split(":")[0])
                warehouse_id = int(warehouse.split(":")[0])
                quantity = int(quantity)
                if trans_type in ["Sale", "Adjustment"]:
                    quantity = -quantity
                    
                if self.stock_entry_model.add_stock_entry(product_id, warehouse_id, abs(quantity), date):
                    self.history_model.add_history_entry(product_id, warehouse_id, quantity, trans_type, date)
                    
                    # Log the action
                    product_name = product.split(":")[1].strip() if ":" in product else product
                    warehouse_name = warehouse.split(":")[1].strip() if ":" in warehouse else warehouse
                    
                    self.audit_log.log_action(
                        self.current_user['Username'],
                        f"Add {trans_type}",
                        f"Added {trans_type.lower()} entry: {abs(quantity)} of {product_name} at {warehouse_name}"
                    )
                    
                    self.load_stock_entries()
                    self.load_inventory()
                    self.view.clear_stock_entry_fields()
                    self.view.show_info("Success", "Stock entry added")
                else:
                    self.view.show_error("Error", "Failed to add stock entry")
            except ValueError:
                self.view.show_error("Error", "Invalid input")
        else:
            self.view.show_error("Error", "Missing required fields")

    def show_low_stock_report(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.view.report_text.delete(1.0, tk.END)
        low_stock = self.inventory_model.check_low_stock()
        report = "Low Stock Report\n\n"
        for item in low_stock:
            report += f"Product: {item['ProductName']}\nWarehouse: {item['WarehouseName']}\nQuantity: {item['Quantity']}\nMin Level: {item['MinStockLevel']}\n\n"
        self.view.report_text.insert(tk.END, report)
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Report",
            "Generated low stock report"
        )

    def show_stock_value_report(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.view.report_text.delete(1.0, tk.END)
        value = self.inventory_model.calculate_total_stock_value()
        report = f"Stock Value Report\n\nTotal Value: ${value:.2f}\n"
        self.view.report_text.insert(tk.END, report)
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Report",
            "Generated stock value report"
        )

    def show_stock_per_warehouse(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.view.report_text.delete(1.0, tk.END)
        report = "Stock Per Warehouse Report\n\n"
        warehouses = self.warehouse_model.get_all_warehouses()
        for w in warehouses:
            report += f"Warehouse: {w['WarehouseName']}\n"
            inventory = self.inventory_model.get_inventory_levels()
            for i in inventory:
                if i['WarehouseID'] == w['WarehouseID']:
                    report += f"  Product: {i['ProductName']}, Quantity: {i['Quantity']}\n"
            report += "\n"
        self.view.report_text.insert(tk.END, report)
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Report",
            "Generated stock per warehouse report"
        )

    def show_supplier_delivery_history(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.view.report_text.delete(1.0, tk.END)
        history = self.supplier_model.get_supplier_delivery_history()
        report = "Supplier Delivery History\n\n"
        for h in history:
            report += f"Supplier: {h['SupplierName']}\nProduct: {h['ProductName']}\nQuantity: {h['Quantity']}\nDate: {h['EntryDate']}\n\n"
        self.view.report_text.insert(tk.END, report)
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Report",
            "Generated supplier delivery history report"
        )

    def show_transaction_history(self):
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.view.report_text.delete(1.0, tk.END)
        start_date = self.view.report_from_date_var.get()
        end_date = self.view.report_to_date_var.get()
        history = self.history_model.get_history_by_date_range(start_date, end_date)
        report = f"Transaction History ({start_date} to {end_date})\n\n"
        for h in history:
            report += f"Product: {h['ProductName']}\nWarehouse: {h['WarehouseName']}\nQuantity: {h['Quantity']}\nType: {h['TransactionType']}\nDate: {h['TransactionDate']}\n\n"
        self.view.report_text.insert(tk.END, report)
        
        # Log the action
        self.audit_log.log_action(
            self.current_user['Username'],
            "View Report",
            f"Generated transaction history report ({start_date} to {end_date})"
        )

    def apply_date_range(self):
        """Apply date range filter to transaction history"""
        if not self.auth_controller.check_permission('inventory_manager'):
            self.view.show_error("Permission Denied", "You don't have permission to view reports")
            return
            
        self.show_transaction_history()