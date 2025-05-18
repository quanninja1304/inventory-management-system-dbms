-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2025 at 11:05 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

CREATE DATABASE inventory_db;
USE inventory_db;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_db`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddStockEntry` (IN `p_product_id` INT, IN `p_warehouse_id` INT, IN `p_quantity` INT, IN `p_date` DATE)   BEGIN
    -- Thêm vào StockEntries
    INSERT INTO StockEntries (ProductID, WarehouseID, Quantity, EntryDate)
    VALUES (p_product_id, p_warehouse_id, p_quantity, p_date);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CalculateTotalStockValue` ()   BEGIN
    SELECT SUM(i.Quantity * p.UnitPrice) AS TotalValue
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CheckLowStock` ()   BEGIN
    SELECT w.WarehouseName, p.ProductName, i.Quantity, i.MinStockLevel
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Warehouses w ON i.WarehouseID = w.WarehouseID
    WHERE i.Quantity < i.MinStockLevel;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetInventoryBySupplier` (IN `supplier_id` INT)   BEGIN
    SELECT s.SupplierName, p.ProductName, SUM(i.Quantity) as TotalQuantity,
           SUM(i.Quantity * p.UnitPrice) as TotalValue
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Suppliers s ON p.SupplierID = s.SupplierID
    WHERE s.SupplierID = supplier_id
    GROUP BY s.SupplierName, p.ProductName;
END$$

--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateAverageDeliveryTime` (`supplier_id` INT) RETURNS DECIMAL(10,2) DETERMINISTIC BEGIN
    DECLARE avg_days DECIMAL(10,2);
    
    -- Giả định: Thời gian giao hàng được tính từ dữ liệu trong StockEntries
    -- Trong thực tế, bạn có thể cần bảng Orders để theo dõi ngày đặt hàng
    -- Đây là ví dụ đơn giản dựa trên dữ liệu hiện có
    
    SELECT AVG(DATEDIFF(se.EntryDate, DATE_SUB(se.EntryDate, INTERVAL 7 DAY))) INTO avg_days
    FROM StockEntries se
    JOIN Products p ON se.ProductID = p.ProductID
    WHERE p.SupplierID = supplier_id;
    
    -- Xử lý khi không có dữ liệu
    IF avg_days IS NULL THEN
        RETURN 0;
    END IF;
    
    RETURN avg_days;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateProductInventoryValue` (`product_id` INT) RETURNS DECIMAL(10,2) DETERMINISTIC BEGIN
    DECLARE total_value DECIMAL(10,2);
    
    SELECT SUM(i.Quantity * p.UnitPrice) INTO total_value
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID
    WHERE i.ProductID = product_id;
    
    -- Xử lý khi không có dữ liệu
    IF total_value IS NULL THEN
        RETURN 0;
    END IF;
    
    RETURN total_value;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateStockTurnover` (`product_id` INT, `warehouse_id` INT, `start_date` DATE, `end_date` DATE) RETURNS DECIMAL(10,2) DETERMINISTIC BEGIN
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
    
    -- Tồn kho trung bình (giả định đơn giản là tồn kho hiện tại)
    SELECT AVG(Quantity) INTO avg_inventory
    FROM Inventory
    WHERE ProductID = product_id
    AND WarehouseID = warehouse_id;
    
    -- Xử lý trường hợp chia cho 0
    IF avg_inventory <= 0 OR avg_inventory IS NULL THEN
        RETURN 0;
    END IF;
    
    -- Nếu không có bán hàng
    IF sold_quantity IS NULL THEN
        SET sold_quantity = 0;
    END IF;
    
    -- Tính tỷ lệ
    SET turnover_rate = sold_quantity / avg_inventory;
    
    RETURN turnover_rate;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `InventoryID` int(11) NOT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT 0,
  `MinStockLevel` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`InventoryID`, `ProductID`, `WarehouseID`, `Quantity`, `MinStockLevel`) VALUES
(1, 1, 1, 40, 10),
(2, 1, 2, 20, 10),
(3, 2, 1, 80, 10),
(4, 3, 2, 60, 10),
(5, 4, 3, 50, 10),
(6, 5, 4, 0, 10),
(7, 6, 1, 0, 10),
(8, 7, 2, 0, 10),
(9, 8, 3, 0, 10),
(10, 9, 4, 0, 10),
(11, 10, 5, 0, 10);

-- --------------------------------------------------------

--
-- Table structure for table `inventoryhistory`
--

