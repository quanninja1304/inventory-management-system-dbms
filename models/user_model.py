import bcrypt
from datetime import datetime

class User:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def authenticate(self, username, password):
        """Authenticate a user with username and password"""
        query = "SELECT * FROM Users WHERE Username = %s"
        user = self.db.fetch_one(query, (username,))
        
        if user and self.verify_password(password, user['Password']):
            # Update last login time
            update_query = "UPDATE Users SET LastLogin = %s WHERE UserID = %s"
            self.db.execute_query(update_query, (datetime.now(), user['UserID']))
            return user
        return None
    
    def get_all_users(self):
        """Get all users"""
        query = "SELECT UserID, Username, FullName, Email, Role, LastLogin, Active, CreatedAt FROM Users"
        return self.db.fetch_all(query)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT UserID, Username, FullName, Email, Role, LastLogin, Active, CreatedAt FROM Users WHERE UserID = %s"
        return self.db.fetch_one(query, (user_id,))
    
    def create_user(self, username, password, fullname, email, role):
        """Create a new user"""
        # Check if username already exists
        check_query = "SELECT COUNT(*) as count FROM Users WHERE Username = %s"
        result = self.db.fetch_one(check_query, (username,))
        if result and result['count'] > 0:
            return False, "Username already exists"
        
        # Hash password
        hashed_password = self.hash_password(password)
        
        # Insert new user
        query = """
        INSERT INTO Users (Username, Password, FullName, Email, Role, Active, CreatedAt) 
        VALUES (%s, %s, %s, %s, %s, TRUE, %s)
        """
        params = (username, hashed_password, fullname, email, role, datetime.now())
        success = self.db.execute_query(query, params)
        if success:
            return True, "User created successfully"
        return False, "Failed to create user"
    
    def update_user(self, user_id, fullname, email, role, active):
        """Update user details (except password)"""
        query = """
        UPDATE Users 
        SET FullName = %s, Email = %s, Role = %s, Active = %s 
        WHERE UserID = %s
        """
        params = (fullname, email, role, active, user_id)
        return self.db.execute_query(query, params)
    
    def change_password(self, user_id, new_password):
        """Change user password"""
        hashed_password = self.hash_password(new_password)
        query = "UPDATE Users SET Password = %s WHERE UserID = %s"
        params = (hashed_password, user_id)
        return self.db.execute_query(query, params)
    
    def delete_user(self, user_id):
        """Delete a user"""
        query = "DELETE FROM Users WHERE UserID = %s"
        return self.db.execute_query(query, (user_id,))
    
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify a password against a hash"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)