"""
Main application entry point for Railway PostgreSQL Database Project
"""
from database import DatabaseManager
from database_tests import run_all_tests
from advanced_demo import run_advanced_demo
from import_student_data import run_student_data_import, get_student_data_summary

def show_menu():
    """Display the main application menu"""
    print("\n" + "=" * 60)
    print("🚀 RAILWAY POSTGRESQL DATABASE APPLICATION")
    print("=" * 60)
    print("Choose an option:")
    print("1. 🔧 Run Database Connection Tests")
    print("2. 🚀 Run Advanced Demo (with sample data)")
    print("3. 📊 Quick Database Stats")
    print("4. 🔍 Interactive Query Mode")
    print("5. 📚 Student Grades Summary")
    print("6. ❌ Exit")
    print("-" * 60)

def quick_stats():
    """Display quick database statistics"""
    print("\n📊 QUICK DATABASE STATISTICS")
    print("-" * 40)
    
    try:
        with DatabaseManager() as db:
            # Get table counts
            tables_query = """
                SELECT 
                    schemaname,
                    relname as tablename,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables
                ORDER BY relname;
            """
            
            tables = db.execute_query(tables_query)
            if tables:
                print("📋 Table Statistics:")
                for table in tables:
                    print(f"   📂 {table['tablename']}: {table['inserts']} inserts, {table['updates']} updates")
            
            # Get database size
            size_query = "SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;"
            size_result = db.execute_query(size_query)
            if size_result:
                print(f"\n💾 Database Size: {size_result[0]['db_size']}")
            
            # Get user count if users table exists
            user_count = db.execute_query("SELECT COUNT(*) as count FROM users WHERE 1=1;")
            if user_count:
                print(f"👥 Total Users: {user_count[0]['count']}")
            
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

def interactive_query():
    """Interactive query mode"""
    print("\n🔍 INTERACTIVE QUERY MODE")
    print("-" * 40)
    print("Enter SQL queries (type 'exit' to return to menu)")
    print("Example: SELECT * FROM users LIMIT 3;")
    
    try:
        with DatabaseManager() as db:
            while True:
                query = input("\n🔍 SQL> ").strip()
                
                if query.lower() in ('exit', 'quit', 'back'):
                    break
                
                if not query:
                    continue
                
                try:
                    if query.upper().startswith(('SELECT', 'WITH')):
                        results = db.execute_query(query)
                        if results:
                            print(f"\n📊 Results ({len(results)} rows):")
                            for i, row in enumerate(results):
                                if i < 10:  # Limit display to first 10 rows
                                    print(f"   {dict(row)}")
                                elif i == 10:
                                    print(f"   ... and {len(results) - 10} more rows")
                                    break
                        else:
                            print("📊 No results returned")
                    else:
                        success = db.execute_command(query)
                        if success:
                            print("✅ Command executed successfully!")
                        else:
                            print("❌ Command failed")
                            
                except Exception as e:
                    print(f"❌ Query error: {e}")
                    
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")

def main():
    """Main application loop"""
    print("🎉 Welcome to the Railway PostgreSQL Database Application!")
    
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                run_all_tests()
            elif choice == '2':
                run_advanced_demo()
            elif choice == '3':
                quick_stats()
            elif choice == '4':
                interactive_query()
            elif choice == '5':
                get_student_data_summary()
            elif choice == '6':
                print("\n👋 Goodbye! Thanks for using the Railway PostgreSQL Database Application!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()