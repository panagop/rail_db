"""
Student grades analysis and sample queries
"""
from .connection import DatabaseManager


class StudentAnalytics:
    """Class to handle student grades analytics and reporting"""
    
    @staticmethod
    def run_analysis():
        """Run various analytical queries on student grades data"""
    print("🎓 STUDENT GRADES ANALYSIS")
    print("=" * 60)
    
    try:
        with DatabaseManager() as db:
            # 1. Top 10 students with highest average grades
            print("\n🏆 TOP 10 STUDENTS (Highest Average Grades):")
            print("-" * 50)
            top_students = db.execute_query("""
                SELECT 
                    aem,
                    COUNT(*) as total_tests,
                    ROUND(AVG(grade), 2) as avg_grade,
                    ROUND(MIN(grade), 2) as min_grade,
                    ROUND(MAX(grade), 2) as max_grade
                FROM student_grades 
                GROUP BY aem 
                HAVING COUNT(*) >= 3  -- Students with at least 3 tests
                ORDER BY avg_grade DESC 
                LIMIT 10;
            """)
            
            if top_students:
                for i, student in enumerate(top_students, 1):
                    print(f"{i:2d}. AEM {student['aem']}: Avg {student['avg_grade']} "
                          f"({student['total_tests']} tests, range: {student['min_grade']}-{student['max_grade']})")
            
            # 2. Performance trends over years
            print("\n📈 AVERAGE GRADES BY YEAR:")
            print("-" * 50)
            yearly_trends = db.execute_query("""
                SELECT 
                    year,
                    COUNT(*) as total_records,
                    COUNT(DISTINCT aem) as unique_students,
                    ROUND(AVG(grade), 2) as avg_grade,
                    ROUND(STDDEV(grade), 2) as std_dev
                FROM student_grades 
                GROUP BY year 
                ORDER BY year;
            """)
            
            if yearly_trends:
                for year_data in yearly_trends:
                    print(f"{year_data['year']}: {year_data['avg_grade']} avg "
                          f"({year_data['unique_students']} students, "
                          f"{year_data['total_records']} records, "
                          f"σ={year_data['std_dev']})")
            
            # 3. Test difficulty analysis
            print("\n📝 TEST DIFFICULTY ANALYSIS:")
            print("-" * 50)
            test_difficulty = db.execute_query("""
                SELECT 
                    test,
                    COUNT(*) as total_attempts,
                    ROUND(AVG(grade), 2) as avg_grade,
                    ROUND(STDDEV(grade), 2) as std_dev,
                    COUNT(CASE WHEN grade >= 5.0 THEN 1 END) as passing_count,
                    ROUND(
                        COUNT(CASE WHEN grade >= 5.0 THEN 1 END) * 100.0 / COUNT(*), 1
                    ) as pass_rate
                FROM student_grades 
                GROUP BY test 
                ORDER BY avg_grade DESC;
            """)
            
            if test_difficulty:
                for test_data in test_difficulty:
                    print(f"{test_data['test']}: {test_data['avg_grade']} avg, "
                          f"{test_data['pass_rate']}% pass rate "
                          f"({test_data['passing_count']}/{test_data['total_attempts']}, "
                          f"σ={test_data['std_dev']})")
            
            # 4. Grade distribution
            print("\n📊 GRADE DISTRIBUTION:")
            print("-" * 50)
            grade_distribution = db.execute_query("""
                SELECT 
                    CASE 
                        WHEN grade < 1.0 THEN '0.0-0.9'
                        WHEN grade < 2.0 THEN '1.0-1.9'
                        WHEN grade < 3.0 THEN '2.0-2.9'
                        WHEN grade < 4.0 THEN '3.0-3.9'
                        WHEN grade < 5.0 THEN '4.0-4.9 (Fail)'
                        WHEN grade < 6.0 THEN '5.0-5.9 (Pass)'
                        WHEN grade < 7.0 THEN '6.0-6.9'
                        WHEN grade < 8.0 THEN '7.0-7.9'
                        WHEN grade < 9.0 THEN '8.0-8.9'
                        ELSE '9.0-10.0 (Excellent)'
                    END as grade_range,
                    COUNT(*) as count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_grades), 1) as percentage
                FROM student_grades 
                GROUP BY 
                    CASE 
                        WHEN grade < 1.0 THEN '0.0-0.9'
                        WHEN grade < 2.0 THEN '1.0-1.9'
                        WHEN grade < 3.0 THEN '2.0-2.9'
                        WHEN grade < 4.0 THEN '3.0-3.9'
                        WHEN grade < 5.0 THEN '4.0-4.9 (Fail)'
                        WHEN grade < 6.0 THEN '5.0-5.9 (Pass)'
                        WHEN grade < 7.0 THEN '6.0-6.9'
                        WHEN grade < 8.0 THEN '7.0-7.9'
                        WHEN grade < 9.0 THEN '8.0-8.9'
                        ELSE '9.0-10.0 (Excellent)'
                    END
                ORDER BY MIN(grade);
            """)
            
            if grade_distribution:
                for dist in grade_distribution:
                    bar = "█" * min(20, int(dist['percentage']))
                    print(f"{dist['grade_range']:15}: {dist['count']:4d} ({dist['percentage']:4.1f}%) {bar}")
            
            # 5. Students with perfect scores
            print("\n⭐ PERFECT SCORES (Grade = 10.0):")
            print("-" * 50)
            perfect_scores = db.execute_query("""
                SELECT aem, test, year, grade
                FROM student_grades 
                WHERE grade = 10.0 
                ORDER BY year DESC, aem, test;
            """)
            
            if perfect_scores:
                print(f"Total perfect scores: {len(perfect_scores)}")
                for score in perfect_scores[:10]:  # Show first 10
                    print(f"AEM {score['aem']} - {score['test']} ({score['year']})")
                if len(perfect_scores) > 10:
                    print(f"... and {len(perfect_scores) - 10} more")
            
            # 6. Recent performance (2024)
            print("\n🗓️ 2024 PERFORMANCE:")
            print("-" * 50)
            recent_performance = db.execute_query("""
                SELECT 
                    test,
                    COUNT(*) as attempts,
                    ROUND(AVG(grade), 2) as avg_grade,
                    COUNT(CASE WHEN grade >= 5.0 THEN 1 END) as passing
                FROM student_grades 
                WHERE year = 2024
                GROUP BY test 
                ORDER BY test;
            """)
            
            if recent_performance:
                for perf in recent_performance:
                    pass_rate = round(perf['passing'] * 100.0 / perf['attempts'], 1)
                    print(f"{perf['test']}: {perf['avg_grade']} avg, "
                          f"{pass_rate}% pass rate ({perf['passing']}/{perf['attempts']})")
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")

if __name__ == "__main__":
    StudentAnalytics.run_analysis()