from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import torch
import torchaudio
import numpy as np
import os
import logging
import scipy
from transformers import pipeline
from audiocraft.models import MusicGen

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text-to-Music Generator API")

# Enable CORS (for dev, allow all; for prod, restrict origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sentiment pipeline (prompt enrichment)
try:
    logger.info("Loading sentiment analysis pipeline...")
    nlp = pipeline("sentiment-analysis")
    logger.info("Sentiment model loaded.")
except Exception as e:
    logger.error(f"Failed to load sentiment model: {e}")
    raise RuntimeError("Sentiment model failed to load.")

# Load MusicGen model
try:
    logger.info("Loading MusicGen model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    logger.info("MusicGen model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load MusicGen model: {e}")
    raise RuntimeError("MusicGen model failed to load.")

# Request model
class MusicRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Text prompt for music generation")
    duration: int = Field(default=10, ge=1, le=30, description="Duration of generated music (in seconds)")

@app.get("/api")
async def root():
    return {"message": "🎵 Welcome to the Text-to-Music Generator API"}

# 🔁 Updated route here
@app.post("/generate_music")
async def generate_music(request: MusicRequest):
    try:
        logger.info(f"Received prompt: {request.prompt} | Duration: {request.duration}")

        # Enrich prompt
        sentiment = nlp(request.prompt)[0]
        mood = sentiment["label"].lower()
        enhanced_prompt = f"{mood} {request.prompt}"
        logger.info(f"Enhanced prompt: {enhanced_prompt}")

        # Generate audio
        model.set_generation_params(duration=request.duration)
        wav = model.generate([enhanced_prompt])[0].cpu().numpy()

        # Save as .wav
        output_path = "generated_music.wav"
        scipy.io.wavfile.write(output_path, rate=32000, data=wav.T)
        logger.info("Music generated and saved.")

        return {
            "prompt": request.prompt,
            "mood": mood,
            "duration": request.duration,
            "audio_url": "/api/download-music"  # 🔁 Updated download route
        }

    except Exception as e:
        logger.error(f"Error during music generation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during music generation.")

# 🔁 Updated download route
@app.get("/api/download-music")
async def download_music():
    output_path = "generated_music.wav"
    if os.path.exists(output_path):
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="generated_music.wav"
        )
    else:
        logger.warning("Requested download but file was not found.")
        raise HTTPException(status_code=404, detail="Music file not found.")
