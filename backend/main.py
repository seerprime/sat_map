from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes import upload, map_data, alerts, gamification
from utils.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Sat Map API",
    description="AI-Powered Environmental Monitoring Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(map_data.router, prefix="/api/map", tags=["Map Data"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(gamification.router, prefix="/api/game", tags=["Gamification"])

@app.get("/")
async def root():
    return {
        "message": "🛰 Sat Map API - Environmental Monitoring Platform",
        "version": "1.0.0",
        "features": [
            "AI Trash Detection",
            "Water Quality Analysis", 
            "Risk Assessment",
            "Gamification System",
            "Real-time Alerts"
        ],
        "sdgs": ["SDG 11", "SDG 6", "SDG 3"]
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "trash_detector": "operational",
            "water_quality": "operational", 
            "risk_model": "operational",
            "notification_system": "operational"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )