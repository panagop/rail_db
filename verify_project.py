"""
Simple test script to verify all modules work correctly
"""
import sys

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("🔄 Testing module imports...")
        
        from database import DatabaseManager, DatabaseConnection
        print("✅ database.py - imports successful")
        
        from database_tests import run_all_tests, test_basic_connection, test_context_manager
        print("✅ database_tests.py - imports successful")
        
        from advanced_demo import run_advanced_demo, UserOperations
        print("✅ advanced_demo.py - imports successful")
        
        # Test main.py functions (without running the interactive loop)
        from main import show_menu, quick_stats, interactive_query
        print("✅ main.py - imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test basic database connectivity"""
    try:
        from database import DatabaseConnection
        
        print("\n🔄 Testing database connection...")
        db = DatabaseConnection()
        
        if db.connect():
            print("✅ Database connection successful")
            
            # Quick test query
            result = db.execute_query("SELECT 1 as test;")
            if result and result[0]['test'] == 1:
                print("✅ Query execution successful")
            
            db.disconnect()
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 RAIL_DB PROJECT VERIFICATION")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test database connection
    if not test_database_connection():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n📁 Your project structure:")
        print("   ├── main.py              (Interactive menu application)")
        print("   ├── database.py          (Database connection module)")
        print("   ├── database_tests.py    (Test functions moved here)")
        print("   ├── advanced_demo.py     (Advanced features demo)")
        print("   ├── .env                 (Environment variables)")
        print("   └── pyproject.toml       (Project configuration)")
        
        print("\n🎯 Usage:")
        print("   • Run 'uv run python main.py' for interactive menu")
        print("   • Run 'uv run python database_tests.py' for basic tests")
        print("   • Run 'uv run python advanced_demo.py' for advanced demo")
        
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()