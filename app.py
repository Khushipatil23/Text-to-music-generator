from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
import torchaudio
import numpy as np
import os
import time
import scipy
from audiocraft.models import MusicGen

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load the MusicGen model
try:
    print("Loading MusicGen model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    print("Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to load MusicGen model: {e}")

# Define input request model
class MusicRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Welcome to the MusicGen Text-to-Music API!"}

@app.post("/generate_music")
def generate_music(request: MusicRequest):
    try:
        print(f"Generating music for prompt: {request.prompt}")

        # 🎵 Generate music using MusicGen
        model.set_generation_params(duration=10)  # Adjust duration as needed
        wav = model.generate([request.prompt])  # Generate audio
        wav = wav[0].cpu().numpy()  # Convert to NumPy array

        # 💾 Save generated music
        output_path = "generated_music.wav"
        scipy.io.wavfile.write(output_path, rate=32000, data=wav.T)

        # ✅ Ensure the file exists before returning response
        time.sleep(2)  # Small delay to ensure file is written
        if os.path.exists(output_path):
            return {"audio_url": "http://127.0.0.1:8000/download-music"}
        else:
            raise HTTPException(status_code=500, detail="Music file not generated properly")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating music: {e}")

# ✅ Serve the generated music file
@app.get("/download-music")
def download_music():
    if os.path.exists("generated_music.wav"):
        return FileResponse("generated_music.wav", media_type="audio/wav", filename="generated_music.wav")
    else:
        raise HTTPException(status_code=404, detail="Music file not found")
