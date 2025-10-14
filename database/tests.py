"""
Database connection and functionality tests
"""
from .connection import DatabaseManager, DatabaseConnection

def test_basic_connection():
    """Test basic database connection"""
    print("🔄 Testing database connection...")
    
    db = DatabaseConnection()
    if db.connect():
        # Test with a simple query
        result = db.execute_query("SELECT version();")
        if result:
            print(f"📊 PostgreSQL Version: {result[0]['version']}")
        
        # List all tables in the database
        tables = db.execute_query("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        
        if tables:
            print(f"📋 Tables in database: {[table['table_name'] for table in tables]}")
        else:
            print("📋 No tables found in the database")
        
        db.disconnect()
    else:
        print("❌ Failed to connect to database. Please check your .env file.")

def test_context_manager():
    """Test database connection using context manager"""
    print("\n🔄 Testing database connection with context manager...")
    
    try:
        with DatabaseManager() as db:
            # Example: Create a more comprehensive test table
            create_table = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(150),
                age INTEGER,
                city VARCHAR(100),
                country VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                salary DECIMAL(10, 2),
                join_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            if db.execute_command(create_table):
                print("✅ Users table created successfully!")
                
                # Sample data to insert
                sample_users = [
                    ("john_doe", "john.doe@email.com", "John Doe", 28, "New York", "USA", True, 75000.00),
                    ("jane_smith", "jane.smith@email.com", "Jane Smith", 32, "London", "UK", True, 85000.50),
                    ("carlos_rivera", "carlos.rivera@email.com", "Carlos Rivera", 25, "Madrid", "Spain", True, 55000.75),
                    ("alice_wong", "alice.wong@email.com", "Alice Wong", 29, "Toronto", "Canada", False, 72000.00),
                    ("muhammad_ali", "m.ali@email.com", "Muhammad Ali", 35, "Dubai", "UAE", True, 95000.25),
                    ("sophie_martin", "sophie.martin@email.com", "Sophie Martin", 27, "Paris", "France", True, 68000.00),
                    ("raj_patel", "raj.patel@email.com", "Raj Patel", 31, "Mumbai", "India", True, 45000.50),
                    ("emma_johnson", "emma.j@email.com", "Emma Johnson", 26, "Sydney", "Australia", True, 78000.75),
                    ("lars_nielsen", "lars.nielsen@email.com", "Lars Nielsen", 33, "Copenhagen", "Denmark", False, 82000.00),
                    ("maria_garcia", "maria.garcia@email.com", "Maria Garcia", 30, "Mexico City", "Mexico", True, 52000.25)
                ]
                
                # Insert sample data with conflict handling
                insert_data = """
                INSERT INTO users (username, email, full_name, age, city, country, is_active, salary) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                ON CONFLICT (username) DO NOTHING
                RETURNING id;
                """
                
                inserted_count = 0
                for user_data in sample_users:
                    if db.execute_command(insert_data, user_data):
                        inserted_count += 1
                
                print(f"✅ {inserted_count} users processed (new records or updates)!")
                
                # Query and display the data with various examples
                print("\n📊 Sample Queries:")
                
                # 1. All users
                all_users = db.execute_query("SELECT COUNT(*) as total_users FROM users;")
                if all_users:
                    print(f"👥 Total users in database: {all_users[0]['total_users']}")
                
                # 2. Active users by country
                active_by_country = db.execute_query("""
                    SELECT country, COUNT(*) as active_users, AVG(salary) as avg_salary
                    FROM users 
                    WHERE is_active = TRUE 
                    GROUP BY country 
                    ORDER BY active_users DESC;
                """)
                if active_by_country:
                    print("\n🌍 Active users by country:")
                    for row in active_by_country:
                        print(f"   {row['country']}: {row['active_users']} users, Avg Salary: ${row['avg_salary']:,.2f}")
                
                # 3. Recent users (last 5)
                recent_users = db.execute_query("""
                    SELECT id, username, full_name, city, country, salary, created_at
                    FROM users 
                    ORDER BY created_at DESC 
                    LIMIT 5;
                """)
                if recent_users:
                    print("\n🕒 Most recent users:")
                    for user in recent_users:
                        print(f"   {user['full_name']} (@{user['username']}) - {user['city']}, {user['country']} - ${user['salary']:,.2f}")
                
                # 4. Users by age range
                age_ranges = db.execute_query("""
                    SELECT 
                        CASE 
                            WHEN age < 25 THEN 'Under 25'
                            WHEN age BETWEEN 25 AND 30 THEN '25-30'
                            WHEN age BETWEEN 31 AND 35 THEN '31-35'
                            ELSE 'Over 35'
                        END as age_range,
                        COUNT(*) as user_count,
                        AVG(salary) as avg_salary
                    FROM users 
                    GROUP BY age_range 
                    ORDER BY user_count DESC;
                """)
                if age_ranges:
                    print("\n🎂 Users by age range:")
                    for range_data in age_ranges:
                        print(f"   {range_data['age_range']}: {range_data['user_count']} users, Avg Salary: ${range_data['avg_salary']:,.2f}")
                
                # 5. Top earners
                top_earners = db.execute_query("""
                    SELECT full_name, username, city, country, salary
                    FROM users 
                    WHERE is_active = TRUE
                    ORDER BY salary DESC 
                    LIMIT 3;
                """)
                if top_earners:
                    print("\n💰 Top 3 earners:")
                    for i, user in enumerate(top_earners, 1):
                        print(f"   {i}. {user['full_name']} - {user['city']}, {user['country']} - ${user['salary']:,.2f}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def run_all_tests():
    """Run all database tests"""
    print("🚀 Railway PostgreSQL Connection Test")
    print("=" * 50)
    
    # Test basic connection
    test_basic_connection()
    
    # Test context manager
    test_context_manager()
    
    print("\n✨ Connection tests completed!")
    print("\n💡 Next steps:")
    print("1. Update your .env file with actual Railway database credentials")
    print("2. Run this script to test your connection")
    print("3. Start building your application!")

if __name__ == "__main__":
    run_all_tests()