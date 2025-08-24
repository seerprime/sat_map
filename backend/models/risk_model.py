import numpy as np
import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class EnvironmentalRiskModel:
    def __init__(self):
        self.disease_risk_factors = {
            "stagnant_water": {
                "diseases": ["dengue", "malaria", "zika", "chikungunya"],
                "multiplier": 2.5,
                "description": "Breeding ground for disease vectors"
            },
            "organic_waste": {
                "diseases": ["cholera", "typhoid", "hepatitis_a", "gastroenteritis"],
                "multiplier": 2.0,
                "description": "Bacterial contamination risk"
            },
            "plastic_waste": {
                "diseases": ["respiratory_issues", "skin_infections"],
                "multiplier": 1.3,
                "description": "Toxic chemical leaching"
            },
            "industrial_waste": {
                "diseases": ["cancer", "respiratory_disease", "neurological_disorders"],
                "multiplier": 3.0,
                "description": "Heavy metal and chemical contamination"
            }
        }
        
        self.sensitive_locations = {
            "schools": {"radius_km": 0.5, "priority_multiplier": 3.0},
            "hospitals": {"radius_km": 0.3, "priority_multiplier": 2.5},
            "residential": {"radius_km": 0.2, "priority_multiplier": 2.0},
            "water_sources": {"radius_km": 1.0, "priority_multiplier": 4.0},
            "playgrounds": {"radius_km": 0.3, "priority_multiplier": 2.8}
        }
        
        self.environmental_factors = [
            "temperature", "humidity", "rainfall", "wind_speed", 
            "population_density", "waste_management_quality"
        ]
    
    def assess_health_risk(self, location: Tuple[float, float], 
                          trash_data: Dict, water_data: Dict = None) -> Dict:
        """
        Assess disease risk based on environmental contamination
        """
        try:
            # Calculate base risk from trash contamination
            trash_risk = self._calculate_trash_risk(trash_data)
            
            # Calculate water contamination risk
            water_risk = self._calculate_water_risk(water_data) if water_data else 0
            
            # Assess proximity to sensitive locations
            proximity_risk = self._assess_proximity_risk(location)
            
            # Factor in environmental conditions
            environmental_risk = self._assess_environmental_factors(location)
            
            # Calculate combined risk score
            combined_risk = self._calculate_combined_risk(
                trash_risk, water_risk, proximity_risk, environmental_risk
            )
            
            # Generate disease predictions
            disease_predictions = self._predict_disease_risks(
                trash_data, water_data, combined_risk
            )
            
            return {
                "success": True,
                "location": {"lat": location[0], "lng": location[1]},
                "overall_risk_score": combined_risk,
                "risk_level": self._get_risk_level(combined_risk),
                "risk_components": {
                    "trash_contamination": trash_risk,
                    "water_contamination": water_risk,
                    "proximity_to_sensitive_areas": proximity_risk,
                    "environmental_factors": environmental_risk
                },
                "disease_predictions": disease_predictions,
                "priority_score": self._calculate_priority_score(combined_risk, proximity_risk),
                "recommendations": self._generate_risk_recommendations(combined_risk),
                "estimated_affected_population": self._estimate_affected_population(location, combined_risk),
                "assessment_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "overall_risk_score": 0
            }
    
    def _calculate_trash_risk(self, trash_data: Dict) -> float:
        """Calculate risk score from trash contamination data"""
        if not trash_data.get("success", False):
            return 0.1  # Minimal risk if no data
        
        base_risk = 0
        detections = trash_data.get("detections", [])
        
        for detection in detections:
            trash_type = detection.get("type", "")
            confidence = detection.get("confidence", 0)
            weight = detection.get("estimated_weight", 0)
            
            # Risk varies by trash type
            type_risk_multiplier = {
                "plastic": 1.0,
                "metal": 1.5,
                "glass": 1.2,
                "organic": 0.8
            }.get(trash_type, 1.0)