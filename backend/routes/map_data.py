from turtle import distance
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
import random
import json
from utils.fake_data import generate_trash_hotspots, generate_water_contamination_zones, generate_heatmap_data
import math

router = APIRouter()

@router.get("/heatmap-data")
async def get_heatmap_data(
    lat_min: float = Query(..., description="Minimum latitude"),
    lat_max: float = Query(..., description="Maximum latitude"),
    lng_min: float = Query(..., description="Minimum longitude"), 
    lng_max: float = Query(..., description="Maximum longitude"),
    zoom_level: int = Query(10, description="Map zoom level"),
    data_type: str = Query("all", description="Data type: trash, water, or all")
):
    """
    Get heatmap data for specified geographic bounds
    """
    try:
        # Validate bounds
        if lat_min >= lat_max or lng_min >= lng_max:
            raise HTTPException(status_code=400, detail="Invalid coordinate bounds")
        
        # Generate data based on bounds and zoom level
        response = {
            "bounds": {
                "lat_min": lat_min,
                "lat_max": lat_max, 
                "lng_min": lng_min,
                "lng_max": lng_max
            },
            "zoom_level": zoom_level,
            "data_timestamp": "2025-08-24T10:30:00Z"
        }
        
        if data_type in ["trash", "all"]:
            trash_data = generate_trash_hotspots(lat_min, lat_max, lng_min, lng_max, zoom_level)
            response["trash_hotspots"] = trash_data
        
        if data_type in ["water", "all"]:
            water_data = generate_water_contamination_zones(lat_min, lat_max, lng_min, lng_max, zoom_level)
            response["water_contamination"] = water_data
        
        if data_type == "all":
            # Generate combined heatmap overlay
            heatmap_points = generate_heatmap_data(lat_min, lat_max, lng_min, lng_max, zoom_level)
            response["heatmap_overlay"] = heatmap_points
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate heatmap data: {str(e)}")

@router.get("/hotspots")
async def get_priority_hotspots(
    latitude: float = Query(..., description="Center latitude"),
    longitude: float = Query(..., description="Center longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers"),
    limit: int = Query(50, description="Maximum number of hotspots")
):
    """
    Get priority cleanup hotspots around a location
    """
    try:
        hotspots = []
        
        # Generate priority hotspots within radius
        for i in range(min(limit, random.randint(10, 30))):
            # Generate random point within radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0, radius_km)
            
            # Convert to lat/lng offset
            lat_offset = distance / 111 * random.choice([-1, 1])
            lng_offset = (distance / 111) / max(math.cos(math.radians(latitude)), 0.0001) * random.choice([-1, 1])
            
            hotspot_lat = latitude + lat_offset
            hotspot_lng = longitude + lng_offset
            
            # Generate hotspot data
            hotspot = {
                "id": f"hotspot_{i+1}",
                "location": {
                    "latitude": round(hotspot_lat, 6),
                    "longitude": round(hotspot_lng, 6)
                },
                "priority_score": random.randint(1, 10),
                "risk_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
                "estimated_items": random.randint(5, 200),
                "estimated_weight_kg": round(random.uniform(1, 50), 2),
                "contamination_types": random.sample([
                    "plastic_waste", "organic_waste", "chemical_spill", 
                    "electronic_waste", "construction_debris", "medical_waste"
                ], random.randint(1, 3)),
                "last_updated": "2025-08-24T08:15:00Z",
                "verification_status": random.choice(["unverified", "pending", "verified", "resolved"]),
                "cleanup_cost_estimate": round(random.uniform(100, 5000), 2),
                "affected_area_m2": random.randint(50, 2000),
                "distance_from_query_km": round(distance, 2)
            }
            
            # Add health risks for high priority hotspots
            if hotspot["priority_score"] >= 7:
                hotspot["health_risks"] = {
                    "disease_risk": random.choice(["medium", "high"]),
                    "affected_population": random.randint(100, 5000),
                    "sensitive_areas_nearby": random.choice([True, False])
                }
            
            hotspots.append(hotspot)
        
        # Sort by priority score descending
        hotspots.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return {
            "query_location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "search_radius_km": radius_km,
            "hotspots": hotspots
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve hotspots: {str(e)}")