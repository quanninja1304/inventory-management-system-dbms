-- Add Users table to manage system access
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,  -- Will store hashed passwords
    FullName VARCHAR(100),
    Email VARCHAR(100),
    Role ENUM('admin', 'inventory_manager', 'warehouse_staff') NOT NULL,
    LastLogin DATETIME,
    Active BOOLEAN DEFAULT TRUE,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
INSERT INTO Users (Username, Password, FullName, Email, Role, Active) 
VALUES ('admin', '$2b$12$8NKfUCINTFGjoqoWH3HMp.yW2pxXF.LZzZevYEQIZtaSNUQF4vXmq', 'System Administrator', 'admin@example.com', 'admin', TRUE);

-- Insert default inventory manager (password: manager123)
INSERT INTO Users (Username, Password, FullName, Email, Role, Active) 
VALUES ('manager', '$2b$12$LwGEWPXhj9wOhRRJtjxSCeZjHwoPnOKNfGLm.1H3OebCuo7qujKr6', 'Inventory Manager', 'manager@example.com', 'inventory_manager', TRUE);

-- Insert default warehouse staff (password: staff123)
INSERT INTO Users (Username, Password, FullName, Email, Role, Active) 
VALUES ('staff', '$2b$12$fIl7es4oI5K0QQN.hYY/mOaRVGmvBP9Z3UUYHTnEDFKB0ErfnNkO.', 'Warehouse Staff', 'staff@example.com', 'warehouse_staff', TRUE);

-- Create AuditLog table if it doesn't exist
CREATE TABLE IF NOT EXISTS AuditLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Action VARCHAR(100) NOT NULL,
    Details TEXT,
    IPAddress VARCHAR(45),
    Timestamp DATETIME NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_audit_username ON AuditLog(Username);
CREATE INDEX IF NOT EXISTS idx_audit_action ON AuditLog(Action);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON AuditLog(Timestamp);