from unittest import result
import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('chatbot_model_esp.h5')
# intents = json.loads(open('intentsesp.json').read())
intents = json.loads(open('intents_esp_auto.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

# import funciones_especiales
token_esp = nltk.data.load('tokenizers/punkt/spanish.pickle')

def clean_up_sentence(sentence):
    # sentence_words = nltk.word_tokenize(sentence)
    sentence_words = token_esp.tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    print (sentence_words)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    print (bag)
    return(np.array(bag))

def calcola_pred(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.1
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getRisposta(ints, intents_json):
    if len(ints)<1:
        return "no puedo responder"
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            # result = random.choice(i['responses'])
            result = random.choice(i['patterns'])
            break
    return result

def inizia(msg):
    ints = calcola_pred(msg, model)
    print(ints)
    res = getRisposta(ints, intents)
    return res

resUsuario = ''
print('Esto es una Interfaz para un chatbot, si quieres salir escribe "adios chatbot"')

usuario = {
    "nombre":'no_name',
    "edad":0,
    "genero":'sin_genero',
    "estado":'inicio'

}
while resUsuario != 'adios chatbot':
    resUsuario = str(input(""))
    res = inizia(resUsuario)
    print('AI:' + res)