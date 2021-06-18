import json

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
from pydub import AudioSegment

SetLogLevel(0)

if not os.path.exists("voice/model"):
    print("'model' not available.")
    exit(1)


model = Model("voice/model")


def vosk_recognition(file):
    stereo_audio = AudioSegment.from_file(file, format="wav")
    mono_audios = stereo_audio.split_to_mono();
    mono_left = mono_audios[0].export("voice/output/temp.wav", format="wav")
    wf = wave.open(mono_left, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            continue
        else:
            continue

    res = json.loads(rec.Result())
    return res['text']


print(vosk_recognition("voice/audio/test.wav"))