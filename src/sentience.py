'''
Copyright (C) 2025  Avalyn Baldyga
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import tensorflow as tf
import numpy as np
import json
import config
import random

data = json.load(open('words.json', 'r'))
words = data["words"]

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(len(words), 64),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Conv1D(64, 10, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=4),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(512, activation='sigmoid'),
        tf.keras.layers.Dense(len(words), activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model(tf.keras.Input((256,)))
    return model

def tokenize(message) -> list[int]:
    message = message.lower()
    message = message.replace(":3", "colonthree")
    message = filter(lambda x: x.isalpha() or x.isspace(), message)
    message = ''.join(message).split()
    mc = []
    for x in message:
        try:
            mc.append(words.index(x)+1)
        except:
            pass
    message = mc
    message.append(22692)
    return message
def detokenize(message) -> str:
    message = ' '.join([words[x-1] for x in message[:-1]])
    for naughty in config.bad_words:
        if naughty in message:
            return "I almost said something naughty :3"
    message = message.replace("france", "fr*nce")
    message = message.replace("frnce", "fr*nce")
    message = message.replace("french", "fr*nch")
    message = message.replace("frnch", "fr*nch")
    message = message.replace("colonthree", ":3")
    return message
def token_to_array(token):
    array = np.zeros(len(words))
    array[token] = 1
    return array
def tokens_to_array(message):
    array = np.zeros((256, len(words)))
    for i, token in enumerate(message):
        array[i] = token_to_array(token)
    return array
pad = lambda x: np.pad(np.array(x), (0,256 - len(x)))
def train(model, message, response):
    if not message:
        return
    if not response:
        return
    message = tokenize(message)
    message.extend(tokenize(response))
    xdata = np.zeros((len(message), 256))
    ydata = np.zeros((len(message), len(words)))
    current = []
    for i,x in enumerate(message):
        ydata[i] = token_to_array(x)
        xdata[i] = pad(current)
        current.append(x)
    model.fit(xdata, ydata, batch_size=len(message), epochs=1)
def predict(model, message):
    message = tokenize(message)
    op = []
    for _ in range(64 - len(message)):
        padded = pad(message)
        two = np.zeros((1,256))
        two[0] = padded
        output = model.predict_on_batch(two)[0]
        while True:
            max = output.argmax()
            if random.randint(0,1) and not (max == 22692 or ((op[-1] == max) if op else False)):
                break
            else:
                output[max] = -np.inf
        op.append(max)
        print(max)
        if max == 22692:
            break
        message.append(max)
    return detokenize(op)

if __name__ == '__main__':
    model = create_model()
    train(model, "i like penis", "me too bestie")
