from flask import Flask
from flask_restful import Api, request
import chatbot_training as service
import vosk_recognition as vosk_service
import voice_recognition as google_service

app = Flask(__name__)
api = Api(app)


@app.route("/chatbot", methods=['POST'])
def chatbot_service():
    data = request.json
    content_input = data['content']
    response = service.chat(content_input)
    return {"tag": response.tag, "content": response.content}


@app.route("/chatbot/voice", methods=['POST'])
def voice_service():
    data = request.json
    content_input = data['content']
    response = google_service.voice_recognition("voice/voice/" + content_input)
    # response = vosk_service.vosk_recognition("voice/voice/" + content_input)
    return {"tag": "voice", "content": response}


@app.route("/")
def greetings():
    return {"Content": "Hello"}


if __name__ == "__main__":
    app.run(debug=True)


# print(chatbot_service())

