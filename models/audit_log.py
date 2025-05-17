from datetime import datetime

class AuditLog:
    def __init__(self, db_connection=None):
        self.db = db_connection
    
    def log_action(self, username, action, details="", ip_address="localhost"):
        """Log a user action to the audit log"""
        if not self.db:
            return
            
        try:
            # Check if the AuditLog table exists
            check_table_query = """
            SELECT COUNT(*) AS count
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = 'AuditLog'
            """
            result = self.db.fetch_one(check_table_query)
            
            # If table doesn't exist, create it
            if not result or result['count'] == 0:
                create_table_query = """
                CREATE TABLE AuditLog (
                    LogID INT AUTO_INCREMENT PRIMARY KEY,
                    Username VARCHAR(50) NOT NULL,
                    Action VARCHAR(100) NOT NULL,
                    Details TEXT,
                    IPAddress VARCHAR(45),
                    Timestamp DATETIME NOT NULL
                );
                CREATE INDEX idx_audit_username ON AuditLog(Username);
                CREATE INDEX idx_audit_action ON AuditLog(Action);
                CREATE INDEX idx_audit_timestamp ON AuditLog(Timestamp);
                """
                self.db.execute_query(create_table_query)
            
            # Insert the log entry
            query = """
            INSERT INTO AuditLog (Username, Action, Details, IPAddress, Timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            timestamp = datetime.now()
            params = (username, action, details, ip_address, timestamp)
            self.db.execute_query(query, params)
            
        except Exception as e:
            print(f"Error logging action: {e}")
    
    def get_logs(self, start_date=None, end_date=None, username=None, action=None):
        """Get audit logs with optional filtering"""
        if not self.db:
            return []
            
        try:
            # Build query with filters
            query = "SELECT * FROM AuditLog WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND Timestamp >= %s"
                params.append(start_date)
            if end_date:
                query += " AND Timestamp <= %s"
                params.append(end_date)
            if username:
                query += " AND Username = %s"
                params.append(username)
            if action:
                query += " AND Action = %s"
                params.append(action)
            
            query += " ORDER BY Timestamp DESC"
            
            return self.db.fetch_all(query, params)
        except Exception as e:
            print(f"Error getting logs: {e}")
            return []