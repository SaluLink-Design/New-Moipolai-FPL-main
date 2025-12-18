"""
OCR Service - Extract FPL team information from screenshots
"""
import logging
from typing import List, Tuple, Optional
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import io

from config import settings
from models.fpl_models import OCRResult, FPLPlayer
from services.fpl_api import fpl_client

logger = logging.getLogger(__name__)


class OCRService:
    """Service for extracting team information from screenshots using OCR."""
    
    def __init__(self):
        self.engine = settings.ocr_engine
        self.confidence_threshold = settings.ocr_confidence_threshold
        self.reader = None
        
        # Initialize OCR engine
        if self.engine == "easyocr":
            self._init_easyocr()
        elif self.engine == "tesseract":
            self._init_tesseract()
        else:
            raise ValueError(f"Unknown OCR engine: {self.engine}")
    
    def _init_easyocr(self):
        """Initialize EasyOCR reader."""
        try:
            import easyocr
            languages = settings.ocr_languages.split(",")
            self.reader = easyocr.Reader(languages, gpu=False)
            logger.info(f"EasyOCR initialized with languages: {languages}")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            raise
    
    def _init_tesseract(self):
        """Initialize Tesseract OCR."""
        try:
            import pytesseract
            # Test if tesseract is available
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Tesseract: {e}")
            raise
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced)
        
        # Threshold
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def extract_text_easyocr(self, image: np.ndarray) -> List[Tuple[str, float]]:
        """
        Extract text using EasyOCR.
        
        Args:
            image: Input image
            
        Returns:
            List of (text, confidence) tuples
        """
        results = self.reader.readtext(image)
        
        # Filter by confidence and extract text
        extracted = []
        for bbox, text, confidence in results:
            if confidence >= self.confidence_threshold:
                extracted.append((text.strip(), confidence))
                logger.debug(f"Detected: '{text}' (confidence: {confidence:.2f})")
        
        return extracted
    
    def extract_text_tesseract(self, image: np.ndarray) -> List[Tuple[str, float]]:
        """
        Extract text using Tesseract.
        
        Args:
            image: Input image
            
        Returns:
            List of (text, confidence) tuples
        """
        import pytesseract
        from pytesseract import Output
        
        # Get detailed data
        data = pytesseract.image_to_data(image, output_type=Output.DICT)
        
        extracted = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            confidence = float(data['conf'][i])
            text = data['text'][i].strip()
            
            if confidence >= self.confidence_threshold * 100 and text:
                extracted.append((text, confidence / 100.0))
                logger.debug(f"Detected: '{text}' (confidence: {confidence:.2f})")
        
        return extracted
    
    async def process_image(self, image_bytes: bytes) -> OCRResult:
        """
        Process an FPL team screenshot and extract player names.
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            OCRResult with detected players and validation
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Preprocess
            preprocessed = self.preprocess_image(image_np)
            
            # Extract text
            if self.engine == "easyocr":
                extracted_text = self.extract_text_easyocr(preprocessed)
            else:
                extracted_text = self.extract_text_tesseract(preprocessed)
            
            logger.info(f"Extracted {len(extracted_text)} text items from image")
            
            # Filter for player names (heuristics)
            player_names = self._filter_player_names(extracted_text)
            
            # Match to FPL database
            matched_players, unmatched = await self._match_players(player_names)
            
            # Validate team
            is_valid, errors = self._validate_team(matched_players)
            
            # Detect formation
            formation = self._detect_formation(matched_players)
            
            result = OCRResult(
                success=len(matched_players) > 0,
                players_detected=[name for name, _ in player_names],
                confidence_scores=[conf for _, conf in player_names],
                matched_players=matched_players,
                unmatched_names=unmatched,
                is_valid_team=is_valid,
                validation_errors=errors,
                formation=formation
            )
            
            logger.info(f"OCR processing complete. Matched {len(matched_players)}/15 players")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return OCRResult(
                success=False,
                validation_errors=[f"Image processing failed: {str(e)}"]
            )
    
    def _filter_player_names(self, extracted_text: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Filter extracted text to likely player names.
        
        Args:
            extracted_text: List of (text, confidence) tuples
            
        Returns:
            Filtered list of likely player names
        """
        player_names = []
        
        for text, confidence in extracted_text:
            # Skip very short text
            if len(text) < 3:
                continue
            
            # Skip numbers only
            if text.isdigit():
                continue
            
            # Skip common UI elements
            skip_words = ["gameweek", "pitch", "list", "fantasy", "average", "total", "pts", 
                         "highest", "gkp", "def", "mid", "fwd"]
            if text.lower() in skip_words:
                continue
            
            # Likely a player name if it's capitalized and alphabetic
            if text[0].isupper() and any(c.isalpha() for c in text):
                player_names.append((text, confidence))
        
        return player_names
    
    async def _match_players(self, player_names: List[Tuple[str, float]]) -> Tuple[List[FPLPlayer], List[str]]:
        """
        Match extracted names to FPL database.
        
        Args:
            player_names: List of (name, confidence) tuples
            
        Returns:
            Tuple of (matched_players, unmatched_names)
        """
        matched = []
        unmatched = []
        
        for name, confidence in player_names:
            player = await fpl_client.get_player_by_name(name, fuzzy=True)
            
            if player:
                matched.append(FPLPlayer(**player))
                logger.info(f"Matched '{name}' to {player['web_name']}")
            else:
                unmatched.append(name)
                logger.warning(f"Could not match player: {name}")
        
        return matched, unmatched
    
    def _validate_team(self, players: List[FPLPlayer]) -> Tuple[bool, List[str]]:
        """
        Validate that the detected players form a valid FPL team.
        
        Args:
            players: List of matched players
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check total count
        if len(players) != 15:
            errors.append(f"Invalid team size: {len(players)} players (expected 15)")
        
        # Check position counts
        position_counts = {1: 0, 2: 0, 3: 0, 4: 0}  # GK, DEF, MID, FWD
        for player in players:
            position_counts[player.element_type] = position_counts.get(player.element_type, 0) + 1
        
        if position_counts[1] != 2:
            errors.append(f"Invalid GK count: {position_counts[1]} (expected 2)")
        if position_counts[2] != 5:
            errors.append(f"Invalid DEF count: {position_counts[2]} (expected 5)")
        if position_counts[3] != 5:
            errors.append(f"Invalid MID count: {position_counts[3]} (expected 5)")
        if position_counts[4] != 3:
            errors.append(f"Invalid FWD count: {position_counts[4]} (expected 3)")
        
        # Check max 3 players per team
        team_counts = {}
        for player in players:
            team_counts[player.team] = team_counts.get(player.team, 0) + 1
        
        for team_id, count in team_counts.items():
            if count > 3:
                errors.append(f"Too many players from team {team_id}: {count} (max 3)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _detect_formation(self, players: List[FPLPlayer]) -> Optional[str]:
        """
        Detect the formation from the starting 11.
        This is a simplified version - in reality, we'd need to detect which players are on the pitch.
        
        Args:
            players: List of matched players
            
        Returns:
            Formation string (e.g., "3-4-3") or None
        """
        # For now, just return a default formation
        # In a full implementation, we'd analyze the image layout to determine which players are starting
        return "3-4-3"


# Global OCR service instance
ocr_service = OCRService()
