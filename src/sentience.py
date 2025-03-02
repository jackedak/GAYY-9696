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
import json

data = json.load(open('words.json', 'r'))
words = data["words"]

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(len(words), 64, input_length=15),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Conv1D(64, 5, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=4),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(len(words), activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
model = create_model()
print(model.summary())
print(f"Vocab size: {len(words)}")

def tokenize(message):
    message = message.lower()
    message = filter(lambda x: x.isalpha() or x.isspace(), message)
    message = ''.join(message).split()
    message = [words.index(x) for x in message]
    return message
