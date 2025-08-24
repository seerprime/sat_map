from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional, List
import os
import uuid
from PIL import Image
import io
from models.trash_detector import TrashDetector
from models.water_quality import WaterQualityAnalyzer
from models.risk_model import EnvironmentalRiskModel
from utils.config import settings
import json

router = APIRouter()

# Initialize AI models
trash_detector = TrashDetector()
water_analyzer = WaterQualityAnalyzer()
risk_model = EnvironmentalRiskModel()

@router.post("/detect-trash")
async def detect_trash(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    user_id: Optional[str] = Form(None)
):
    """
    Detect trash in uploaded image using AI
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Run trash detection
        detection_results = trash_detector.detect_trash(contents)
        
        # Calculate environmental cost if detection successful
        environmental_cost = {}
        if detection_results.get("success"):
            environmental_cost = risk_model.calculate_environmental_cost(detection_results)
        
        # Generate response
        response = {
            **detection_results,
            "file_info": {
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "file_size_bytes": len(contents),
                "upload_timestamp": "2025-08-24T10:30:00Z"
            },
            "environmental_impact": environmental_cost
        }
        
        # Add location if provided
        if latitude is not None and longitude is not None:
            response["location"] = {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": "user_provided"
            }
        
        # Add user tracking if provided
        if user_id:
            response["user_id"] = user_id
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@router.post("/analyze-water")
async def analyze_water_quality(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    user_id: Optional[str] = Form(None)
):
    """
    Analyze water quality from satellite/drone imagery
    """
    try:
        # Validate file (same as trash detection)
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Invalid file type")
        
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        unique_filename = f"water_{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Analyze water quality
        location = (latitude, longitude) if latitude and longitude else None
        water_results = water_analyzer.analyze_water_quality(contents, location)
        
        response = {
            **water_results,
            "file_info": {
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "file_size_bytes": len(contents),
                "upload_timestamp": "2025-08-24T10:30:00Z"
            }
        }
        
        if location:
            response["location"] = {
                "latitude": latitude,
                "longitude": longitude
            }
        
        if user_id:
            response["user_id"] = user_id
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Water analysis failed: {str(e)}")

@router.post("/combined-analysis")
async def combined_environmental_analysis(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    analysis_type: str = Form("both"),  # "trash", "water", or "both"
    user_id: Optional[str] = Form(None)
):
    """
    Perform combined trash detection and water quality analysis with risk assessment
    """
    try:
        # Validate inputs
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if analysis_type not in ["trash", "water", "both"]:
            raise HTTPException(status_code=400, detail="Invalid analysis_type")
        
        # Process file
        contents = await file.read()
        unique_filename = f"combined_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        
        results = {
            "analysis_id": str(uuid.uuid4()),
            "location": {"latitude": latitude, "longitude": longitude},
            "analysis_type": analysis_type,
            "timestamp": "2025-08-24T10:30:00Z"
        }
        
        # Run trash detection
        if analysis_type in ["trash", "both"]:
            trash_results = trash_detector.detect_trash(contents)
            results["trash_detection"] = trash_results
        
        # Run water analysis
        if analysis_type in ["water", "both"]:
            water_results = water_analyzer.analyze_water_quality(contents, (latitude, longitude))
            results["water_quality"] = water_results
        
        # Run risk assessment if we have both analyses
        if analysis_type == "both" and results.get("trash_detection", {}).get("success"):
            risk_assessment = risk_model.assess_health_risk(
                (latitude, longitude),
                results["trash_detection"],
                results.get("water_quality")
            )
            results["risk_assessment"] = risk_assessment
            
            # Add prediction model
            predictions = risk_model.predict_trash_generation(
                (latitude, longitude),
                results["trash_detection"]
            )
            results["future_predictions"] = predictions
        
        # Calculate combined environmental cost
        if results.get("trash_detection"):
            environmental_cost = risk_model.calculate_environmental_cost(
                results["trash_detection"],
                results.get("water_quality")
            )
            results["environmental_impact"] = environmental_cost
        
        if user_id:
            results["user_id"] = user_id
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Combined analysis failed: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported file formats and limits
    """
    return {
        "supported_extensions": settings.ALLOWED_EXTENSIONS,
        "max_file_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024),
        "recommended_resolution": {
            "min": "800x600",
            "max": "4096x4096",
            "optimal": "1920x1080"
        },
        "supported_analysis_types": [
            {
                "type": "trash_detection",
                "description": "AI-powered trash identification and categorization",
                "output": "trash types, confidence scores, recycling suggestions"
            },
            {
                "type": "water_quality",
                "description": "Water contamination and quality assessment",
                "output": "water quality index, contamination types, health risks"
            },
            {
                "type": "combined_analysis", 
                "description": "Full environmental assessment with risk modeling",
                "output": "comprehensive risk assessment, disease predictions, cost analysis"
            }
        ]
    }

@router.delete("/cleanup/{filename}")
async def cleanup_uploaded_file(filename: str):
    """
    Clean up uploaded file (admin endpoint)
    """
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        
        return {"message": f"File {filename} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

@router.get("/stats")
async def get_upload_stats():
    """
    Get upload and processing statistics
    """
    try:
        upload_dir = settings.UPLOAD_DIR
        
        if not os.path.exists(upload_dir):
            return {"total_files": 0, "total_size_mb": 0}
        
        files = os.listdir(upload_dir)
        total_size = sum(
            os.path.getsize(os.path.join(upload_dir, f)) 
            for f in files if os.path.isfile(os.path.join(upload_dir, f))
        )
        
        return {
            "total_files": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_types": {
                ext: len([f for f in files if f.endswith(f'.{ext}')]) 
                for ext in settings.ALLOWED_EXTENSIONS
            },
            "average_file_size_mb": round((total_size / len(files)) / (1024 * 1024), 2) if files else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")