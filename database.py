"""
Database connection module for Railway PostgreSQL
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to the PostgreSQL database using DATABASE_URL or individual components"""
        try:
            # Try to use DATABASE_URL first (recommended for Railway)
            database_url = os.getenv('DATABASE_URL')
            
            if database_url:
                self.connection = psycopg2.connect(database_url)
            else:
                # Fallback to individual components
                self.connection = psycopg2.connect(
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT', 5432),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
            
            # Use RealDictCursor to get results as dictionaries
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✅ Successfully connected to PostgreSQL database!")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Error connecting to PostgreSQL database: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔌 Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"❌ Error executing query: {e}")
            return None
    
    def execute_command(self, command, params=None):
        """Execute an INSERT, UPDATE, or DELETE command"""
        try:
            self.cursor.execute(command, params)
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            print(f"❌ Error executing command: {e}")
            self.connection.rollback()
            return False

# Context manager for automatic connection handling
class DatabaseManager:
    def __enter__(self):
        self.db = DatabaseConnection()
        if self.db.connect():
            return self.db
        else:
            raise Exception("Failed to connect to database")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.disconnect()