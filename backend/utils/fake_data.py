import random
import math
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

def generate_trash_hotspots(lat_min: float, lat_max: float, 
                           lng_min: float, lng_max: float, 
                           zoom_level: int) -> List[Dict]:
    """
    Generate realistic trash hotspot data based on geographic bounds and zoom level
    """
    # Determine number of hotspots based on zoom level and area
    area = (lat_max - lat_min) * (lng_max - lng_min)
    base_density = 200  # hotspots per square degree
    
    # Adjust density based on zoom level (higher zoom = more detail)
    if zoom_level >= 15:
        density_multiplier = 2.0
    elif zoom_level >= 12:
        density_multiplier = 1.5
    elif zoom_level >= 10:
        density_multiplier = 1.0
    else:
        density_multiplier = 0.5
    
    num_hotspots = int(area * base_density * density_multiplier)
    num_hotspots = min(max(num_hotspots, 5), 200)  # Clamp between 5-200
    
    hotspots = []
    
    for i in range(num_hotspots):
        # Generate random location within bounds
        lat = random.uniform(lat_min, lat_max)
        lng = random.uniform(lng_min, lng_max)
        
        # Generate hotspot characteristics
        intensity = random.uniform(0.3, 1.0)
        
        hotspot = {
            "id": f"trash_hotspot_{i+1}",
            "type": "trash_accumulation",
            "location": {
                "latitude": round(lat, 6),
                "longitude": round(lng, 6)
            },
            "intensity": round(intensity, 3),
            "radius_meters": random.randint(50, 500),
            "estimated_items": int(intensity * random.randint(20, 300)),
            "estimated_weight_kg": round(intensity * random.uniform(5, 150), 2),
            "contamination_types": random.sample([
                "plastic_bottles", "food_waste", "paper_debris", 
                "cigarette_butts", "metal_cans", "glass_fragments",
                "electronic_waste", "construction_debris", "medical_waste"
            ], random.randint(2, 5)),
            "risk_level": get_risk_level_from_intensity(intensity),
            "last_updated": generate_recent_timestamp(),
            "verification_status": random.choice([
                "verified", "pending_verification", "user_reported", "ai_detected"
            ]),
            "cleanup_priority": calculate_cleanup_priority(intensity),
            "affected_area_m2": random.randint(100, 2000)
        }
        
        # Add environmental impact data
        hotspot["environmental_impact"] = {
            "soil_contamination": random.choice([True, False]),
            "water_risk": intensity > 0.7,
            "air_quality_impact": intensity > 0.6,
            "wildlife_threat": random.choice([True, False]) if intensity > 0.5 else False
        }
        
        hotspots.append(hotspot)
    
    return hotspots

def generate_water_contamination_zones(lat_min: float, lat_max: float,
                                     lng_min: float, lng_max: float,
                                     zoom_level: int) -> List[Dict]:
    """
    Generate water contamination zone data
    """
    area = (lat_max - lat_min) * (lng_max - lng_min)
    num_zones = int(area * 50 * (zoom_level / 10))  # Fewer water zones than trash
    num_zones = min(max(num_zones, 2), 50)
    
    zones = []
    
    for i in range(num_zones):
        lat = random.uniform(lat_min, lat_max)
        lng = random.uniform(lng_min, lng_max)
        
        contamination_level = random.uniform(0.2, 0.95)
        
        zone = {
            "id": f"water_zone_{i+1}",
            "type": "water_contamination",
            "location": {
                "latitude": round(lat, 6),
                "longitude": round(lng, 6)
            },
            "contamination_level": round(contamination_level, 3),
            "affected_radius_km": round(random.uniform(0.1, 2.0), 2),
            "water_body_type": random.choice([
                "river", "lake", "pond", "stream", "canal", "reservoir", "groundwater"
            ]),
            "contamination_sources": random.sample([
                "industrial_discharge", "sewage_overflow", "agricultural_runoff",
                "solid_waste_leaching", "chemical_spill", "urban_stormwater",
                "illegal_dumping", "oil_spill"
            ], random.randint(1, 3)),
            "pollutants_detected": generate_pollutant_data(contamination_level),
            "water_quality_index": max(0, round(100 - (contamination_level * 100), 1)),
            "health_risk_level": get_health_risk_from_contamination(contamination_level),
            "last_tested": generate_recent_timestamp(),
            "monitoring_frequency": random.choice(["daily", "weekly", "monthly"]),
            "treatment_required": contamination_level > 0.4,
            "estimated_cleanup_cost": round(contamination_level * random.uniform(10000, 100000), 2)
        }
        
        # Add specific water quality parameters
        zone["water_parameters"] = {
            "ph": round(random.uniform(6.0, 9.0), 1),
            "dissolved_oxygen": round(random.uniform(2.0, 12.0), 1),
            "turbidity": round(contamination_level * random.uniform(10, 100), 1),
            "temperature": round(random.uniform(15, 35), 1),
            "conductivity": round(random.uniform(100, 2000), 1)
        }
        
        zones.append(zone)
    
    return zones

