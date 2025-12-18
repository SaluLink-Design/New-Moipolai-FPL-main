"""
OCR API Routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging

from services.ocr_service import ocr_service
from models.fpl_models import OCRResult

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=OCRResult)
async def upload_team_image(file: UploadFile = File(...)):
    """
    Upload and process FPL team screenshot.
    
    Args:
        file: Image file upload
        
    Returns:
        OCR result with detected players
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    # Validate file size (10MB max)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10MB"
        )
    
    try:
        logger.info(f"Processing uploaded image: {file.filename}")
        result = await ocr_service.process_image(contents)
        
        if not result.success:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Failed to process image",
                    "errors": result.validation_errors
                }
            )
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/validate")
async def validate_team(team_data: dict):
    """
    Validate a manually entered or corrected team.
    
    Args:
        team_data: Team data to validate
        
    Returns:
        Validation result
    """
    # TODO: Implement team validation logic
    return JSONResponse(
        content={
            "valid": True,
            "message": "Team validation not yet implemented"
        }
    )
