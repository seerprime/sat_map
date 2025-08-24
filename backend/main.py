from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
from routes import upload, map_data, alerts, gamification
from utils.config import settings

# Base directories
BASE_DIR = Path(__file__).parent.parent  # Repo root
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = Path(__file__).parent / "static"

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

# Mount backend static folder (optional)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"⚠️ Static folder not found at: {STATIC_DIR}")

# Mount frontend folder at root for SPA + static assets
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="index.html")
else:
    print(f"⚠️ Frontend folder not found at: {FRONTEND_DIR}")

# Include API routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(map_data.router, prefix="/api/map", tags=["Map Data"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(gamification.router, prefix="/api/game", tags=["Gamification"])

# API Root endpoint
@app.get("/api")
async def api_root():
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