def generate_heatmap_data(lat_min: float, lat_max: float,
                         lng_min: float, lng_max: float,
                         zoom_level: int) -> List[Dict]:
    """
    Generate heatmap overlay points for combined environmental data
    """
    # Create a grid of points for smooth heatmap visualization
    if zoom_level >= 15:
        grid_resolution = 0.001  # High detail
    elif zoom_level >= 12:
        grid_resolution = 0.005
    elif zoom_level >= 10:
        grid_resolution = 0.01
    else:
        grid_resolution = 0.02
    
    points = []
    
    lat_current = lat_min
    while lat_current < lat_max:
        lng_current = lng_min
        while lng_current < lng_max:
            # Generate intensity based on urban density simulation
            intensity = simulate_urban_pollution_intensity(lat_current, lng_current)
            
            if intensity > 0.1:  # Only include significant points
                point = {
                    "latitude": round(lat_current, 6),
                    "longitude": round(lng_current, 6),
                    "intensity": round(intensity, 3),
                    "radius": int(intensity * 200) + 50,  # Visual radius for heatmap
                    "data_sources": []
                }
                
                # Determine what contributes to this intensity
                if intensity > 0.7:
                    point["data_sources"].extend(["high_trash_density", "water_contamination"])
                elif intensity > 0.4:
                    point["data_sources"].append("moderate_contamination")
                else:
                    point["data_sources"].append("low_level_pollution")
                
                points.append(point)
            
            lng_current += grid_resolution
        lat_current += grid_resolution
    
    return points

def generate_pollutant_data(contamination_level: float) -> List[Dict]:
    """
    Generate realistic pollutant detection data
    """
    pollutants = [
        {"name": "BOD", "unit": "mg/L", "safe_limit": 3.0},
        {"name": "COD", "unit": "mg/L", "safe_limit": 10.0},
        {"name": "Total_Suspended_Solids", "unit": "mg/L", "safe_limit": 30.0},
        {"name": "Ammonia", "unit": "mg/L", "safe_limit": 0.5},
        {"name": "Nitrates", "unit": "mg/L", "safe_limit": 45.0},
        {"name": "Phosphates", "unit": "mg/L", "safe_limit": 0.1},
        {"name": "Heavy_Metals", "unit": "µg/L", "safe_limit": 50.0},
        {"name": "Coliform_Bacteria", "unit": "CFU/100ml", "safe_limit": 0},
        {"name": "Oil_and_Grease", "unit": "mg/L", "safe_limit": 10.0}
    ]
    
    detected_pollutants = []
    num_pollutants = min(len(pollutants), random.randint(3, 7))
    selected_pollutants = random.sample(pollutants, num_pollutants)
    
    for pollutant in selected_pollutants:
        # Higher contamination = higher pollutant levels
        base_multiplier = 1 + (contamination_level * 5)
        detected_level = pollutant["safe_limit"] * base_multiplier * random.uniform(0.5, 2.0)
        
        detected_pollutants.append({
            "pollutant": pollutant["name"],
            "detected_level": round(detected_level, 3),
            "unit": pollutant["unit"],
            "safe_limit": pollutant["safe_limit"],
            "exceeds_limit": detected_level > pollutant["safe_limit"],
            "risk_factor": min(5.0, detected_level / pollutant["safe_limit"])
        })
    
    return detected_pollutants

