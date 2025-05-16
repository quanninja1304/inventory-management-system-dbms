-- Create Database
CREATE DATABASE inventory_db;
USE inventory_db;

-- Tạo bảng Suppliers
CREATE TABLE Suppliers (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20)
);

-- Create Products Table
CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Description TEXT,
    UnitPrice DECIMAL(10,2) NOT NULL,
    SupplierID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- Create Warehouses Table
CREATE TABLE Warehouses (
    WarehouseID INT AUTO_INCREMENT PRIMARY KEY,
    WarehouseName VARCHAR(100) NOT NULL,
    Address VARCHAR(255)
);

-- Create an Inventory table to track current stock levels
CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    Quantity INT DEFAULT 0,
    MinStockLevel INT DEFAULT 0,
    UNIQUE KEY (ProductID, WarehouseID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);

-- Create a StockEntries table to record stock-in transactions
CREATE TABLE StockEntries (
    EntryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    Quantity INT NOT NULL,
    EntryDate DATE NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);

-- Create an InventoryHistory table to track inventory transaction history
CREATE TABLE InventoryHistory (
    HistoryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    Quantity INT NOT NULL,
    TransactionDate DATETIME NOT NULL,
    TransactionType VARCHAR(50),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);

-- Create indexes to speed up search queries
CREATE INDEX idx_product_name ON Products (ProductName);
CREATE INDEX idx_warehouse_id ON Inventory (WarehouseID);
CREATE INDEX idx_inventoryhistory_warehouse ON InventoryHistory (WarehouseID);

-- Create a view to summarize stock levels by warehouse
CREATE VIEW StockPerWarehouse AS
SELECT w.WarehouseID, w.WarehouseName, p.ProductID, p.ProductName, i.Quantity
FROM Warehouses w
JOIN Inventory i ON w.WarehouseID = i.WarehouseID
JOIN Products p ON i.ProductID = p.ProductID;

-- Create a view to summarize the delivery history of each supplier
CREATE VIEW SupplierDeliveryHistory AS
SELECT s.SupplierID, s.SupplierName, p.ProductID, p.ProductName, se.Quantity, se.EntryDate
FROM Suppliers s
JOIN Products p ON s.SupplierID = p.SupplierID
JOIN StockEntries se ON p.ProductID = se.ProductID;

-- Create a stored procedure to check for low stock
DELIMITER //
CREATE PROCEDURE CheckLowStock()
BEGIN
    SELECT w.WarehouseName, p.ProductName, i.Quantity, i.MinStockLevel
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Warehouses w ON i.WarehouseID = w.WarehouseID
    WHERE i.Quantity < i.MinStockLevel;
END //
DELIMITER ;

-- "Create a stored procedure to calculate the total inventory value
DELIMITER //
CREATE PROCEDURE CalculateTotalStockValue()
BEGIN
    SELECT SUM(i.Quantity * p.UnitPrice) AS TotalValue
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID;
END //
DELIMITER ;

-- Create a trigger to record history when new stock is added
DELIMITER //
CREATE TRIGGER after_stockentry_insert
AFTER INSERT ON StockEntries
FOR EACH ROW
BEGIN
    INSERT INTO InventoryHistory (ProductID, WarehouseID, Quantity, TransactionDate, TransactionType)
    VALUES (NEW.ProductID, NEW.WarehouseID, NEW.Quantity, NEW.EntryDate, 'StockEntry');
END //
DELIMITER ;

-- Create a trigger to update the Inventory table 
-- when a new transaction is recorded in the InventoryHistory table
DELIMITER //
CREATE TRIGGER after_inventoryhistory_insert
AFTER INSERT ON InventoryHistory
FOR EACH ROW
BEGIN
    INSERT INTO Inventory (ProductID, WarehouseID, Quantity)
    VALUES (NEW.ProductID, NEW.WarehouseID, NEW.Quantity)
    ON DUPLICATE KEY UPDATE Quantity = Quantity + NEW.Quantity;
END //
DELIMITER ;

-- Insert sample data for the Suppliers table
INSERT INTO Suppliers (SupplierName, Address, PhoneNumber) VALUES
('Supplier A', '123 Main St', '555-1234'),
('Supplier B', '456 Elm St', '555-5678'),
('Supplier C', '789 Oak St', '555-9012'),
('Supplier D', '321 Pine St', '555-3456'),
('Supplier E', '654 Maple St', '555-7890');

-- Insert sample data for the Products table
INSERT INTO Products (ProductName, Description, UnitPrice, SupplierID) VALUES
('Product 1', 'Description 1', 10.99, 1),
('Product 2', 'Description 2', 20.49, 2),
('Product 3', 'Description 3', 15.00, 3),
('Product 4', 'Description 4', 25.99, 4),
('Product 5', 'Description 5', 30.00, 5),
('Product 6', 'Description 6', 12.50, 1),
('Product 7', 'Description 7', 18.75, 2),
('Product 8', 'Description 8', 22.00, 3),
('Product 9', 'Description 9', 28.50, 4),
('Product 10', 'Description 10', 35.00, 5);

