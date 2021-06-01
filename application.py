from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, request
import chatbot_training as service
import chatbot_voice_recognition as voice_service

app = Flask(__name__)
api = Api(app)


@app.route("/chatbot", methods=['POST'])
def chatbot_service():
    data = request.json
    content_input = data['content']
    response = service.chat(content_input)
    return {"tag": response.tag, "content": response.content}


@app.route("/chatbot/voice", methods=['POST'])
def chatbot_voice_service():
    data = request.json
    content_input = data['content']
    response = voice_service.voice_recognition("audio/" + content_input)
    return {"tag": "voice", "content": response}


@app.route("/")
def greetings():
    return {"Content": "Hello"}


if __name__ == "__main__":
    app.run(debug=True)


# print(chatbot_service())

