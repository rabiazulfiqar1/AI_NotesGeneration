from transformers import pipeline

asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small.en",
    return_timestamps=True,
    chunk_length_s=30
)

audio_path = "How to Learn Programming Languages in 1 Day (using Google).wav"

result = asr(audio_path)

for chunk in result["chunks"]:
    print(chunk["timestamp"], ":", chunk["text"])
