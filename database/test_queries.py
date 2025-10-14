"""
Simple test queries for the student grades database
"""
from .connection import DatabaseManager

print("✅ Successfully connected to PostgreSQL database!")

with DatabaseManager() as db:
    print("🔍 Sample Student Data (AEM 6609):")
    result = db.execute_query("SELECT * FROM student_grades WHERE aem = 6609 ORDER BY year, test;")
    for row in result:
        print(f"   {row['year']} {row['test']}: Grade {row['grade']}")
    
    print("\n🔍 2024 Test 1 Results (first 5):")
    result = db.execute_query("SELECT aem, grade FROM student_grades WHERE test = %s AND year = %s ORDER BY grade DESC LIMIT 5;", ("Test 1", 2024))
    for row in result:
        print(f"   AEM {row['aem']}: {row['grade']}")

print("🔌 Database connection closed")