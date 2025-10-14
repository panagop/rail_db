"""
Student grades data import module
"""
import json
import os
from database import DatabaseManager

def load_student_data():
    """Load student data from the JavaScript file"""
    js_file_path = os.path.join(os.path.dirname(__file__), 'old_files', 'betongrades.js')
    
    with open(js_file_path, 'r') as file:
        content = file.read()
    
    # Extract the JSON array from the JavaScript variable declaration
    # Find the start of the array
    start_index = content.find('[')
    if start_index == -1:
        raise ValueError("Could not find JSON array in the file")
    
    # Extract just the JSON array part
    json_data = content[start_index:]
    
    # Parse the JSON data
    student_grades = json.loads(json_data)
    
    print(f"✅ Loaded {len(student_grades)} student grade records")
    return student_grades

def create_student_grades_table():
    """Create the student_grades table"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS student_grades (
        id SERIAL PRIMARY KEY,
        aem INTEGER NOT NULL,
        test VARCHAR(50) NOT NULL,
        grade DECIMAL(10, 8) NOT NULL,
        year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(aem, test, year)  -- Prevent duplicate entries for same student/test/year
    );
    """
    
    # Create index for better query performance
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_student_grades_aem ON student_grades(aem);",
        "CREATE INDEX IF NOT EXISTS idx_student_grades_year ON student_grades(year);",
        "CREATE INDEX IF NOT EXISTS idx_student_grades_test ON student_grades(test);",
        "CREATE INDEX IF NOT EXISTS idx_student_grades_grade ON student_grades(grade);"
    ]
    
    with DatabaseManager() as db:
        # Create table
        if db.execute_command(create_table_sql):
            print("✅ Student grades table created successfully!")
        
        # Create indexes
        for index_sql in create_indexes_sql:
            db.execute_command(index_sql)
        
        print("✅ Database indexes created successfully!")

def import_student_data():
    """Import student data into the database"""
    try:
        # Load data from file
        student_data = load_student_data()
        
        # Create table
        create_student_grades_table()
        
        # Insert data
        with DatabaseManager() as db:
            insert_sql = """
            INSERT INTO student_grades (aem, test, grade, year) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (aem, test, year) DO UPDATE SET
                grade = EXCLUDED.grade,
                updated_at = CURRENT_TIMESTAMP;
            """
            
            inserted_count = 0
            updated_count = 0
            
            for record in student_data:
                aem = record['AEM']
                test = record['Test']
                grade = record['Grade']
                year = record['Year']
                
                # Check if record exists
                check_sql = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"
                existing = db.execute_query(check_sql, (aem, test, year))
                
                if db.execute_command(insert_sql, (aem, test, grade, year)):
                    if existing:
                        updated_count += 1
                    else:
                        inserted_count += 1
            
            print(f"✅ Data import completed!")
            print(f"   📊 New records inserted: {inserted_count}")
            print(f"   🔄 Records updated: {updated_count}")
            print(f"   📋 Total records processed: {len(student_data)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        return False

def get_student_data_summary():
    """Get summary statistics of the imported data"""
    with DatabaseManager() as db:
        print("\n📊 STUDENT GRADES DATA SUMMARY")
        print("=" * 50)
        
        # Total records
        total_records = db.execute_query("SELECT COUNT(*) as total FROM student_grades;")
        if total_records:
            print(f"📋 Total Records: {total_records[0]['total']:,}")
        
        # Unique students
        unique_students = db.execute_query("SELECT COUNT(DISTINCT aem) as students FROM student_grades;")
        if unique_students:
            print(f"👥 Unique Students: {unique_students[0]['students']:,}")
        
        # Years covered
        year_range = db.execute_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM student_grades;")
        if year_range:
            print(f"📅 Years Covered: {year_range[0]['min_year']} - {year_range[0]['max_year']}")
        
        # Tests available
        tests = db.execute_query("SELECT DISTINCT test FROM student_grades ORDER BY test;")
        if tests:
            test_list = [test['test'] for test in tests]
            print(f"📝 Available Tests: {', '.join(test_list)}")
        
        # Grade statistics
        grade_stats = db.execute_query("""
            SELECT 
                ROUND(AVG(grade), 2) as avg_grade,
                ROUND(MIN(grade), 2) as min_grade,
                ROUND(MAX(grade), 2) as max_grade,
                ROUND(STDDEV(grade), 2) as std_dev
            FROM student_grades;
        """)
        if grade_stats:
            stats = grade_stats[0]
            print(f"📈 Grade Statistics:")
            print(f"   Average: {stats['avg_grade']}")
            print(f"   Range: {stats['min_grade']} - {stats['max_grade']}")
            print(f"   Std Dev: {stats['std_dev']}")
        
        # Records per year
        yearly_stats = db.execute_query("""
            SELECT 
                year, 
                COUNT(*) as record_count,
                COUNT(DISTINCT aem) as student_count,
                ROUND(AVG(grade), 2) as avg_grade
            FROM student_grades 
            GROUP BY year 
            ORDER BY year;
        """)
        if yearly_stats:
            print(f"\n📊 Records by Year:")
            for year_data in yearly_stats:
                print(f"   {year_data['year']}: {year_data['record_count']} records, "
                      f"{year_data['student_count']} students, "
                      f"avg grade: {year_data['avg_grade']}")
        
        # Records per test
        test_stats = db.execute_query("""
            SELECT 
                test, 
                COUNT(*) as record_count,
                ROUND(AVG(grade), 2) as avg_grade,
                ROUND(MIN(grade), 2) as min_grade,
                ROUND(MAX(grade), 2) as max_grade
            FROM student_grades 
            GROUP BY test 
            ORDER BY test;
        """)
        if test_stats:
            print(f"\n📝 Statistics by Test:")
            for test_data in test_stats:
                print(f"   {test_data['test']}: {test_data['record_count']} records, "
                      f"avg: {test_data['avg_grade']}, "
                      f"range: {test_data['min_grade']}-{test_data['max_grade']}")

def run_student_data_import():
    """Main function to run the student data import"""
    print("🚀 STUDENT GRADES DATA IMPORT")
    print("=" * 50)
    
    if import_student_data():
        get_student_data_summary()
        
        print(f"\n💡 Sample Queries:")
        print(f"   SELECT * FROM student_grades WHERE aem = 6609;")
        print(f"   SELECT * FROM student_grades WHERE test = 'Test 1' AND year = 2024;")
        print(f"   SELECT aem, AVG(grade) as avg_grade FROM student_grades GROUP BY aem ORDER BY avg_grade DESC;")
        print(f"   SELECT year, test, AVG(grade) as avg_grade FROM student_grades GROUP BY year, test ORDER BY year, test;")
    else:
        print("❌ Import failed. Please check the error messages above.")

if __name__ == "__main__":
    run_student_data_import()