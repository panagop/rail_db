"""
Analytics router for statistical endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import DatabaseManager
from ..models import TestStats, YearlyStats, GradeDistribution, DatabaseSummary

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=DatabaseSummary)
async def get_database_summary():
    """Get overall database summary statistics"""
    try:
        with DatabaseManager() as db:
            # Total records and students
            total_query = """
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT aem) as unique_students
                FROM student_grades;
            """
            total_result = db.execute_query(total_query)
            
            # Year range
            year_query = "SELECT MIN(year) as min_year, MAX(year) as max_year FROM student_grades;"
            year_result = db.execute_query(year_query)
            
            # Available tests
            tests_query = "SELECT DISTINCT test FROM student_grades ORDER BY test;"
            tests_result = db.execute_query(tests_query)
            
            # Grade statistics
            grade_query = """
                SELECT 
                    ROUND(AVG(grade), 2) as avg_grade,
                    ROUND(MIN(grade), 2) as min_grade,
                    ROUND(MAX(grade), 2) as max_grade
                FROM student_grades;
            """
            grade_result = db.execute_query(grade_query)
            
            if total_result and year_result and tests_result and grade_result:
                return DatabaseSummary(
                    total_records=total_result[0]["total_records"],
                    unique_students=total_result[0]["unique_students"],
                    years_covered=f"{year_result[0]['min_year']}-{year_result[0]['max_year']}",
                    available_tests=[test["test"] for test in tests_result],
                    average_grade=float(grade_result[0]["avg_grade"]),
                    min_grade=float(grade_result[0]["min_grade"]),
                    max_grade=float(grade_result[0]["max_grade"])
                )
            else:
                raise HTTPException(status_code=404, detail="No data found")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/test-stats", response_model=List[TestStats])
async def get_test_statistics():
    """Get statistics for each test"""
    try:
        with DatabaseManager() as db:
            query = """
                SELECT 
                    test,
                    COUNT(*) as total_attempts,
                    ROUND(AVG(grade), 2) as average_grade,
                    COUNT(CASE WHEN grade >= 5.0 THEN 1 END) * 100.0 / COUNT(*) as pass_rate,
                    ROUND(MIN(grade), 2) as min_grade,
                    ROUND(MAX(grade), 2) as max_grade
                FROM student_grades 
                GROUP BY test 
                ORDER BY average_grade DESC;
            """
            
            results = db.execute_query(query)
            
            if results:
                return [
                    TestStats(
                        test=row["test"],
                        total_attempts=row["total_attempts"],
                        average_grade=float(row["average_grade"]),
                        pass_rate=float(row["pass_rate"]),
                        min_grade=float(row["min_grade"]),
                        max_grade=float(row["max_grade"])
                    ) for row in results
                ]
            else:
                return []
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/yearly-stats", response_model=List[YearlyStats])
async def get_yearly_statistics():
    """Get statistics by year"""
    try:
        with DatabaseManager() as db:
            query = """
                SELECT 
                    year,
                    COUNT(*) as total_records,
                    COUNT(DISTINCT aem) as unique_students,
                    ROUND(AVG(grade), 2) as average_grade
                FROM student_grades 
                GROUP BY year 
                ORDER BY year DESC;
            """
            
            results = db.execute_query(query)
            
            if results:
                return [YearlyStats(**row) for row in results]
            else:
                return []
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/grade-distribution", response_model=List[GradeDistribution])
async def get_grade_distribution():
    """Get grade distribution across all records"""
    try:
        with DatabaseManager() as db:
            query = """
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
                        WHEN grade < 8.0 THEN '8.0-8.9'
                        ELSE '9.0-10.0 (Excellent)'
                    END
                ORDER BY MIN(grade);
            """
            
            results = db.execute_query(query)
            
            if results:
                return [GradeDistribution(**row) for row in results]
            else:
                return []
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/top-students")
async def get_top_students(limit: int = Query(10, description="Number of top students", le=50)):
    """Get top performing students"""
    try:
        with DatabaseManager() as db:
            query = """
                SELECT 
                    aem,
                    COUNT(*) as total_tests,
                    ROUND(AVG(grade), 2) as average_grade,
                    ROUND(MIN(grade), 2) as min_grade,
                    ROUND(MAX(grade), 2) as max_grade
                FROM student_grades 
                GROUP BY aem 
                HAVING COUNT(*) >= 3
                ORDER BY average_grade DESC 
                LIMIT %s;
            """
            
            results = db.execute_query(query, (limit,))
            
            if results:
                return {
                    "top_students": [
                        {
                            "aem": row["aem"],
                            "total_tests": row["total_tests"],
                            "average_grade": float(row["average_grade"]),
                            "min_grade": float(row["min_grade"]),
                            "max_grade": float(row["max_grade"])
                        } for row in results
                    ]
                }
            else:
                return {"top_students": []}
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/perfect-scores")
async def get_perfect_scores():
    """Get all perfect score records"""
    try:
        with DatabaseManager() as db:
            query = """
                SELECT aem, test, year, grade
                FROM student_grades 
                WHERE grade = 10.0 
                ORDER BY year DESC, aem, test;
            """
            
            results = db.execute_query(query)
            
            if results:
                return {
                    "total_perfect_scores": len(results),
                    "perfect_scores": [
                        {
                            "aem": row["aem"],
                            "test": row["test"],
                            "year": row["year"],
                            "grade": float(row["grade"])
                        } for row in results
                    ]
                }
            else:
                return {"total_perfect_scores": 0, "perfect_scores": []}
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")