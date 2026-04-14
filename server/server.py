from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from utils.Kokoro_tts.kokoro import stream_voice_chunks, get_all_voice

BASE_DIR = Path(__file__).resolve().parent

class Text(BaseModel):
    data: str
    voice: str = "af_sarah"
    speed: float = 1.0

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to open reader. Created by Saumya Sarma",
        "github": "https://github/Saumya-Kanti-Sarma/open-reader",
        "created_on": "13-4-2026"
    }

@app.get("/voices")
def list_voices():
    return get_all_voice()

# ✅ endpoint bhi async hona chahiye
@app.post("/get-voice")
async def get_voice(text: Text):
    try:
        generator = stream_voice_chunks(
            text=text.data,
            voice=text.voice,
            speed=text.speed
        )
        return StreamingResponse(
            generator,
            media_type="audio/wav",
            headers={"Cache-Control": "no-cache"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))