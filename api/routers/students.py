"""
Student grades router
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import DatabaseManager
from ..models import StudentGrade, StudentGradeCreate, StudentGradeUpdate, StudentStats, APIResponse

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/grades", response_model=List[StudentGrade])
async def get_student_grades(
    aem: Optional[int] = Query(None, description="Filter by student AEM"),
    test: Optional[str] = Query(None, description="Filter by test name"),
    year: Optional[int] = Query(None, description="Filter by year"),
    limit: int = Query(100, description="Limit results", le=1000),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get student grades with optional filters"""
    try:
        with DatabaseManager() as db:
            # Build query based on filters
            where_conditions = []
            params = []
            
            if aem:
                where_conditions.append("aem = %s")
                params.append(aem)
            
            if test:
                where_conditions.append("test = %s")
                params.append(test)
            
            if year:
                where_conditions.append("year = %s")
                params.append(year)
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = f"""
                SELECT id, aem, test, grade, year, created_at, updated_at
                FROM student_grades
                {where_clause}
                ORDER BY year DESC, aem, test
                LIMIT %s OFFSET %s;
            """
            
            params.extend([limit, offset])
            
            results = db.execute_query(query, tuple(params))
            
            if results:
                return [StudentGrade(**row) for row in results]
            else:
                return []
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/grades/{aem}", response_model=List[StudentGrade])
async def get_student_grades_by_aem(aem: int):
    """Get all grades for a specific student"""
    try:
        with DatabaseManager() as db:
            query = """
                SELECT id, aem, test, grade, year, created_at, updated_at
                FROM student_grades
                WHERE aem = %s
                ORDER BY year DESC, test;
            """
            
            results = db.execute_query(query, (aem,))
            
            if results:
                return [StudentGrade(**row) for row in results]
            else:
                raise HTTPException(status_code=404, detail=f"No grades found for student {aem}")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/grades", response_model=APIResponse)
async def create_student_grade(grade_data: StudentGradeCreate):
    """Create a new student grade record"""
    try:
        with DatabaseManager() as db:
            query = """
                INSERT INTO student_grades (aem, test, grade, year)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (aem, test, year) DO UPDATE SET
                    grade = EXCLUDED.grade,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id;
            """
            
            result = db.execute_query(
                query, 
                (grade_data.aem, grade_data.test, grade_data.grade, grade_data.year)
            )
            
            if result:
                return APIResponse(
                    success=True,
                    message="Grade record created/updated successfully",
                    data={"id": result[0]["id"]}
                )
            else:
                raise HTTPException(status_code=400, detail="Failed to create grade record")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/grades/{aem}/{test}/{year}", response_model=APIResponse)
async def update_student_grade(
    aem: int, 
    test: str, 
    year: int, 
    grade_update: StudentGradeUpdate
):
    """Update a specific student grade"""
    try:
        with DatabaseManager() as db:
            # Check if record exists
            check_query = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"
            existing = db.execute_query(check_query, (aem, test, year))
            
            if not existing:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No grade record found for student {aem}, test {test}, year {year}"
                )
            
            # Update the record
            update_query = """
                UPDATE student_grades 
                SET grade = %s, updated_at = CURRENT_TIMESTAMP
                WHERE aem = %s AND test = %s AND year = %s;
            """
            
            success = db.execute_command(
                update_query, 
                (grade_update.grade, aem, test, year)
            )
            
            if success:
                return APIResponse(
                    success=True,
                    message="Grade updated successfully"
                )
            else:
                raise HTTPException(status_code=400, detail="Failed to update grade")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/grades/{aem}/{test}/{year}", response_model=APIResponse)
async def delete_student_grade(aem: int, test: str, year: int):
    """Delete a specific student grade"""
    try:
        with DatabaseManager() as db:
            # Check if record exists
            check_query = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"
            existing = db.execute_query(check_query, (aem, test, year))
            
            if not existing:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No grade record found for student {aem}, test {test}, year {year}"
                )
            
            # Delete the record
            delete_query = "DELETE FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"
            success = db.execute_command(delete_query, (aem, test, year))
            
            if success:
                return APIResponse(
                    success=True,
                    message="Grade deleted successfully"
                )
            else:
                raise HTTPException(status_code=400, detail="Failed to delete grade")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats", response_model=List[StudentStats])
async def get_student_stats(
    limit: int = Query(50, description="Limit results", le=100),
    min_tests: int = Query(1, description="Minimum number of tests", ge=1)
):
    """Get student statistics"""
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
                HAVING COUNT(*) >= %s
                ORDER BY average_grade DESC
                LIMIT %s;
            """
            
            results = db.execute_query(query, (min_tests, limit))
            
            if results:
                return [StudentStats(**row) for row in results]
            else:
                return []
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")