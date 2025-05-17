import mysql.connector
from mysql.connector import Error
import logging
import time

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, configure_logging

class DatabaseConnection:
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, max_retries=3):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.max_retries = max_retries
        
        # Use the configure_logging function from config.py
        configure_logging()
        
        # Connect to the database immediately during initialization
        self.connect()
    
    def connect(self):
        """Connect to the database with retry mechanism"""
        retries = 0
        while retries < self.max_retries:
            try:
                logging.info(f"Attempting to connect to database (Attempt {retries + 1}): {self.database} on {self.host}")
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    connection_timeout=10
                )
                
                if self.connection.is_connected():
                    self.cursor = self.connection.cursor(dictionary=True)
                    db_info = self.connection.get_server_info()
                    logging.info(f"Connected to MySQL server version {db_info}")
                    
                    # Test the connection with a simple query
                    self.cursor.execute("SELECT 1")
                    self.cursor.fetchone()
                    
                    return True
                else:
                    logging.error("Failed to establish a connection")
                    retries += 1
                    if retries < self.max_retries:
                        time.sleep(2)  # Wait before retrying
            except Error as e:
                logging.error(f"Database connection error: {e}")
                retries += 1
                if retries < self.max_retries:
                    time.sleep(2)  # Wait before retrying
                
        logging.error(f"Failed to connect to database after {self.max_retries} attempts")
        return False
    
    def close(self):
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            logging.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            self.connection.commit()
            logging.info(f"Query executed: {query}")
            return True
        except Error as e:
            logging.error(f"Query execution error: {query} - {e}")
            # Check if connection was lost
            if "MySQL Connection not available" in str(e) or "Connection to MySQL is in closed state" in str(e):
                logging.info("Attempting to reconnect...")
                if self.connect():
                    try:
                        # Retry the query after reconnection
                        self.cursor.execute(query, params or ())
                        self.connection.commit()
                        logging.info(f"Query retry successful: {query}")
                        return True
                    except Error as retry_e:
                        logging.error(f"Query retry error: {query} - {retry_e}")
            return False
    
    def fetch_all(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchall()
            logging.info(f"Data fetched: {query}")
            return result
        except Error as e:
            logging.error(f"Data fetch error: {query} - {e}")
            # Check if connection was lost
            if "MySQL Connection not available" in str(e) or "Connection to MySQL is in closed state" in str(e):
                logging.info("Attempting to reconnect...")
                if self.connect():
                    try:
                        # Retry the query after reconnection
                        self.cursor.execute(query, params or ())
                        result = self.cursor.fetchall()
                        logging.info(f"Fetch retry successful: {query}")
                        return result
                    except Error as retry_e:
                        logging.error(f"Fetch retry error: {query} - {retry_e}")
            return []
            
    def fetch_one(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone()
            logging.info(f"Single data fetched: {query}")
            return result
        except Error as e:
            logging.error(f"Single data fetch error: {query} - {e}")
            # Check if connection was lost
            if "MySQL Connection not available" in str(e) or "Connection to MySQL is in closed state" in str(e):
                logging.info("Attempting to reconnect...")
                if self.connect():
                    try:
                        # Retry the query after reconnection
                        self.cursor.execute(query, params or ())
                        result = self.cursor.fetchone()
                        logging.info(f"Fetch retry successful: {query}")
                        return result
                    except Error as retry_e:
                        logging.error(f"Fetch retry error: {query} - {retry_e}")
            return None
    
    def call_procedure(self, procedure_name, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.callproc(procedure_name, params or ())
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            
            logging.info(f"Procedure called: {procedure_name}")
            return results
        except Error as e:
            logging.error(f"Procedure call error: {procedure_name} - {e}")
            # Check if connection was lost
            if "MySQL Connection not available" in str(e) or "Connection to MySQL is in closed state" in str(e):
                logging.info("Attempting to reconnect...")
                if self.connect():
                    try:
                        # Retry the procedure after reconnection
                        self.cursor.callproc(procedure_name, params or ())
                        results = []
                        for result in self.cursor.stored_results():
                            results.extend(result.fetchall())
                        logging.info(f"Procedure retry successful: {procedure_name}")
                        return results
                    except Error as retry_e:
                        logging.error(f"Procedure retry error: {procedure_name} - {retry_e}")
            return []
    
    def get_last_insert_id(self):
        try:
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            return self.cursor.fetchone()["LAST_INSERT_ID()"]
        except Error as e:
            logging.error(f"Error getting last insert ID: {e}")
            return None