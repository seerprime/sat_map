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
    
    def predict_trash_generation(self, location: tuple, trash_data: dict) -> dict:
        """
        Predict future trash generation at a location.
        Currently a dummy implementation.
        """
        # Example: random small prediction values
        return {
            "predicted_trash_kg_next_week": round(random.uniform(5, 50), 2),
            "predicted_trash_kg_next_month": round(random.uniform(20, 200), 2),
            "confidence": round(random.uniform(0.6, 0.95), 2)
        }
    
    
    def assess_health_risk(self, location: Tuple[float, float], 
                          trash_data: Dict, water_data: Dict = None) -> Dict:
        """
        Assess disease risk based on environmental contamination
        """
        try:
            trash_risk = self._calculate_trash_risk(trash_data)
            water_risk = self._calculate_water_risk(water_data) if water_data else 0
            proximity_risk = self._assess_proximity_risk(location)
            environmental_risk = self._assess_environmental_factors(location)
            
            combined_risk = self._calculate_combined_risk(
                trash_risk, water_risk, proximity_risk, environmental_risk
            )
            
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
            return {"success": False, "error": str(e), "overall_risk_score": 0}
    
    def _calculate_trash_risk(self, trash_data: Dict) -> float:
        if not trash_data.get("success", False):
            return 0.1
        base_risk = 0
        detections = trash_data.get("detections", [])
        for detection in detections:
            trash_type = detection.get("type", "")
            confidence = detection.get("confidence", 0)
            weight = detection.get("estimated_weight", 0)
            type_risk_multiplier = {
                "plastic": 1.0,
                "metal": 1.5,
                "glass": 1.2,
                "organic": 0.8
            }.get(trash_type, 1.0)
            base_risk += confidence * weight * type_risk_multiplier
        return min(base_risk, 10.0)
    
    def _calculate_water_risk(self, water_data: Dict) -> float:
        if not water_data or not water_data.get("success", False):
            return 0.05
        quality_index = water_data.get("quality_index", 1)
        return max(0.1, (1 - quality_index) * 10)
    
    def _assess_proximity_risk(self, location: Tuple[float, float]) -> float:
        return random.uniform(0, 3)
    
    def _assess_environmental_factors(self, location: Tuple[float, float]) -> float:
        return random.uniform(0, 2)
    
    def _calculate_combined_risk(self, trash_risk: float, water_risk: float, 
                                 proximity_risk: float, environmental_risk: float) -> float:
        return trash_risk + water_risk + proximity_risk + environmental_risk
    
    def _predict_disease_risks(self, trash_data: Dict, water_data: Dict, combined_risk: float) -> List[str]:
        diseases = []
        for factor, info in self.disease_risk_factors.items():
            if random.random() < 0.3:
                diseases.extend(info["diseases"])
        return list(set(diseases))
    
    def _get_risk_level(self, score: float) -> str:
        if score < 3: return "low"
        if score < 6: return "medium"
        return "high"
    
    def _calculate_priority_score(self, combined_risk: float, proximity_risk: float) -> float:
        return combined_risk * (1 + proximity_risk / 5)
    
    def _generate_risk_recommendations(self, combined_risk: float) -> List[str]:
        if combined_risk < 3: return ["Monitor area"]
        if combined_risk < 6: return ["Clean area", "Alert local authorities"]
        return ["Immediate cleanup", "Evacuation if necessary", "Medical intervention"]
    
    def _estimate_affected_population(self, location: Tuple[float, float], combined_risk: float) -> int:
        base_population = random.randint(50, 1000)
        return int(base_population * (combined_risk / 10))
    
    # --- NEW METHOD ---
    def calculate_environmental_cost(self, trash_data: Dict, water_data: Dict = None) -> Dict:
        try:
            trash_risk = self._calculate_trash_risk(trash_data)
            water_risk = self._calculate_water_risk(water_data) if water_data else 0
            estimated_cost_usd = (trash_risk * 1000) + (water_risk * 500)
            return {
                "estimated_cost_usd": round(estimated_cost_usd, 2),
                "impact_level": (
                    "low" if estimated_cost_usd < 500 else
                    "medium" if estimated_cost_usd < 2000 else
                    "high"
                ),
                "trash_risk_score": trash_risk,
                "water_risk_score": water_risk
            }
        except Exception as e:
            return {"estimated_cost_usd": 0, "impact_level": "unknown", "error": str(e)}
