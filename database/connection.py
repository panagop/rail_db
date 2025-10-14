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
            # Debug: Check all environment variables
            database_url = os.getenv('DATABASE_URL')
            print(f"🔍 DEBUG - DATABASE_URL exists: {database_url is not None}")
            if database_url:
                print(f"🔍 DEBUG - DATABASE_URL starts with: {database_url[:20]}...")
            
            # Check Railway-specific variables
            railway_vars = [
                'PGHOST', 'PGPORT', 'PGDATABASE', 'PGUSER', 'PGPASSWORD',
                'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'
            ]
            for var in railway_vars:
                value = os.getenv(var)
                if value:
                    print(f"🔍 DEBUG - {var}: {'*' * 10 if 'PASS' in var else value}")
            
            # Try to use DATABASE_URL first (recommended for Railway)
            if database_url:
                print("🔄 Attempting connection with DATABASE_URL...")
                self.connection = psycopg2.connect(database_url)
            else:
                print("🔄 DATABASE_URL not found, trying individual components...")
                # Try Railway's individual PostgreSQL variables
                host = os.getenv('PGHOST') or os.getenv('DB_HOST', 'localhost')
                port = os.getenv('PGPORT') or os.getenv('DB_PORT', '5432')
                database = os.getenv('PGDATABASE') or os.getenv('DB_NAME', 'postgres')
                user = os.getenv('PGUSER') or os.getenv('DB_USER', 'postgres')
                password = os.getenv('PGPASSWORD') or os.getenv('DB_PASSWORD', '')
                
                print(f"🔄 Connecting to: {host}:{port}/{database} as {user}")
                
                self.connection = psycopg2.connect(
                    host=host,
                    port=int(port),
                    database=database,
                    user=user,
                    password=password
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