-- Insert sample data for the Warehouses table
INSERT INTO Warehouses (WarehouseName, Address) VALUES
('Warehouse A', '100 Warehouse Rd'),
('Warehouse B', '200 Storage Ln'),
('Warehouse C', '300 Logistics Ave'),
('Warehouse D', '400 Distribution St'),
('Warehouse E', '500 Supply Chain Blvd');

-- Insert sample data for the Inventory table (initialize beginning stock)
INSERT INTO Inventory (ProductID, WarehouseID, Quantity, MinStockLevel) VALUES
(1, 1, 0, 10),
(1, 2, 0, 10),
(2, 1, 0, 10),
(3, 2, 0, 10),
(4, 3, 0, 10),
(5, 4, 0, 10),
(6, 1, 0, 10),
(7, 2, 0, 10),
(8, 3, 0, 10),
(9, 4, 0, 10),
(10, 5, 0, 10);

-- Insert sample data for the StockEntries table
INSERT INTO StockEntries (ProductID, WarehouseID, Quantity, EntryDate) VALUES
(1, 1, 50, '2025-05-01'),
(1, 2, 20, '2025-05-02'),
(2, 1, 100, '2025-05-03'),
(3, 2, 75, '2025-05-04'),
(4, 3, 50, '2025-05-05');

-- Insert sample data for the InventoryHistory table (e.g., for stock-out or adjustment transactions)
INSERT INTO InventoryHistory (ProductID, WarehouseID, Quantity, TransactionDate, TransactionType) VALUES
(1, 1, -10, '2025-05-06 15:00:00', 'Sale'),
(2, 1, -20, '2025-05-07 16:00:00', 'Sale'),
(3, 2, -15, '2025-05-08 17:00:00', 'Adjustment');


-- User Defined Functions
USE inventory_db;

-- 1. Function to calculate Stock Turnover Rate
-- Stock Turnover = Quantity Sold / Average Inventory
DELIMITER //
CREATE FUNCTION CalculateStockTurnover(product_id INT, warehouse_id INT, start_date DATE, end_date DATE) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE sold_quantity INT;
    DECLARE avg_inventory DECIMAL(10,2);
    DECLARE turnover_rate DECIMAL(10,2);
    
    -- Tổng số lượng bán ra trong khoảng thời gian
    SELECT ABS(SUM(Quantity)) INTO sold_quantity
    FROM InventoryHistory
    WHERE ProductID = product_id 
    AND WarehouseID = warehouse_id
    AND TransactionDate BETWEEN start_date AND end_date
    AND TransactionType = 'Sale';
    
    -- Average Inventory (simplified assumption: current inventory)
    SELECT AVG(Quantity) INTO avg_inventory
    FROM Inventory
    WHERE ProductID = product_id
    AND WarehouseID = warehouse_id;
    
	-- Handle division by zero case
    IF avg_inventory <= 0 OR avg_inventory IS NULL THEN
        RETURN 0;
    END IF;
    
    -- If there are no sales
    IF sold_quantity IS NULL THEN
        SET sold_quantity = 0;
    END IF;
    
    -- Calculate the rate
    SET turnover_rate = sold_quantity / avg_inventory;
    
    RETURN turnover_rate;
END //
DELIMITER ;

