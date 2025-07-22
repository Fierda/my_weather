from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import logging

from app.models import WeatherResponse, LocationRequest
from app.services.weather import WeatherService
from app.auth import router as auth_router
from app.deps import get_current_user
from app.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Weather API",
    description="Production-grade weather service",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security (optional, not enforced in these routes)
security = HTTPBearer()

# Initialize weather service
weather_service = WeatherService()

# Routes
@app.get("/")
async def root():
    return {"message": "Weather API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "weather-api"}


@app.post("/api/weather", response_model=WeatherResponse)
async def get_weather(location: LocationRequest,current_user: User = Depends(get_current_user)):
    """Get current weather for a city (POST)"""
    return await weather_service.get_weather(location.city, location.country)


@app.get("/api/weather/{city}", response_model=WeatherResponse)
async def get_weather_by_city(city: str,current_user: User = Depends(get_current_user)):
    """Get current weather for a city (GET)"""
    return await weather_service.get_weather(city)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