CREATE TABLE `inventoryhistory` (
  `HistoryID` int(11) NOT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `Quantity` int(11) NOT NULL,
  `TransactionDate` datetime NOT NULL,
  `TransactionType` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventoryhistory`
--

INSERT INTO `inventoryhistory` (`HistoryID`, `ProductID`, `WarehouseID`, `Quantity`, `TransactionDate`, `TransactionType`) VALUES
(1, 1, 1, 50, '2025-05-01 00:00:00', 'StockEntry'),
(2, 1, 2, 20, '2025-05-02 00:00:00', 'StockEntry'),
(3, 2, 1, 100, '2025-05-03 00:00:00', 'StockEntry'),
(4, 3, 2, 75, '2025-05-04 00:00:00', 'StockEntry'),
(5, 4, 3, 50, '2025-05-05 00:00:00', 'StockEntry'),
(6, 1, 1, -10, '2025-05-06 15:00:00', 'Sale'),
(7, 2, 1, -20, '2025-05-07 16:00:00', 'Sale'),
(8, 3, 2, -15, '2025-05-08 17:00:00', 'Adjustment');

--
-- Triggers `inventoryhistory`
--
DELIMITER $$
CREATE TRIGGER `after_inventoryhistory_insert` AFTER INSERT ON `inventoryhistory` FOR EACH ROW BEGIN
    INSERT INTO Inventory (ProductID, WarehouseID, Quantity)
    VALUES (NEW.ProductID, NEW.WarehouseID, NEW.Quantity)
    ON DUPLICATE KEY UPDATE Quantity = Quantity + NEW.Quantity;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `Description` text DEFAULT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  `SupplierID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `ProductName`, `Description`, `UnitPrice`, `SupplierID`) VALUES
(1, 'Product 1', 'Description 1', 10.99, 1),
(2, 'Product 2', 'Description 2', 20.49, 2),
(3, 'Product 3', 'Description 3', 15.00, 3),
(4, 'Product 4', 'Description 4', 25.99, 4),
(5, 'Product 5', 'Description 5', 30.00, 5),
(6, 'Product 6', 'Description 6', 12.50, 1),
(7, 'Product 7', 'Description 7', 18.75, 2),
(8, 'Product 8', 'Description 8', 22.00, 3),
(9, 'Product 9', 'Description 9', 28.50, 4),
(10, 'Product 10', 'Description 10', 35.00, 5);

-- --------------------------------------------------------

--
-- Table structure for table `stockentries`
--

CREATE TABLE `stockentries` (
  `EntryID` int(11) NOT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `WarehouseID` int(11) DEFAULT NULL,
  `Quantity` int(11) NOT NULL,
  `EntryDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stockentries`
--

INSERT INTO `stockentries` (`EntryID`, `ProductID`, `WarehouseID`, `Quantity`, `EntryDate`) VALUES
(1, 1, 1, 50, '2025-05-01'),
(2, 1, 2, 20, '2025-05-02'),
(3, 2, 1, 100, '2025-05-03'),
(4, 3, 2, 75, '2025-05-04'),
(5, 4, 3, 50, '2025-05-05');

--
-- Triggers `stockentries`
--
DELIMITER $$
CREATE TRIGGER `after_stockentry_insert` AFTER INSERT ON `stockentries` FOR EACH ROW BEGIN
    INSERT INTO InventoryHistory (ProductID, WarehouseID, Quantity, TransactionDate, TransactionType)
    VALUES (NEW.ProductID, NEW.WarehouseID, NEW.Quantity, NEW.EntryDate, 'StockEntry');
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `stockperwarehouse`
-- (See below for the actual view)
--
CREATE TABLE `stockperwarehouse` (
`WarehouseID` int(11)
,`WarehouseName` varchar(100)
,`ProductID` int(11)
,`ProductName` varchar(100)
,`Quantity` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `supplierdeliveryhistory`
-- (See below for the actual view)
--
CREATE TABLE `supplierdeliveryhistory` (
`SupplierID` int(11)
,`SupplierName` varchar(100)
,`ProductID` int(11)
,`ProductName` varchar(100)
,`Quantity` int(11)
,`EntryDate` date
);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `SupplierID` int(11) NOT NULL,
  `SupplierName` varchar(100) NOT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`SupplierID`, `SupplierName`, `Address`, `PhoneNumber`) VALUES
(1, 'Supplier A', '123 Main St', '555-1234'),
(2, 'Supplier B', '456 Elm St', '555-5678'),
(3, 'Supplier C', '789 Oak St', '555-9012'),
(4, 'Supplier D', '321 Pine St', '555-3456'),
(5, 'Supplier E', '654 Maple St', '555-7890');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `role` enum('admin','employee','user') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'admin1', '0192023a7bbd73250516f069df18b500', 'admin', '2025-05-18 08:52:11'),
(2, 'employee1', '0314ee502c6f4e284128ad14e84e37d5', 'employee', '2025-05-18 08:52:11'),
(3, 'user1', '6ad14ba9986e3615423dfca256d04e3f', 'user', '2025-05-18 08:52:11');

