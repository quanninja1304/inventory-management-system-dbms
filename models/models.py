from datetime import datetime

class Product:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_products(self):
        query = """
        SELECT p.*, s.SupplierName 
        FROM Products p
        LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID
        """
        return self.db.fetch_all(query)
    
    def get_product_by_id(self, product_id):
        query = "SELECT * FROM Products WHERE ProductID = %s"
        return self.db.fetch_one(query, (product_id,))
    
    def add_product(self, name, description, unit_price, supplier_id):
        query = """
        INSERT INTO Products (ProductName, Description, UnitPrice, SupplierID) 
        VALUES (%s, %s, %s, %s)
        """
        params = (name, description, unit_price, supplier_id)
        return self.db.execute_query(query, params)
    
    def update_product(self, product_id, name, description, unit_price, supplier_id):
        query = """
        UPDATE Products 
        SET ProductName = %s, Description = %s, UnitPrice = %s, SupplierID = %s 
        WHERE ProductID = %s
        """
        params = (name, description, unit_price, supplier_id, product_id)
        return self.db.execute_query(query, params)
    
    def delete_product(self, product_id):
        query = "DELETE FROM Products WHERE ProductID = %s"
        return self.db.execute_query(query, (product_id,))

class Supplier:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_suppliers(self):
        query = "SELECT * FROM Suppliers"
        return self.db.fetch_all(query)
    
    def get_supplier_by_id(self, supplier_id):
        query = "SELECT * FROM Suppliers WHERE SupplierID = %s"
        return self.db.fetch_one(query, (supplier_id,))
    
    def add_supplier(self, name, address, phone_number):
        query = """
        INSERT INTO Suppliers (SupplierName, Address, PhoneNumber) 
        VALUES (%s, %s, %s)
        """
        params = (name, address, phone_number)
        return self.db.execute_query(query, params)
    
    def update_supplier(self, supplier_id, name, address, phone_number):
        query = """
        UPDATE Suppliers 
        SET SupplierName = %s, Address = %s, PhoneNumber = %s 
        WHERE SupplierID = %s
        """
        params = (name, address, phone_number, supplier_id)
        return self.db.execute_query(query, params)
    
    def delete_supplier(self, supplier_id):
        query = "DELETE FROM Suppliers WHERE SupplierID = %s"
        return self.db.execute_query(query, (supplier_id,))
    
    def get_supplier_delivery_history(self):
        query = "SELECT * FROM SupplierDeliveryHistory"
        return self.db.fetch_all(query)

class Warehouse:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_warehouses(self):
        query = "SELECT * FROM Warehouses"
        return self.db.fetch_all(query)
    
    def get_warehouse_by_id(self, warehouse_id):
        query = "SELECT * FROM Warehouses WHERE WarehouseID = %s"
        return self.db.fetch_one(query, (warehouse_id,))
    
    def add_warehouse(self, name, address):
        query = "INSERT INTO Warehouses (WarehouseName, Address) VALUES (%s, %s)"
        params = (name, address)
        return self.db.execute_query(query, params)
    
    def update_warehouse(self, warehouse_id, name, address):
        query = """
        UPDATE Warehouses 
        SET WarehouseName = %s, Address = %s 
        WHERE WarehouseID = %s
        """
        params = (name, address, warehouse_id)
        return self.db.execute_query(query, params)
    
    def delete_warehouse(self, warehouse_id):
        query = "DELETE FROM Warehouses WHERE WarehouseID = %s"
        return self.db.execute_query(query, (warehouse_id,))

class Inventory:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_inventory_levels(self):
        query = """
        SELECT p.ProductName, w.WarehouseName, i.Quantity, i.MinStockLevel, i.ProductID, i.WarehouseID
        FROM Inventory i
        JOIN Products p ON i.ProductID = p.ProductID
        JOIN Warehouses w ON i.WarehouseID = w.WarehouseID
        """
        return self.db.fetch_all(query)
    
    def update_inventory(self, product_id, warehouse_id, quantity, min_stock_level):
        query = """
        INSERT INTO Inventory (ProductID, WarehouseID, Quantity, MinStockLevel)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE Quantity = %s, MinStockLevel = %s
        """
        params = (product_id, warehouse_id, quantity, min_stock_level, quantity, min_stock_level)
        return self.db.execute_query(query, params)
    
    def check_low_stock(self):
        return self.db.call_procedure("CheckLowStock")
    
    def calculate_total_stock_value(self):
        result = self.db.call_procedure("CalculateTotalStockValue")
        return result[0]['TotalValue'] if result else 0

class StockEntry:
    def __init__(self, db_connection):
        self.db = db_connection
    

    def get_all_entries(self):
        query = """
        SELECT se.*, p.ProductName, w.WarehouseName 
        FROM StockEntries se
        JOIN Products p ON se.ProductID = p.ProductID
        JOIN Warehouses w ON se.WarehouseID = w.WarehouseID
        """
        return self.db.fetch_all(query)
    
    def add_stock_entry(self, product_id, warehouse_id, quantity, entry_date=None):
        if entry_date is None:
            entry_date = datetime.now().strftime('%Y-%m-%d')
        query = """
        INSERT INTO StockEntries (ProductID, WarehouseID, Quantity, EntryDate) 
        VALUES (%s, %s, %s, %s)
        """
        params = (product_id, warehouse_id, quantity, entry_date)
        return self.db.execute_query(query, params)

class InventoryHistory:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_history(self):
        query = """
        SELECT ih.*, p.ProductName, w.WarehouseName 
        FROM InventoryHistory ih
        JOIN Products p ON ih.ProductID = p.ProductID
        JOIN Warehouses w ON ih.WarehouseID = w.WarehouseID
        ORDER BY ih.TransactionDate DESC
        """
        return self.db.fetch_all(query)
    
    def add_history_entry(self, product_id, warehouse_id, quantity, transaction_type, transaction_date=None):
        if transaction_date is None:
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = """
        INSERT INTO InventoryHistory (ProductID, WarehouseID, Quantity, TransactionDate, TransactionType) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (product_id, warehouse_id, quantity, transaction_date, transaction_type)
        return self.db.execute_query(query, params)
    
    def get_history_by_date_range(self, start_date, end_date):
        query = """
        SELECT ih.*, p.ProductName, w.WarehouseName 
        FROM InventoryHistory ih
        JOIN Products p ON ih.ProductID = p.ProductID
        JOIN Warehouses w ON ih.WarehouseID = w.WarehouseID
        WHERE DATE(ih.TransactionDate) BETWEEN %s AND %s
        ORDER BY ih.TransactionDate DESC
        """
        params = (start_date, end_date)
        return self.db.fetch_all(query, params)