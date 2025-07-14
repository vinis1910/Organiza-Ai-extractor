from io import BytesIO
import cv2, numpy as np
from faster_whisper import WhisperModel
from fastapi import UploadFile
import soundfile as sf
from paddleocr import PaddleOCR

OCR_LANG = "por"
OCR_CONFIG = "--oem 3 --psm 6"
WHISPER_MODEL = "small"


_whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
ocr = PaddleOCR(use_angle_cls=True, lang="pt", rec=False, det=True, cls=True, show_log=False)
ocr = PaddleOCR(use_angle_cls=True, lang="pt")


class ExtractorService:
    @staticmethod
    async def image_to_text(file) -> str:
        img_bytes = await file.read()
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        result = ocr.ocr(img, cls=True)
        return " ".join(text for box, (text, score) in result[0]).strip()

    @staticmethod
    async def audio_to_text(file: UploadFile, language: str = "pt") -> str:
        data = BytesIO(await file.read())
        audio, sr = sf.read(data)
        segments, info = _whisper_model.transcribe(audio, language=language)
        return " ".join(s.text for s in segments).strip()