-- --------------------------------------------------------

--
-- Stand-in structure for view `warehouseinventoryview`
-- (See below for the actual view)
--
CREATE TABLE `warehouseinventoryview` (
`ProductName` varchar(100)
,`WarehouseName` varchar(100)
,`Quantity` int(11)
,`MinStockLevel` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `warehouses`
--

CREATE TABLE `warehouses` (
  `WarehouseID` int(11) NOT NULL,
  `WarehouseName` varchar(100) NOT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehouses`
--

INSERT INTO `warehouses` (`WarehouseID`, `WarehouseName`, `Address`) VALUES
(1, 'Warehouse A', '100 Warehouse Rd'),
(2, 'Warehouse B', '200 Storage Ln'),
(3, 'Warehouse C', '300 Logistics Ave'),
(4, 'Warehouse D', '400 Distribution St'),
(5, 'Warehouse E', '500 Supply Chain Blvd');

-- --------------------------------------------------------

--
-- Structure for view `stockperwarehouse`
--
DROP TABLE IF EXISTS `stockperwarehouse`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `stockperwarehouse`  AS SELECT `w`.`WarehouseID` AS `WarehouseID`, `w`.`WarehouseName` AS `WarehouseName`, `p`.`ProductID` AS `ProductID`, `p`.`ProductName` AS `ProductName`, `i`.`Quantity` AS `Quantity` FROM ((`warehouses` `w` join `inventory` `i` on(`w`.`WarehouseID` = `i`.`WarehouseID`)) join `products` `p` on(`i`.`ProductID` = `p`.`ProductID`)) ;

-- --------------------------------------------------------

--
-- Structure for view `supplierdeliveryhistory`
--
DROP TABLE IF EXISTS `supplierdeliveryhistory`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `supplierdeliveryhistory`  AS SELECT `s`.`SupplierID` AS `SupplierID`, `s`.`SupplierName` AS `SupplierName`, `p`.`ProductID` AS `ProductID`, `p`.`ProductName` AS `ProductName`, `se`.`Quantity` AS `Quantity`, `se`.`EntryDate` AS `EntryDate` FROM ((`suppliers` `s` join `products` `p` on(`s`.`SupplierID` = `p`.`SupplierID`)) join `stockentries` `se` on(`p`.`ProductID` = `se`.`ProductID`)) ;

-- --------------------------------------------------------

--
-- Structure for view `warehouseinventoryview`
--
DROP TABLE IF EXISTS `warehouseinventoryview`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `warehouseinventoryview`  AS SELECT `p`.`ProductName` AS `ProductName`, `w`.`WarehouseName` AS `WarehouseName`, `i`.`Quantity` AS `Quantity`, `i`.`MinStockLevel` AS `MinStockLevel` FROM ((`inventory` `i` join `products` `p` on(`i`.`ProductID` = `p`.`ProductID`)) join `warehouses` `w` on(`i`.`WarehouseID` = `w`.`WarehouseID`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`InventoryID`),
  ADD UNIQUE KEY `ProductID` (`ProductID`,`WarehouseID`),
  ADD KEY `idx_warehouse_id` (`WarehouseID`);

--
-- Indexes for table `inventoryhistory`
--
ALTER TABLE `inventoryhistory`
  ADD PRIMARY KEY (`HistoryID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `idx_inventoryhistory_warehouse` (`WarehouseID`),
  ADD KEY `idx_transaction_type` (`TransactionType`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `idx_product_name` (`ProductName`),
  ADD KEY `idx_supplier_product` (`SupplierID`);

--
-- Indexes for table `stockentries`
--
ALTER TABLE `stockentries`
  ADD PRIMARY KEY (`EntryID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `WarehouseID` (`WarehouseID`),
  ADD KEY `idx_entry_date` (`EntryDate`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `warehouses`
--
ALTER TABLE `warehouses`
  ADD PRIMARY KEY (`WarehouseID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `InventoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `inventoryhistory`
--
ALTER TABLE `inventoryhistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `stockentries`
--
ALTER TABLE `stockentries`
  MODIFY `EntryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `SupplierID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `warehouses`
--
ALTER TABLE `warehouses`
  MODIFY `WarehouseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`),
  ADD CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouses` (`WarehouseID`);

--
-- Constraints for table `inventoryhistory`
--
ALTER TABLE `inventoryhistory`
  ADD CONSTRAINT `inventoryhistory_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`),
  ADD CONSTRAINT `inventoryhistory_ibfk_2` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouses` (`WarehouseID`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `suppliers` (`SupplierID`);

--
-- Constraints for table `stockentries`
--
ALTER TABLE `stockentries`
  ADD CONSTRAINT `stockentries_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`),
  ADD CONSTRAINT `stockentries_ibfk_2` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouses` (`WarehouseID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
