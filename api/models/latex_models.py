"""
LaTeX equations models for API responses
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class LatexEquation(BaseModel):
    """Base model for LaTeX equations"""
    name: str = Field(..., description="Name of the equation")
    category: str = Field(..., description="Category (e.g., 'fragility', 'seismic')")
    latex: str = Field(..., description="LaTeX code for the equation")
    description: Optional[str] = Field(None, description="Description of the equation")
    variables: Optional[Dict[str, str]] = Field(None, description="Variable definitions")


class ParameterizedEquation(LatexEquation):
    """Model for equations with parameters"""
    parameters: Optional[Dict[str, float]] = Field(None, description="Parameter values")
    latex_with_values: Optional[str] = Field(None, description="LaTeX with substituted values")
    numerical_result: Optional[float] = Field(None, description="Computed numerical result")


class FragilityParameters(BaseModel):
    """Parameters for fragility curve calculations"""
    pga: float = Field(..., description="Peak Ground Acceleration", ge=0)
    pga_mean: float = Field(..., description="Mean PGA for damage state", gt=0)
    beta: float = Field(..., description="Beta parameter (standard deviation)", gt=0)
    damage_state: Optional[str] = Field("ds_i", description="Damage state identifier")