import nltk
import numpy
import numpy as np
import random
import tensorflow
import tflearn
import json
import pickle
from nltk.stem.lancaster import LancasterStemmer


nltk.download('punkt')
stemmer = LancasterStemmer()

with open("json file/intents.json") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        docs_x.append(word)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    word = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in word:
            bag.append(1)
        else:
            bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)
with open("data/data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


model.load("data/model.tflearn")
# model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
# model.save("data/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(wrd.lower()) for wrd in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


class ReturnValue:
    def __init__(self, content, tag):
        self.content = content
        self.tag = tag


def chat(inp):
    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tags = labels[results_index]
    for tag in data["intents"]:
        if tag["tag"] == tags:
            responses = tag['responses']

            return ReturnValue(random.choice(responses), tags)


print(chat("What can i call you").content)
