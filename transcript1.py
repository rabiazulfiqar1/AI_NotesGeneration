import librosa
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en")

# Load audio and ensure 16kHz
audio_path = "How to Learn Programming Languages in 1 Day (using Google).wav"
speech_array, sr = librosa.load(audio_path, sr=16000)
speech_array = torch.from_numpy(speech_array)

# Parameters
chunk_size = 30 * 16000  # 30 seconds per chunk
num_chunks = (len(speech_array) + chunk_size - 1) // chunk_size

full_transcript = []

for i in range(num_chunks):
    start = i * chunk_size
    end = min((i+1) * chunk_size, len(speech_array))
    chunk = speech_array[start:end]

    inputs = processor(chunk, sampling_rate=16000, return_tensors="pt")
    predicted_ids = model.generate(inputs["input_features"])
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    full_transcript.append(transcription[0])

# Join all chunks
final_transcript = " ".join(full_transcript)
print(final_transcript)
