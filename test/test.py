import pandas as pd
import mysql.connector
import numpy as np

# Replace with your actual database credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'username',
    'password': 'your_password',
    'database': 'inventory_db'
}

# Connect to the database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

def import_csv_to_mysql(csv_file, table_name, columns):
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        
        # Make sure we have only the columns we need
        df = df[columns].copy()
        
        # Use INSERT IGNORE to skip duplicates
        placeholders = ','.join(['%s'] * len(columns))
        query = f"INSERT IGNORE INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
        
        # Convert DataFrame to list of Python tuples with explicit type conversion
        data = []
        for _, row in df.iterrows():
            # Convert each value to the appropriate Python type
            row_data = []
            for col in columns:
                val = row[col]
                # Handle different numpy data types
                if isinstance(val, (np.integer, np.int64, np.int32)):
                    val = int(val)
                elif isinstance(val, (np.float64, np.float32)):
                    val = float(val)
                elif isinstance(val, (np.bool_)):
                    val = bool(val)
                elif pd.isna(val):
                    val = None
                elif isinstance(val, str) and val.strip() == '':
                    val = None
                row_data.append(val)
            data.append(tuple(row_data))
        
        # Execute the query
        cursor.executemany(query, data)
        conn.commit()
        
        # Report results
        print(f"Processed {len(df)} rows for `{table_name}`")
        print(f"Inserted {cursor.rowcount} new rows, {len(df) - cursor.rowcount} skipped (already exist)")
        
    except Exception as e:
        conn.rollback()
        print(f"Error importing {csv_file} to {table_name}: {e}")
        raise

# Import tables in order based on foreign key dependencies
try:
    # Import suppliers first (parent table)
    import_csv_to_mysql('test/suppliers.csv', 'suppliers', 
                        ['SupplierID', 'SupplierName', 'Address', 'PhoneNumber'])
    
    # Then products (depends on suppliers)
    import_csv_to_mysql('test/products.csv', 'products', 
                        ['ProductID', 'ProductName', 'Description', 'UnitPrice', 'SupplierID'])
    
    # Warehouses (independent table)
    import_csv_to_mysql('test/warehouses.csv', 'warehouses', 
                        ['WarehouseID', 'WarehouseName', 'Address'])
    
    # Then inventory (depends on products and warehouses)
    import_csv_to_mysql('test/inventory.csv', 'inventory', 
                        ['InventoryID', 'ProductID', 'WarehouseID', 'Quantity', 'MinStockLevel'])
    
    # Then stock entries (depends on products and warehouses)
    import_csv_to_mysql('test/stockentries.csv', 'stockentries', 
                        ['EntryID', 'ProductID', 'WarehouseID', 'Quantity', 'EntryDate'])
    
    # Then inventory history (depends on products and warehouses)
    import_csv_to_mysql('test/inventoryhistory.csv', 'inventoryhistory', 
                        ['HistoryID', 'ProductID', 'WarehouseID', 'Quantity', 'TransactionDate', 'TransactionType'])
    
    print("All data imported successfully!")
    
except Exception as e:
    print(f"Import process failed: {e}")
    
finally:
    cursor.close()
    conn.close()