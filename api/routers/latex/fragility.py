"""
LaTeX equations router for structural engineering formulas
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import math
import scipy.stats as stats
from ...models.latex_models import LatexEquation, ParameterizedEquation, FragilityParameters

router = APIRouter(prefix="/latex", tags=["latex"])


def calculate_fragility_probability(pga: float, pga_mean: float, beta: float) -> float:
    """Calculate fragility curve probability using lognormal distribution"""
    if pga <= 0 or pga_mean <= 0 or beta <= 0:
        raise ValueError("All parameters must be positive")
    
    # Calculate the standardized variable
    z = (1 / beta) * math.log(pga / pga_mean)
    
    # Return the cumulative probability using standard normal distribution
    return stats.norm.cdf(z)


@router.get("/fragility/basic", response_model=LatexEquation)
async def get_basic_fragility_equation():
    """Get the basic fragility curve equation in LaTeX format"""
    return LatexEquation(
        name="Fragility Curve - Basic Form",
        category="fragility",
        latex=r"P[ds \geq ds_i\;/\;PGA] = \Phi \left[ \frac{1}{\beta_{ds_i}} \ln \left( \frac{PGA}{\overline{PGA}_{ds_i}} \right) \right]",
        description="Probability of exceeding damage state ds_i given Peak Ground Acceleration (PGA)",
        variables={
            "P[ds ≥ ds_i / PGA]": "Probability of exceeding damage state ds_i given PGA",
            "Φ": "Standard normal cumulative distribution function",
            "β_{ds_i}": "Standard deviation of the natural logarithm of PGA for damage state ds_i",
            "PGA": "Peak Ground Acceleration",
            "\\overline{PGA}_{ds_i}": "Median PGA capacity for damage state ds_i"
        }
    )


@router.get("/fragility/parameterized", response_model=ParameterizedEquation)
async def get_parameterized_fragility(
    pga: float = Query(..., description="Peak Ground Acceleration", gt=0),
    pga_mean: float = Query(..., description="Mean PGA for damage state", gt=0),
    beta: float = Query(..., description="Beta parameter (log standard deviation)", gt=0),
    damage_state: str = Query("ds_i", description="Damage state identifier")
):
    """Get fragility equation with specific parameter values and numerical result"""
    
    try:
        # Calculate the probability
        probability = calculate_fragility_probability(pga, pga_mean, beta)
        
        # Create LaTeX with substituted values
        latex_with_values = (
            f"P[ds \\geq {damage_state}\\;/\\;PGA] = \\Phi \\left[ "
            f"\\frac{{1}}{{{beta:.3f}}} \\ln \\left( \\frac{{{pga:.3f}}}{{{pga_mean:.3f}}} \\right) \\right] "
            f"= \\Phi \\left[ {(1/beta) * math.log(pga/pga_mean):.3f} \\right] = {probability:.4f}"
        )
        
        return ParameterizedEquation(
            name=f"Fragility Curve - {damage_state}",
            category="fragility",
            latex=r"P[ds \geq ds_i\;/\;PGA] = \Phi \left[ \frac{1}{\beta_{ds_i}} \ln \left( \frac{PGA}{\overline{PGA}_{ds_i}} \right) \right]",
            description=f"Fragility curve calculation for damage state {damage_state}",
            parameters={
                "PGA": pga,
                "PGA_mean": pga_mean,
                "beta": beta
            },
            latex_with_values=latex_with_values,
            numerical_result=probability,
            variables={
                "P[ds ≥ ds_i / PGA]": f"Probability of exceeding {damage_state} given PGA = {probability:.4f}",
                "Φ": "Standard normal CDF",
                "β_{ds_i}": f"Log standard deviation = {beta}",
                "PGA": f"Peak Ground Acceleration = {pga}",
                "\\overline{PGA}_{ds_i}": f"Median capacity = {pga_mean}"
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/fragility/calculate", response_model=ParameterizedEquation)
async def calculate_fragility_with_params(params: FragilityParameters):
    """Calculate fragility probability using POST with parameter object"""
    
    try:
        probability = calculate_fragility_probability(
            params.pga, 
            params.pga_mean, 
            params.beta
        )
        
        # Create detailed LaTeX with step-by-step calculation
        z_value = (1/params.beta) * math.log(params.pga / params.pga_mean)
        
        latex_with_values = (
            f"P[ds \\geq {params.damage_state}\\;/\\;PGA] = \\Phi \\left[ "
            f"\\frac{{1}}{{{params.beta:.3f}}} \\ln \\left( \\frac{{{params.pga:.3f}}}{{{params.pga_mean:.3f}}} \\right) \\right]\\\\[0.5em]"
            f"= \\Phi \\left[ \\frac{{1}}{{{params.beta:.3f}}} \\times {math.log(params.pga / params.pga_mean):.3f} \\right]\\\\[0.5em]"
            f"= \\Phi \\left[ {z_value:.3f} \\right]\\\\[0.5em]"
            f"= {probability:.4f}"
        )
        
        return ParameterizedEquation(
            name=f"Fragility Analysis - {params.damage_state}",
            category="fragility",
            latex=r"P[ds \geq ds_i\;/\;PGA] = \Phi \left[ \frac{1}{\beta_{ds_i}} \ln \left( \frac{PGA}{\overline{PGA}_{ds_i}} \right) \right]",
            description=f"Complete fragility curve analysis for {params.damage_state}",
            parameters={
                "PGA": params.pga,
                "PGA_mean": params.pga_mean,
                "beta": params.beta,
                "z_value": z_value
            },
            latex_with_values=latex_with_values,
            numerical_result=probability,
            variables={
                "P[ds ≥ ds_i / PGA]": f"Exceedance probability = {probability:.4f}",
                "Φ(z)": f"Standard normal CDF of z = {z_value:.3f}",
                "z": f"Standardized variable = {z_value:.3f}",
                "ln(PGA/PGA_mean)": f"Natural log ratio = {math.log(params.pga / params.pga_mean):.3f}"
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.get("/fragility/examples")
async def get_fragility_examples():
    """Get example fragility calculations for common scenarios"""
    
    examples = []
    
    # Example scenarios
    scenarios = [
        {"name": "Light Damage", "pga": 0.1, "pga_mean": 0.2, "beta": 0.5, "ds": "Light"},
        {"name": "Moderate Damage", "pga": 0.3, "pga_mean": 0.4, "beta": 0.6, "ds": "Moderate"},
        {"name": "Heavy Damage", "pga": 0.6, "pga_mean": 0.8, "beta": 0.7, "ds": "Heavy"},
        {"name": "Complete Damage", "pga": 1.0, "pga_mean": 1.2, "beta": 0.8, "ds": "Complete"}
    ]
    
    for scenario in scenarios:
        try:
            prob = calculate_fragility_probability(
                scenario["pga"], 
                scenario["pga_mean"], 
                scenario["beta"]
            )
            
            examples.append({
                "scenario": scenario["name"],
                "parameters": {
                    "PGA": scenario["pga"],
                    "PGA_mean": scenario["pga_mean"],
                    "beta": scenario["beta"]
                },
                "probability": round(prob, 4),
                "percentage": f"{prob * 100:.2f}%",
                "latex": f"P[ds \\geq {scenario['ds']}] = \\Phi[{(1/scenario['beta']) * math.log(scenario['pga']/scenario['pga_mean']):.3f}] = {prob:.4f}"
            })
            
        except Exception as e:
            examples.append({
                "scenario": scenario["name"],
                "error": str(e)
            })
    
    return {
        "description": "Common fragility curve calculation examples",
        "base_equation": r"P[ds \geq ds_i\;/\;PGA] = \Phi \left[ \frac{1}{\beta_{ds_i}} \ln \left( \frac{PGA}{\overline{PGA}_{ds_i}} \right) \right]",
        "examples": examples
    }


@router.get("/equations", response_model=List[LatexEquation])
async def list_all_equations():
    """Get a list of all available LaTeX equations"""
    
    equations = [
        LatexEquation(
            name="Fragility Curve - Basic",
            category="fragility",
            latex=r"P[ds \geq ds_i\;/\;PGA] = \Phi \left[ \frac{1}{\beta_{ds_i}} \ln \left( \frac{PGA}{\overline{PGA}_{ds_i}} \right) \right]",
            description="Basic fragility curve equation for seismic damage assessment"
        ),
        LatexEquation(
            name="Standard Normal CDF",
            category="statistics", 
            latex=r"\Phi(z) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{z} e^{-\frac{t^2}{2}} dt",
            description="Standard normal cumulative distribution function"
        ),
        LatexEquation(
            name="Lognormal Distribution",
            category="statistics",
            latex=r"f(x) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}}",
            description="Probability density function of lognormal distribution"
        )
    ]
    
    return equations