"""
Simple student data utilities
"""
from .connection import DatabaseManager


def get_student_data_summary():
    """Get summary statistics of the imported student data"""
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
            print("📈 Grade Statistics:")
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
            ORDER BY year DESC
            LIMIT 5;
        """)
        if yearly_stats:
            print("\n📊 Recent Years Performance:")
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
                ROUND(
                    COUNT(CASE WHEN grade >= 5.0 THEN 1 END) * 100.0 / COUNT(*), 1
                ) as pass_rate
            FROM student_grades 
            GROUP BY test 
            ORDER BY test;
        """)
        if test_stats:
            print("\n📝 Statistics by Test:")
            for test_data in test_stats:
                print(f"   {test_data['test']}: {test_data['record_count']} records, "
                      f"avg: {test_data['avg_grade']}, "
                      f"pass rate: {test_data['pass_rate']}%")