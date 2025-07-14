from fastapi import APIRouter, File, UploadFile, HTTPException
from src.services.extractor import ExtractorService
import time
import logging

router = APIRouter(prefix="/extract", tags=["Extract"])
logger = logging.getLogger(__name__)


@router.post("/image")
async def extract_image(file: UploadFile = File(...)):
    try:
        start = time.perf_counter()
        text = await ExtractorService.image_to_text(file)
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"Extract text from image processing took={elapsed:.2f} ms")
        return {"data": text}
    except Exception as e:
        raise HTTPException(400, f"OCR failed: {e}")


@router.post("/audio")
async def extract_audio(file: UploadFile = File(...)):
    try:
        start = time.perf_counter()
        text = await ExtractorService.audio_to_text(file, language="pt")
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"Extract text from audio processing took={elapsed:.2f} ms")
        return {"data": text}
    except Exception as e:
        raise HTTPException(400, f"Transcripter failed: {e}")
