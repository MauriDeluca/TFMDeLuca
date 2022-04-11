from unittest import result
import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model

#Creacion GUI con tkinter
from tkinter import *
import json
import pandas
chatbot_basico = open('chatbot_basico.json').read()
chatbot_basico_config = json.loads(chatbot_basico)
preguntas_formulario = pandas.read_csv('Formvacacionesconetiquetas.csv')

#Se salta las columnas que son ["Marca temporal","Segmento edad","destinos de Argentina elegirias"]
for pregunta in preguntas_formulario.columns[2:-1]:
    for p in chatbot_basico_config["preguntas"]:
        if p["estado"] == "siguiente_bot":
            p["pregunta"].append(pregunta)
#inicializa al usuario
usuario = {
    "nombre":'no_name',
    "edad":0,
    "genero":'sin_genero',
    "estado":'no_estado'

}
#Inicializa los estados
estados = []
for e in chatbot_basico_config["preguntas"]:
    estados.append(e["estado"])

archivo_txt = 'respuestas_usuarios_IA.txt'

#Carga de IA español
model = load_model('chatbot_model_esp8.h5')

#Eleccion de archivo de intents
# intents = json.loads(open('intentsesp.json').read())
intents = json.loads(open('intents_esp_auto_3.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

token_esp = nltk.data.load('tokenizers/punkt/spanish.pickle')
# preprocessamento input resUsuario
def clean_up_sentence(sentence):
    # sentence_words = nltk.word_tokenize(sentence)
    sentence_words = token_esp.tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# creacion bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def calculo_prediccion(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.20 # 0.40
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # ordenar por mayor probabilidad
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def obtenerRespuesta(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['patterns'])
            break
    return result


def estado_usuario(usuario):
    #Actualiza la ubicación de conversación
    actualizar_estado = True
    if estados.index(usuario["estado"])+1 < len(estados):
        if usuario["estado"] == "siguiente_bot":
            cantidad_respuestas = 0
            cantidad_preguntas = 0
            file_object=  open(archivo_txt, "r")
            for linea in file_object.readlines():
                if usuario["nombre"]+";siguiente_bot" in linea:
                    cantidad_respuestas += 1
            for p in chatbot_basico_config["preguntas"]:
                if p["estado"] == "siguiente_bot":
                    cantidad_preguntas = len(p["pregunta"])
            if cantidad_respuestas != cantidad_preguntas:
                actualizar_estado = False
        if actualizar_estado:
            usuario["estado"] = estados[estados.index(usuario["estado"])+1]
    else:
        usuario["estado"] = 'final'
    return usuario

def guardar_respuesta(usuario, msg):
    #Almacena la respuesta en un archivo
    with open(archivo_txt, "a") as file_object:
        file_object.write(usuario["nombre"]+";"+usuario["estado"]+";"+msg+"\n")
    if usuario["estado"] in usuario:
        usuario[usuario["estado"]]=msg
    return 'guardado'

def hacer_pregunta(usuario):
    #Busca la pregunta según el estado
    pregunta = chatbot_basico_config["sin_respuesta"]
    for p in chatbot_basico_config["preguntas"]:
        if p["estado"]==usuario["estado"]:
            pregunta = p["pregunta"]
    if usuario["estado"] == "siguiente_bot":
        cantidad_respuestas = 0
        file_object=  open(archivo_txt, "r")
        for linea in file_object.readlines():
            if usuario["nombre"]+";siguiente_bot" in linea:
                cantidad_respuestas += 1
        pregunta = [pregunta[cantidad_respuestas]]
    elif usuario["estado"] == "decision_bot":
        respuestas_rn = []
        file_object=  open(archivo_txt, "r")
        for linea in file_object.readlines():
            if usuario["nombre"]+";siguiente_bot" in linea:
                respuestas_rn.append(linea.split(";")[-1].replace('\n',''))
        print(respuestas_rn)
        # predict(respuestas_rn) -> solucion de RN básico con las respuestas encontradas
        pregunta = ["respuesta según algoritmo RN se imprimen las respuestas del usuario {0}".format(usuario["nombre"])]
    elif usuario["estado"] == "final":
        pregunta = chatbot_basico_config["final"]
    return pregunta[0] #luego podria ser random

def verificar_respuestas(usuario, msg):

    if usuario["estado"] == 'siguiente_bot':
        ints = calculo_prediccion(msg, model)
        if len(ints)==0:
            return False
        print(ints)
        res = obtenerRespuesta(ints, intents)
        print (res)
    return True

def respuesta_chatbot(usuario, msg):
    #Esquema general de funcionamiento
    guardar = guardar_respuesta(usuario, msg)
    if not verificar_respuestas(usuario, msg):
        #antes de regresar la frase sin respuesta elimina la última respuesta guardada
        return chatbot_basico_config["sin_respuesta"][0] #puede ser random
    if usuario["estado"] == 'no_estado':
        usuario["estado"] = chatbot_basico_config["preguntas"][0]["estado"]
        pregunta = chatbot_basico_config["preguntas"][0]["pregunta"][0]
        
    elif usuario["estado"] == 'final':
        pregunta = chatbot_basico_config["final"][0] 
    else:
        estado_usuario(usuario)
        pregunta = hacer_pregunta(usuario)
    return pregunta

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()   
    EntryBox.delete("0.0",END)   
    if msg != '':   
        ChatLog.config(state=NORMAL)   
        ChatLog.insert(END, "You: " + msg + '\n\n')   
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))   
        res = respuesta_chatbot(usuario, msg) 
        ChatLog.insert(END, "Bot: " + res + '\n\n')   
        ChatLog.config(state=DISABLED)   
        ChatLog.yview(END)

#Interfaz gráfica
base = Tk()  
base.title("Recomendador destinos turisticos")
base.geometry("400x500")  
base.resizable(width=FALSE, height=FALSE) 
#Chat window
ChatLog = Text(base, bd=0, bg="white", height="10", width="60", font="Arial",)
ChatLog.config(state=DISABLED)
#scrollbar
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")  
ChatLog['yscrollcommand'] = scrollbar.set  
#Create Button send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )
#Create box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", send)
scrollbar.place(x=376,y=6, height=386)  
ChatLog.place(x=6,y=6, height=386, width=370)  
EntryBox.place(x=128, y=401, height=90, width=265)  
SendButton.place(x=6, y=401, height=90)
# pregunta_inicial = hacer_pregunta(usuario)
# ChatLog.insert(END, "Bot: " + pregunta_inicial + '\n\n') 
base.mainloop()
print("las caracteristicas del usuario son:")
print(usuario)
