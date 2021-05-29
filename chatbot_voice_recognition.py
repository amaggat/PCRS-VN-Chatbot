import speech_recognition as sr

r = sr.Recognizer()


def voice_recognition(audio_file):
    with sr.AudioFile("audio/" + audio_file) as source:
        audio = r.record(source)

        try:
            text = r.recognize_google(audio)
            return text
        except:
            return "Fail"


