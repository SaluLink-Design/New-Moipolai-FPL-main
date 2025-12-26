"""
FPL AI Model - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from config import settings
from api.routes import predictions, transfers, teams, ocr
from services.data_cache import cache_manager
from services.fpl_api import fpl_client
from services.supabase_client import supabase_service

# Create necessary directories before logging setup
Path("logs").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)
Path(settings.model_path).mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.log_file) if settings.log_file else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting FPL AI Model API...")
    
    # Create necessary directories
    Path(settings.model_path).mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    
    # Initialize services
    await cache_manager.connect()
    await fpl_client.initialize()
    await supabase_service.connect()

    logger.info("FPL AI Model API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FPL AI Model API...")
    await cache_manager.disconnect()
    await fpl_client.close()
    await supabase_service.disconnect()
    logger.info("FPL AI Model API shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="FPL AI Model API",
    description="Intelligent Fantasy Premier League prediction and recommendation engine",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware - with support for wildcard domains
cors_origins = settings.cors_origins_list

# If any origin contains wildcard, use allow_origin_regex instead
has_wildcard = any("*" in origin for origin in cors_origins)
if has_wildcard:
    # Remove wildcard origins from list and convert to regex
    static_origins = [o for o in cors_origins if "*" not in o]
    # Build regex pattern for wildcard domains
    pattern = r"https://.*\.fly\.dev"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=static_origins,
        allow_origin_regex=pattern,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "service": "FPL AI Model API",
        "version": "1.0.0",
        "environment": settings.env
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "api": "up",
            # "database": "up" if await check_database() else "down",
            # "redis": "up" if await cache_manager.ping() else "down",
            # "fpl_api": "up" if await fpl_client.check_health() else "down",
        }
    }


# Include routers
from api.routes import fpl

app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(transfers.router, prefix="/api/transfers", tags=["Transfers"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCR"])
app.include_router(fpl.router, prefix="/api/fpl", tags=["FPL Data"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