def simulate_urban_pollution_intensity(lat: float, lng: float) -> float:
    """
    Simulate pollution intensity based on location using noise functions
    """
    # Create clusters using sine waves (simulating urban centers)
    cluster1 = math.sin(lat * 100) * math.cos(lng * 100)
    cluster2 = math.sin(lat * 150 + 1) * math.cos(lng * 120 + 0.5)
    cluster3 = math.sin(lat * 80 + 2) * math.cos(lng * 90 + 1.5)
    
    # Combine clusters and add some randomness
    base_intensity = (cluster1 + cluster2 + cluster3) / 3
    base_intensity = (base_intensity + 1) / 2  # Normalize to 0-1
    
    # Add random variation
    random_factor = random.uniform(0.7, 1.3)
    intensity = base_intensity * random_factor
    
    # Add distance-based falloff from "city centers"
    city_centers = [(28.6139, 77.2090)]  # Delhi coordinates as example
    
    for center_lat, center_lng in city_centers:
        distance = math.sqrt((lat - center_lat)**2 + (lng - center_lng)**2)
        if distance < 0.1:  # Close to city center
            intensity *= 1.5
        elif distance < 0.2:
            intensity *= 1.2
    
    return max(0, min(1, intensity))

def generate_recent_timestamp() -> str:
    """
    Generate a recent timestamp (within last 30 days)
    """
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    
    timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return timestamp.isoformat() + "Z"

def get_risk_level_from_intensity(intensity: float) -> str:
    """
    Convert intensity to risk level string
    """
    if intensity >= 0.8:
        return "CRITICAL"
    elif intensity >= 0.6:
        return "HIGH"
    elif intensity >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"

def get_health_risk_from_contamination(contamination_level: float) -> str:
    """
    Convert contamination level to health risk
    """
    if contamination_level >= 0.8:
        return "severe"
    elif contamination_level >= 0.6:
        return "high"
    elif contamination_level >= 0.4:
        return "moderate"
    else:
        return "low"

def calculate_cleanup_priority(intensity: float) -> int:
    """
    Calculate cleanup priority score (1-10)
    """
    base_priority = intensity * 8
    
    # Add random variation
    priority = base_priority + random.uniform(-1, 2)
    
    return max(1, min(10, round(priority)))

def generate_satellite_imagery_metadata() -> Dict:
    """
    Generate mock satellite imagery metadata
    """
    satellites = [
        "Sentinel-2A", "Sentinel-2B", "Landsat-8", "Landsat-9",
        "WorldView-3", "SPOT-6", "SPOT-7", "PlanetScope"
    ]
    
    selected_satellite = random.choice(satellites)
    
    # Satellite-specific characteristics
    satellite_specs = {
        "Sentinel-2A": {"resolution": 10, "revisit_days": 10, "spectral_bands": 13},
        "Sentinel-2B": {"resolution": 10, "revisit_days": 10, "spectral_bands": 13},
        "Landsat-8": {"resolution": 30, "revisit_days": 16, "spectral_bands": 11},
        "Landsat-9": {"resolution": 30, "revisit_days": 16, "spectral_bands": 11},
        "WorldView-3": {"resolution": 0.31, "revisit_days": 1, "spectral_bands": 8},
        "SPOT-6": {"resolution": 1.5, "revisit_days": 26, "spectral_bands": 4},
        "SPOT-7": {"resolution": 1.5, "revisit_days": 26, "spectral_bands": 4},
        "PlanetScope": {"resolution": 3, "revisit_days": 1, "spectral_bands": 4}
    }
    
    specs = satellite_specs[selected_satellite]
    
    return {
        "satellite": selected_satellite,
        "acquisition_date": generate_recent_timestamp(),
        "resolution_m": specs["resolution"],
        "cloud_coverage_percent": random.randint(0, 40),
        "sun_elevation": random.randint(30, 80),
        "processing_level": random.choice(["L1C", "L2A", "L3"]),
        "spectral_bands": specs["spectral_bands"],
        "data_quality": random.choice(["excellent", "good", "fair"]),
        "atmospheric_correction": random.choice([True, False]),
        "geometric_accuracy": f"±{random.uniform(1, 10):.1f}m"
    }

