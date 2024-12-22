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
