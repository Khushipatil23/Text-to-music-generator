from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
import torchaudio
import numpy as np
import os
import time
import scipy
from transformers import pipeline
from audiocraft.models import MusicGen

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Sentiment Model (for prompt enrichment)
nlp = pipeline("sentiment-analysis")

# Load MusicGen model
try:
    print("Loading MusicGen model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    print("Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to load MusicGen model: {e}")

# Request model
class MusicRequest(BaseModel):
    prompt: str
    duration: int = 10  # Default to 10 seconds

@app.get("/")
def home():
    return {"message": "🎶 Welcome to the Enhanced MusicGen Text-to-Music API!"}

@app.post("/generate_music")
def generate_music(request: MusicRequest):
    try:
        print(f"Original prompt: {request.prompt}")

        # Analyze mood from prompt
        sentiment = nlp(request.prompt)[0]
        mood = sentiment["label"].lower()
        enhanced_prompt = f"{mood} {request.prompt}"
        print(f"Enhanced prompt: {enhanced_prompt}")

        # Generate music
        model.set_generation_params(duration=request.duration)
        wav = model.generate([enhanced_prompt])[0].cpu().numpy()

        # Save audio
        output_path = "generated_music.wav"
        scipy.io.wavfile.write(output_path, rate=32000, data=wav.T)

        time.sleep(1)
        if os.path.exists(output_path):
            return {
                "prompt": request.prompt,
                "mood": mood,
                "duration": request.duration,
                "audio_url": "http://127.0.0.1:8000/download-music"
            }
        else:
            raise HTTPException(status_code=500, detail="Music file not saved")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.get("/download-music")
def download_music():
    if os.path.exists("generated_music.wav"):
        return FileResponse("generated_music.wav", media_type="audio/wav", filename="generated_music.wav")
    else:
        raise HTTPException(status_code=404, detail="File not found")