def generate_cleanup_cost_estimate(item_count: int, weight_kg: float, 
                                 location_difficulty: str = "medium") -> Dict:
    """
    Generate realistic cleanup cost estimates
    """
    # Base costs per unit
    cost_per_item = 2.5  # USD
    cost_per_kg = 3.0   # USD
    
    # Location difficulty multipliers
    difficulty_multipliers = {
        "easy": 1.0,      # Accessible urban areas
        "medium": 1.5,    # Suburban or partially accessible
        "hard": 2.5,      # Remote or difficult terrain
        "extreme": 4.0    # Hazardous or very remote locations
    }
    
    multiplier = difficulty_multipliers.get(location_difficulty, 1.5)
    
    # Calculate component costs
    labor_cost = (item_count * cost_per_item + weight_kg * cost_per_kg) * multiplier
    equipment_cost = labor_cost * 0.3  # Equipment rental and tools
    transportation_cost = labor_cost * 0.2  # Vehicle costs
    disposal_cost = weight_kg * 1.5  # Proper disposal fees
    overhead = (labor_cost + equipment_cost + transportation_cost) * 0.15
    
    total_cost = labor_cost + equipment_cost + transportation_cost + disposal_cost + overhead
    
    return {
        "total_cost_usd": round(total_cost, 2),
        "cost_breakdown": {
            "labor": round(labor_cost, 2),
            "equipment": round(equipment_cost, 2),
            "transportation": round(transportation_cost, 2),
            "disposal": round(disposal_cost, 2),
            "overhead": round(overhead, 2)
        },
        "location_difficulty": location_difficulty,
        "difficulty_multiplier": multiplier,
        "estimated_crew_size": max(2, int(weight_kg / 20) + 1),
        "estimated_duration_hours": max(2, int(weight_kg / 10) + int(item_count / 50)),
        "specialized_equipment_needed": weight_kg > 100 or item_count > 500
    }

def generate_environmental_impact_metrics(trash_data: Dict) -> Dict:
    """
    Generate environmental impact calculations
    """
    if not trash_data.get("detections"):
        return {"co2_impact": 0, "water_impact": 0, "soil_impact": 0}
    
    total_weight = trash_data.get("estimated_total_weight_kg", 0)
    total_items = trash_data.get("total_items_detected", 0)
    
    # Environmental impact calculations
    co2_saved_by_cleanup = total_weight * 2.3  # kg CO2 per kg waste
    water_contamination_risk = total_weight * 15  # liters of water at risk
    soil_affected_area = total_items * 5  # square meters affected
    
    # Wildlife impact assessment
    wildlife_threat_score = min(10, total_items / 10)  # Scale 1-10
    
    # Microplastics generation potential
    plastic_items = len([d for d in trash_data["detections"] 
                        if "plastic" in d.get("type", "").lower()])
    microplastics_risk = plastic_items * 1000  # particles per plastic item
    
    return {
        "carbon_impact": {
            "co2_equivalent_kg": round(co2_saved_by_cleanup, 2),
            "equivalent_car_km": round(co2_saved_by_cleanup / 0.2, 1),
            "equivalent_tree_months": round(co2_saved_by_cleanup / 0.5, 1)
        },
        "water_impact": {
            "water_at_risk_liters": round(water_contamination_risk, 2),
            "groundwater_threat": total_weight > 10,
            "aquatic_ecosystem_risk": "high" if total_weight > 50 else "medium"
        },
        "soil_impact": {
            "affected_area_m2": round(soil_affected_area, 2),
            "contamination_depth_cm": min(30, total_weight / 2),
            "remediation_time_months": max(1, int(total_weight / 20))
        },
        "biodiversity_impact": {
            "wildlife_threat_score": round(wildlife_threat_score, 1),
            "species_at_risk": max(1, int(wildlife_threat_score / 2)),
            "habitat_degradation": wildlife_threat_score > 5
        },
        "microplastics": {
            "potential_particles": int(microplastics_risk),
            "food_chain_risk": "high" if plastic_items > 10 else "medium"
        }
    }

