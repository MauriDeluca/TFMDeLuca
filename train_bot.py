import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

import json
import pickle

import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, LSTM, Embedding
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
words = []
classes = []
documents = []
ignore_words = ['?', '!']
# data_file = open('intentsesp.json').read()
data_file = open('intents_esp_auto_3.json').read()
intents = json.loads(data_file)

# intents
# patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # print(pattern)
        if str(pattern).lower() == 'nan':
            continue
        # tokenizacion
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # agregacion de los documentos
        documents.append((w, intent['tag']))

        # agrega clases a nuestra lista
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))

# preparacion para el entrenamiento de la red
training = []
output_empty = [0] * len(classes)
for doc in documents:
    # bag of words
    bag = []
    # lista de tokens
    pattern_words = doc[0]
    # lemmatizacion del token
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # si la palabra matchea, ingreso 1, sino 0
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

training = np.array(training)
# creacion del set de train y de test: X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

# Modelo
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

#Modelo con LSTM
#model = Sequential()
#model.add(Embedding(len(classes), len(train_y[0]), input_length=len(train_x[0])))
#model.add(LSTM(45))
#model.add(Dropout(0.3))
#model.add(Dense(len(classes), activation='sigmoid'))


sgd = SGD(lr=0.01, decay=1e-6, momentum=0.7, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
# loss
# mse
# categorical_crossentropy
# kullback_leibler_divergence
# entrena y guarda el modelo
hist = model.fit(np.array(train_x), np.array(train_y), epochs=150, batch_size=5, verbose=1)
model.save('chatbot_model_esp14.h5', hist)
model.summary()
#test_loss, test_acc = model.evaluate(test_x, test_y)
#print('Test accuracy:', test_acc)
print("model created")

# activation signal
# relu function
# sigmoid function
# softmax function
# softplus function
# softsign function
# tanh function
# selu function
# elu function
# exponential function
