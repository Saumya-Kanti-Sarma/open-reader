from kokoro_onnx import Kokoro
import struct
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

voices = {
    "af_bella":   "en-us",
    "af_sarah":   "en-us",
    "af_nicole":  "en-us",
    "af_sky":     "en-us",
    "am_adam":    "en-us",
    "am_michael": "en-us",
    "bf_emma":    "en-gb",
    "bf_isabella":"en-gb",
    "bm_george":  "en-gb",
    "bm_lewis":   "en-gb",
}

def get_kokoro():
    return Kokoro(
        os.path.join(BASE_DIR, "voice_model", "kokoro-v1.0.fp16-gpu.onnx"),
        os.path.join(BASE_DIR, "voice_model", "voices.bin")
    )

def make_wav_header(sample_rate=24000, num_channels=1, bits_per_sample=16):
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', 0xFFFFFFFF, b'WAVE', b'fmt ',
        16, 1, num_channels, sample_rate,
        byte_rate, block_align, bits_per_sample,
        b'data', 0xFFFFFFFF
    )
    return header

# async generator banana pada kyunki create_stream() async hai
async def stream_voice_chunks(text, voice="af_sarah", lang="en-us", speed=1.0):
    kokoro = get_kokoro()

    yield make_wav_header(sample_rate=24000)

    # async for — normal for nahi chalega
    async for samples, sample_rate in kokoro.create_stream(text, voice=voice, speed=speed, lang=lang):
        pcm = (samples * 32767).astype('int16')
        yield pcm.tobytes()

def get_all_voice():
    return voices