def generate_weather_impact_data(location: Tuple[float, float]) -> Dict:
    """
    Generate weather data that affects environmental conditions
    """
    lat, lng = location
    
    # Mock weather data (in production, would fetch from weather API)
    current_conditions = {
        "temperature_c": random.randint(20, 40),
        "humidity_percent": random.randint(40, 90),
        "wind_speed_kmh": random.randint(5, 25),
        "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
        "precipitation_mm": random.uniform(0, 50),
        "air_pressure_hpa": random.randint(1000, 1020),
        "uv_index": random.randint(3, 11)
    }
    
    # Calculate environmental impact modifiers
    trash_dispersion_risk = "high" if current_conditions["wind_speed_kmh"] > 20 else "medium"
    water_contamination_spread = "high" if current_conditions["precipitation_mm"] > 20 else "low"
    
    # Vector breeding conditions (for disease risk)
    mosquito_breeding_risk = (
        "high" if current_conditions["temperature_c"] > 25 and 
        current_conditions["humidity_percent"] > 70 else "medium"
    )
    
    return {
        "current_conditions": current_conditions,
        "environmental_modifiers": {
            "trash_dispersion_risk": trash_dispersion_risk,
            "water_contamination_spread": water_contamination_spread,
            "mosquito_breeding_risk": mosquito_breeding_risk,
            "air_quality_dispersion": "good" if current_conditions["wind_speed_kmh"] > 15 else "poor"
        },
        "cleanup_conditions": {
            "recommended_time": "morning" if current_conditions["temperature_c"] < 30 else "evening",
            "safety_precautions": generate_safety_recommendations(current_conditions),
            "equipment_considerations": generate_equipment_recommendations(current_conditions)
        }
    }

def generate_safety_recommendations(weather: Dict) -> List[str]:
    """
    Generate safety recommendations based on weather
    """
    recommendations = []
    
    if weather["temperature_c"] > 35:
        recommendations.extend([
            "Heat stroke precautions required",
            "Frequent hydration breaks",
            "Avoid midday operations"
        ])
    
    if weather["uv_index"] > 8:
        recommendations.append("UV protection essential")
    
    if weather["wind_speed_kmh"] > 20:
        recommendations.append("Secure loose materials to prevent dispersion")
    
    if weather["precipitation_mm"] > 10:
        recommendations.extend([
            "Waterproof equipment required",
            "Slip hazard awareness"
        ])
    
    return recommendations or ["Standard safety protocols apply"]

def generate_equipment_recommendations(weather: Dict) -> List[str]:
    """
    Generate equipment recommendations based on weather
    """
    equipment = ["Standard cleanup kit", "Safety gloves", "First aid supplies"]
    
    if weather["temperature_c"] > 30:
        equipment.extend(["Cooling vests", "Extra water supplies", "Shade tents"])
    
    if weather["precipitation_mm"] > 5:
        equipment.extend(["Waterproof gear", "Non-slip footwear"])
    
    if weather["wind_speed_kmh"] > 15:
        equipment.extend(["Weighted collection bags", "Wind barriers"])
    
    return equipment