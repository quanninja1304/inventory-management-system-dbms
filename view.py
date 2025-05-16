import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x600")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.products_tab = ttk.Frame(self.notebook)
        self.suppliers_tab = ttk.Frame(self.notebook)
        self.warehouses_tab = ttk.Frame(self.notebook)
        self.inventory_tab = ttk.Frame(self.notebook)
        self.stock_entry_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.products_tab, text="Products")
        self.notebook.add(self.suppliers_tab, text="Suppliers")
        self.notebook.add(self.warehouses_tab, text="Warehouses")
        self.notebook.add(self.inventory_tab, text="Inventory")
        self.notebook.add(self.stock_entry_tab, text="Stock Entries")
        self.notebook.add(self.reports_tab, text="Reports")
        
        self.setup_products_tab()
        self.setup_suppliers_tab()
        self.setup_warehouses_tab()
        self.setup_inventory_tab()
        self.setup_stock_entry_tab()
        self.setup_reports_tab()
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN).pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_products_tab(self):
        left_frame = ttk.LabelFrame(self.products_tab, text="Product List")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.products_tree = ttk.Treeview(left_frame, columns=("ID", "Name", "Price", "Supplier"), show="headings")
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Supplier", text="Supplier")
        self.products_tree.column("ID", width=50)
        self.products_tree.column("Name", width=150)
        self.products_tree.column("Price", width=80)
        self.products_tree.column("Supplier", width=100)
        self.products_tree.pack(fill="both", expand=True)
        
        right_frame = ttk.LabelFrame(self.products_tab, text="Product Details")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(right_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.product_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.product_desc_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.product_desc_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.product_price_var = tk.DoubleVar()
        ttk.Entry(right_frame, textvariable=self.product_price_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Supplier:").grid(row=3, column=0, padx=5, pady=5)
        self.product_supplier_var = tk.StringVar()
        self.supplier_combobox = ttk.Combobox(right_frame, textvariable=self.product_supplier_var)
        self.supplier_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Add").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear").pack(side=tk.LEFT, padx=5)
        
        self.products_tab.columnconfigure(0, weight=3)
        self.products_tab.columnconfigure(1, weight=2)
        self.products_tab.rowconfigure(0, weight=1)
    
    def setup_suppliers_tab(self):
        left_frame = ttk.LabelFrame(self.suppliers_tab, text="Supplier List")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.suppliers_tree = ttk.Treeview(left_frame, columns=("ID", "Name", "Address", "Phone"), show="headings")
        self.suppliers_tree.heading("ID", text="ID")
        self.suppliers_tree.heading("Name", text="Name")
        self.suppliers_tree.heading("Address", text="Address")
        self.suppliers_tree.heading("Phone", text="Phone")
        self.suppliers_tree.column("ID", width=50)
        self.suppliers_tree.column("Name", width=100)
        self.suppliers_tree.column("Address", width=150)
        self.suppliers_tree.column("Phone", width=100)
        self.suppliers_tree.pack(fill="both", expand=True)
        
        right_frame = ttk.LabelFrame(self.suppliers_tab, text="Supplier Details")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(right_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.supplier_name_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.supplier_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        self.supplier_address_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.supplier_address_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.supplier_phone_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.supplier_phone_var).grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Add").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear").pack(side=tk.LEFT, padx=5)
        
        self.suppliers_tab.columnconfigure(0, weight=3)
        self.suppliers_tab.columnconfigure(1, weight=2)
        self.suppliers_tab.rowconfigure(0, weight=1)
    
    def setup_warehouses_tab(self):
        left_frame = ttk.LabelFrame(self.warehouses_tab, text="Warehouse List")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.warehouses_tree = ttk.Treeview(left_frame, columns=("ID", "Name", "Address"), show="headings")
        self.warehouses_tree.heading("ID", text="ID")
        self.warehouses_tree.heading("Name", text="Name")
        self.warehouses_tree.heading("Address", text="Address")
        self.warehouses_tree.column("ID", width=50)
        self.warehouses_tree.column("Name", width=100)
        self.warehouses_tree.column("Address", width=150)
        self.warehouses_tree.pack(fill="both", expand=True)
        
        right_frame = ttk.LabelFrame(self.warehouses_tab, text="Warehouse Details")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(right_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.warehouse_name_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.warehouse_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        self.warehouse_address_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.warehouse_address_var).grid(row=1, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Add").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear").pack(side=tk.LEFT, padx=5)
        
        self.warehouses_tab.columnconfigure(0, weight=3)
        self.warehouses_tab.columnconfigure(1, weight=2)
        self.warehouses_tab.rowconfigure(0, weight=1)
    
    def setup_inventory_tab(self):
        top_frame = ttk.LabelFrame(self.inventory_tab, text="Inventory Search")
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        ttk.Label(top_frame, text="Product:").grid(row=0, column=0, padx=5, pady=5)
        self.inventory_product_var = tk.StringVar()
        self.inventory_product_combo = ttk.Combobox(top_frame, textvariable=self.inventory_product_var)
        self.inventory_product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(top_frame, text="Warehouse:").grid(row=0, column=2, padx=5, pady=5)
        self.inventory_warehouse_var = tk.StringVar()
        self.inventory_warehouse_combo = ttk.Combobox(top_frame, textvariable=self.inventory_warehouse_var)
        self.inventory_warehouse_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Search").grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(top_frame, text="Show All").grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(top_frame, text="Low Stock").grid(row=0, column=6, padx=5, pady=5)
        
        bottom_frame = ttk.LabelFrame(self.inventory_tab, text="Inventory List")
        bottom_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)
        
        self.inventory_tree = ttk.Treeview(bottom_frame, columns=("Product", "Warehouse", "Quantity", "MinLevel"), show="headings")
        self.inventory_tree.heading("Product", text="Product")
        self.inventory_tree.heading("Warehouse", text="Warehouse")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("MinLevel", text="Min Level")
        self.inventory_tree.column("Product", width=150)
        self.inventory_tree.column("Warehouse", width=100)
        self.inventory_tree.column("Quantity", width=80)
        self.inventory_tree.column("MinLevel", width=80)
        self.inventory_tree.pack(fill="both", expand=True)
        
        self.inventory_tab.columnconfigure(0, weight=1)
        self.inventory_tab.rowconfigure(1, weight=1)
    
    def setup_stock_entry_tab(self):
        left_frame = ttk.LabelFrame(self.stock_entry_tab, text="New Stock Entry")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(left_frame, text="Product:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_product_var = tk.StringVar()
        self.entry_product_combo = ttk.Combobox(left_frame, textvariable=self.entry_product_var)
        self.entry_product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Warehouse:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_warehouse_var = tk.StringVar()
        self.entry_warehouse_combo = ttk.Combobox(left_frame, textvariable=self.entry_warehouse_var)
        self.entry_warehouse_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_quantity_var = tk.IntVar()
        ttk.Entry(left_frame, textvariable=self.entry_quantity_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Date:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(left_frame, textvariable=self.entry_date_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Type:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_type_var = tk.StringVar(value="StockEntry")
        ttk.Radiobutton(left_frame, text="Stock Entry", variable=self.entry_type_var, value="StockEntry").grid(row=4, column=1, sticky="w")
        ttk.Radiobutton(left_frame, text="Sale", variable=self.entry_type_var, value="Sale").grid(row=5, column=1, sticky="w")
        ttk.Radiobutton(left_frame, text="Adjustment", variable=self.entry_type_var, value="Adjustment").grid(row=6, column=1, sticky="w")
        
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Add Entry").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear").pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.LabelFrame(self.stock_entry_tab, text="Stock Entry History")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.stock_entry_tree = ttk.Treeview(right_frame, columns=("ID", "Product", "Warehouse", "Quantity", "Date"), show="headings")
        self.stock_entry_tree.heading("ID", text="ID")
        self.stock_entry_tree.heading("Product", text="Product")
        self.stock_entry_tree.heading("Warehouse", text="Warehouse")
        self.stock_entry_tree.heading("Quantity", text="Quantity")
        self.stock_entry_tree.heading("Date", text="Date")
        self.stock_entry_tree.column("ID", width=50)
        self.stock_entry_tree.column("Product", width=100)
        self.stock_entry_tree.column("Warehouse", width=100)
        self.stock_entry_tree.column("Quantity", width=80)
        self.stock_entry_tree.column("Date", width=100)
        self.stock_entry_tree.pack(fill="both", expand=True)
        
        self.stock_entry_tab.columnconfigure(0, weight=1)
        self.stock_entry_tab.columnconfigure(1, weight=1)
        self.stock_entry_tab.rowconfigure(0, weight=1)
    
    def setup_reports_tab(self):
        left_frame = ttk.LabelFrame(self.reports_tab, text="Reports")
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        
        ttk.Button(left_frame, text="Low Stock").pack(pady=5, fill="x")
        ttk.Button(left_frame, text="Stock Value").pack(pady=5, fill="x")
        ttk.Button(left_frame, text="Stock Per Warehouse").pack(pady=5, fill="x")
        ttk.Button(left_frame, text="Supplier Delivery").pack(pady=5, fill="x")
        ttk.Button(left_frame, text="Transaction History").pack(pady=5, fill="x")
        
        date_frame = ttk.LabelFrame(left_frame, text="Date Range")
        date_frame.pack(pady=5, fill="x")
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, padx=5, pady=5)
        self.report_from_date_var = tk.StringVar(value=datetime.now().replace(day=1).strftime('%Y-%m-%d'))
        ttk.Entry(date_frame, textvariable=self.report_from_date_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(date_frame, text="To:").grid(row=1, column=0, padx=5, pady=5)
        self.report_to_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(date_frame, textvariable=self.report_to_date_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(date_frame, text="Apply").grid(row=2, column=0, columnspan=2, pady=5)
        
        right_frame = ttk.LabelFrame(self.reports_tab, text="Report Results")
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.report_text = tk.Text(right_frame, height=20)
        self.report_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.reports_tab.columnconfigure(1, weight=1)
        self.reports_tab.rowconfigure(0, weight=1)
    
    def clear_product_fields(self):
        self.product_name_var.set("")
        self.product_desc_var.set("")
        self.product_price_var.set(0.0)
        self.product_supplier_var.set("")
    
    def clear_supplier_fields(self):
        self.supplier_name_var.set("")
        self.supplier_address_var.set("")
        self.supplier_phone_var.set("")
    
    def clear_warehouse_fields(self):
        self.warehouse_name_var.set("")
        self.warehouse_address_var.set("")
    
    def clear_stock_entry_fields(self):
        self.entry_product_var.set("")
        self.entry_warehouse_var.set("")
        self.entry_quantity_var.set(0)
        self.entry_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.entry_type_var.set("StockEntry")
    
    def show_info(self, title, message):
        messagebox.showinfo(title, message)
    
    def show_error(self, title, message):
        messagebox.showerror(title, message)
    
    def ask_yes_no(self, title, message):
        return messagebox.askyesno(title, message)