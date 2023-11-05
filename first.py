import sounddevice as sd
from scipy.io.wavfile import write
import openai

openai.api_key = "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"

fs = 44100
seconds = 3

print("録音を開始します")
recording = sd.rec(int(seconds * fs),samplerate = fs,channels= 1)
sd.wait()

write('output.wav', fs, recording)
print("録音が終了しました。")

with open('output.wav', "rb") as audio_file:

    transcript = openai.Audio.transcribe("whisper-1", audio_file)

print(transcript.text)