import ttkbootstrap as ttk
from controllers.controller import Controller
import os
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# First run setup - check if database exists and users table exists
def check_database_setup():
    try:
        # Try to connect to the MySQL server without specifying a database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor(dictionary=True)
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        result = cursor.fetchone()
        database_exists = result is not None
        
        if not database_exists:
            print(f"Database {DB_NAME} does not exist. Setting up new database...")
            # Create database
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database {DB_NAME} created.")
        
        # Connect to the database
        cursor.execute(f"USE {DB_NAME}")
        
        # Check if Tables exist
        cursor.execute("SHOW TABLES LIKE 'Users'")
        users_table_exists = cursor.fetchone() is not None
        
        if not users_table_exists:
            print("Users table does not exist. Running setup scripts...")
            
            # Execute the SQL scripts
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql", "sql_script.sql")
            users_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql", "users_schema.sql")
            
            # Execute main SQL script if it's a new database
            if not database_exists:
                with open(script_path, 'r') as f:
                    # Split the script into separate commands
                    for command in f.read().split(';'):
                        if command.strip():
                            try:
                                cursor.execute(command)
                                conn.commit()
                            except Exception as e:
                                print(f"Error executing SQL command: {e}")
                                print(f"Command: {command}")
            
            # Execute users schema SQL
            with open(users_script_path, 'r') as f:
                for command in f.read().split(';'):
                    if command.strip():
                        try:
                            cursor.execute(command)
                            conn.commit()
                        except Exception as e:
                            print(f"Error executing SQL command: {e}")
                            print(f"Command: {command}")
            
            print("Database setup completed.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    # Check database setup
    if check_database_setup():
        # Start the application
        root = ttk.Window()
        app = Controller(root)
        root.mainloop()
    else:
        print("Failed to set up database. Please check your configuration.")