"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class StudentGrade(BaseModel):
    """Model for student grade data"""
    id: Optional[int] = None
    aem: int = Field(..., description="Student AEM number")
    test: str = Field(..., description="Test name")
    grade: Decimal = Field(..., description="Grade value", ge=0, le=10)
    year: int = Field(..., description="Academic year")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: float
        }


class StudentGradeCreate(BaseModel):
    """Model for creating new student grades"""
    aem: int = Field(..., description="Student AEM number")
    test: str = Field(..., description="Test name")
    grade: float = Field(..., description="Grade value", ge=0, le=10)
    year: int = Field(..., description="Academic year")


class StudentGradeUpdate(BaseModel):
    """Model for updating student grades"""
    grade: Optional[float] = Field(None, description="Grade value", ge=0, le=10)


class StudentStats(BaseModel):
    """Model for student statistics"""
    aem: int
    total_tests: int
    average_grade: float
    min_grade: float
    max_grade: float


class TestStats(BaseModel):
    """Model for test statistics"""
    test: str
    total_attempts: int
    average_grade: float
    pass_rate: float
    min_grade: float
    max_grade: float


class YearlyStats(BaseModel):
    """Model for yearly statistics"""
    year: int
    total_records: int
    unique_students: int
    average_grade: float


class GradeDistribution(BaseModel):
    """Model for grade distribution"""
    grade_range: str
    count: int
    percentage: float


class DatabaseSummary(BaseModel):
    """Model for database summary"""
    total_records: int
    unique_students: int
    years_covered: str
    available_tests: List[str]
    average_grade: float
    min_grade: float
    max_grade: float


class APIResponse(BaseModel):
    """Generic API response model"""
    success: bool
    message: str
    data: Optional[dict] = None