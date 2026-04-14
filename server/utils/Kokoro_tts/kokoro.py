from kokoro_onnx import Kokoro
import soundfile as sf
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

voices = {
    # Female - American
    "af_bella":   "en-us",
    "af_sarah":   "en-us",
    "af_nicole":  "en-us",
    "af_sky":     "en-us",
    # Male - American
    "am_adam":    "en-us",
    "am_michael": "en-us",
    # Female - British
    "bf_emma":    "en-gb",
    "bf_isabella":"en-gb",
    # Male - British
    "bm_george":  "en-gb",
    "bm_lewis":   "en-gb",
}

def make_voice_file(text, voice="af_sarah", lang="en-us", speed=1.0):
    try:
        output_dir = os.path.join( "temp_voice")
        os.makedirs(output_dir, exist_ok=True)

        kokoro = Kokoro(
            os.path.join( BASE_DIR, "voice_model", "kokoro-v1.0.fp16-gpu.onnx"),
            os.path.join( BASE_DIR, "voice_model", "voices.bin")
        )

        file_name = str(int(time.time())) + ".wav"
        output_path = os.path.join(output_dir, file_name)

        voice_binary, rate = kokoro.create(text, voice=voice, speed=speed, lang=lang)
        sf.write(output_path, voice_binary, rate)

        return output_path

    except Exception as e:
        print(f"Error generating voice at utils/Kokoro_tts/kokoro.py: {e}")
        return str(e)

def get_all_voice():
    return voices

if __name__ == "__main__":
    result = make_voice_file(text="Welcome to open reader. An Open source text to speech software created by Saumya Sarma.")
    print(f"Result: {result}")
    print(f"Files in temp_voice: {os.listdir(os.path.join( 'temp_voice'))}")