import speech_recognition as sr

r = sr.Recognizer()


def voice_recognition(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sphinx could not understand voice")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))