-- 2. Function to calculate the average delivery time of a supplier
DELIMITER //
CREATE FUNCTION CalculateAverageDeliveryTime(supplier_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE avg_days DECIMAL(10,2);
    
	-- Assumption: Delivery time is calculated based on data in the StockEntries table
	-- In practice, you may need an Orders table to track the order date
	-- This is a simplified example based on available data
 
    SELECT AVG(DATEDIFF(se.EntryDate, DATE_SUB(se.EntryDate, INTERVAL 7 DAY))) INTO avg_days
    FROM StockEntries se
    JOIN Products p ON se.ProductID = p.ProductID
    WHERE p.SupplierID = supplier_id;
    
    -- Handle cases with no data
    IF avg_days IS NULL THEN
        RETURN 0;
    END IF;
    
    RETURN avg_days;
END //
DELIMITER ;

-- 3. Function to calculate the inventory value of a product
DELIMITER //
CREATE FUNCTION CalculateProductInventoryValue(product_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_value DECIMAL(10,2);
    
    SELECT SUM(i.Quantity * p.UnitPrice) INTO total_value
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    WHERE i.ProductID = product_id;
    
    -- Handle cases with no data
    IF total_value IS NULL THEN
        RETURN 0;
    END IF;
    
    RETURN total_value;
END //
DELIMITER ;

-- Create additional indexes to optimize query performance
CREATE INDEX idx_supplier_product ON Products(SupplierID);
CREATE INDEX idx_transaction_type ON InventoryHistory(TransactionType);
CREATE INDEX idx_entry_date ON StockEntries(EntryDate);

-- Create an additional stored procedure for safe stock-in operations
DELIMITER //
CREATE PROCEDURE AddStockEntry(IN p_product_id INT, IN p_warehouse_id INT, IN p_quantity INT, IN p_date DATE)
BEGIN
    -- Insert into StockEntries
    INSERT INTO StockEntries (ProductID, WarehouseID, Quantity, EntryDate)
    VALUES (p_product_id, p_warehouse_id, p_quantity, p_date);
END //
DELIMITER ;

-- Create a stored procedure to generate an inventory report by supplier
DELIMITER //
CREATE PROCEDURE GetInventoryBySupplier(IN supplier_id INT)
BEGIN
    SELECT s.SupplierName, p.ProductName, SUM(i.Quantity) as TotalQuantity,
           SUM(i.Quantity * p.UnitPrice) as TotalValue
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Suppliers s ON p.SupplierID = s.SupplierID
    WHERE s.SupplierID = supplier_id
    GROUP BY s.SupplierName, p.ProductName;
END //
DELIMITER ;

-- Create an additional view for warehouse staff to view the data
CREATE VIEW WarehouseInventoryView AS
SELECT p.ProductName, w.WarehouseName, i.Quantity, i.MinStockLevel
FROM Inventory i
JOIN Products p ON i.ProductID = p.ProductID
JOIN Warehouses w ON i.WarehouseID = w.WarehouseID;


-- Database Security and Administration (Requires root or administrative privileges)
-- NOTE: You need MySQL administrative privileges to run this script

-- 1. Create users and roles
-- Note: If you encounter password policy errors, you may need to set a more complex password
CREATE USER IF NOT EXISTS 'inventory_manager'@'localhost' IDENTIFIED BY 'Inv_Manager_Pass123!';
CREATE USER IF NOT EXISTS 'inventory_admin'@'localhost' IDENTIFIED BY 'Inv_Admin_Pass123!';
CREATE USER IF NOT EXISTS 'warehouse_staff'@'localhost' IDENTIFIED BY 'Warehouse_Staff_Pass123!';

-- 2. Grant permissions to the Inventory Manager (can view and update inventory data)
GRANT SELECT, INSERT, UPDATE ON inventory_db.Inventory TO 'inventory_manager'@'localhost';
GRANT SELECT, INSERT ON inventory_db.InventoryHistory TO 'inventory_manager'@'localhost';
GRANT SELECT ON inventory_db.Products TO 'inventory_manager'@'localhost';
GRANT SELECT ON inventory_db.Warehouses TO 'inventory_manager'@'localhost';
GRANT SELECT ON inventory_db.Suppliers TO 'inventory_manager'@'localhost';
GRANT SELECT ON inventory_db.StockEntries TO 'inventory_manager'@'localhost';
GRANT EXECUTE ON PROCEDURE inventory_db.CheckLowStock TO 'inventory_manager'@'localhost';
GRANT EXECUTE ON PROCEDURE inventory_db.CalculateTotalStockValue TO 'inventory_manager'@'localhost';
GRANT EXECUTE ON FUNCTION inventory_db.CalculateStockTurnover TO 'inventory_manager'@'localhost';
GRANT EXECUTE ON FUNCTION inventory_db.CalculateProductInventoryValue TO 'inventory_manager'@'localhost';
GRANT EXECUTE ON PROCEDURE inventory_db.GetInventoryBySupplier TO 'inventory_manager'@'localhost';

-- 3. Grant permissions to Warehouse Staff (can only view and update StockEntries)
GRANT SELECT ON inventory_db.Products TO 'warehouse_staff'@'localhost';
GRANT SELECT ON inventory_db.Warehouses TO 'warehouse_staff'@'localhost';
GRANT SELECT, INSERT ON inventory_db.StockEntries TO 'warehouse_staff'@'localhost';
GRANT SELECT ON inventory_db.Inventory TO 'warehouse_staff'@'localhost';
GRANT SELECT ON inventory_db.WarehouseInventoryView TO 'warehouse_staff'@'localhost';
GRANT EXECUTE ON PROCEDURE inventory_db.AddStockEntry TO 'warehouse_staff'@'localhost';

-- 4. Grant permissions to Admin (full access to the database)
GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_admin'@'localhost';

-- 5. Apply the permissions
FLUSH PRIVILEGES;

-- Note on backup (to be executed from the command line):
/*
To back up the database:
mysqldump -u root -p inventory_db > /path/to/backup/inventory_db_$(date +%Y%m%d).sql

To restore the database:
mysql -u root -p inventory_db < /path/to/backup/inventory_db_backup.sql
*/
