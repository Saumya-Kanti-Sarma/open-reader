from kokoro_onnx import Kokoro
import soundfile as sf
import os

# All available English voices
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

speech = "Richard Phillips Feynman; May 11, 1918 – February 15, 1988, was an American theoretical physicist. He shared the 1965 Nobel Prize in Physics with Julian Schwinger and Shin'ichiro Tomonaga for their fundamental work in quantum electrodynamics with deep consequences for the physics of elementary particles."

# Output folder
os.makedirs("voice_samples", exist_ok=True)

kokoro = Kokoro("kokoro-v1.0.fp16-gpu.onnx", "voices.bin")

for voice, lang in voices.items():
    print(f"Generating: {voice} ({lang})...")
    try:
        samples, sample_rate = kokoro.create(speech, voice=voice, speed=1.0, lang=lang)
        output_path = f"voice_samples/{voice}.wav"
        sf.write(output_path, samples, sample_rate)
        print(f"  ✅ Saved: {output_path}")
    except Exception as e:
        print(f"  ❌ Failed {voice}: {e}")

print("\nDone! All samples saved in /voice_samples folder.")