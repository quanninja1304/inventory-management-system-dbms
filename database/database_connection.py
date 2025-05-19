import mysql.connector
from mysql.connector import Error
import logging
from config import (
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
    configure_logging
)


class DatabaseConnection:
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        configure_logging()
        
    # def setup_logging(self):
    #     logging.basicConfig(filename='inventory_system.log', level=logging.INFO,
    #                         format='%(asctime)s - %(levelname)s - %(message)s')
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host or '127.0.0.1',
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                logging.info("Database connection established")
                return True
        except Error as e:
            logging.error(f"Database connection error: {e}")
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
            return []
    
    def get_last_insert_id(self):
        try:
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            return self.cursor.fetchone()["LAST_INSERT_ID()"]
        except Error as e:
            logging.error(f"Error getting last insert ID: {e}")
            return None