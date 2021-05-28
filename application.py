from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, request
import main as service

app = Flask(__name__)
api = Api(app)


@app.route("/chatbot", methods=['POST'])
def chatbot_service():
    data = request.json
    content_input = data['content']
    response = service.chat(content_input)
    return {"tag": response.tag, "content": response.content}


@app.route("/")
def greetings():
    return {"Content": "Hello"}


if __name__ == "__main__":
    app.run(debug=True)


# print(chatbot_service())

