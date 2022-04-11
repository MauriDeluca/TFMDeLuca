from unittest import result
import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split

#Creating GUI with tkinter
from tkinter import *
import json
import pandas
chatbot_basico = open('chatbot_basico.json').read()
chatbot_basico_config = json.loads(chatbot_basico)
preguntas_formulario = pandas.read_csv('Formulario1.csv', encoding ='latin1')

#se salta las columnas que son ["Marca temporal","Segmento edad","destinos de Argentina elegirias"]
for pregunta in preguntas_formulario.columns[2:-1]:
    for p in chatbot_basico_config["preguntas"]:
        if p["estado"] == "siguiente_bot":
            p["pregunta"].append(pregunta)
#inicializa al usuario para mantenerlo en memoria al ser global
usuario = {
    "nombre":'no_name',
    "edad":0,
    "genero":'sin_genero',
    "estado":'no_estado'

}
#Inicializa los estados que existen
estados = []
for e in chatbot_basico_config["preguntas"]:
    estados.append(e["estado"])

archivo_txt = 'respuestas_usuarios_IA.txt'

#Carga de modelo español
model = load_model('chatbot_model_esp14.h5')

#Eleccion de archivo de intents
# intents = json.loads(open('intentsesp.json').read())
intents = json.loads(open('intents_esp_auto_3.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

token_esp = nltk.data.load('tokenizers/punkt/spanish.pickle')

#decision_bot2
n_features = len(preguntas_formulario.columns[2:-1])
y_index = {}
posicion = 0
for destino in preguntas_formulario.iloc[:,-1].str.lower().unique():
    y_index[destino]=posicion
    posicion += 1
x_index = {}
posicion = 0
# for respuesta in preguntas_formulario.iloc[:,3].str.lower().unique():
#     x_index[respuesta]=posicion
#     posicion += 1
inicio = 2
final = len(preguntas_formulario.columns[:])-1
data_set = {}
for n in range(preguntas_formulario.shape[0]):
    data_set[n]=[]
while True:
    index_ = 0
    for respuesta in preguntas_formulario.iloc[:,inicio].str.lower().unique():
        x_index[respuesta]=posicion
        posicion += 1
    for x_ in preguntas_formulario.iloc[:,inicio]:
        data_set[index_].append(x_index[x_.lower()])
        index_ += 1
    inicio += 1
    if inicio == final:
        break
train_x = []
for key, values in data_set.items():
    train_x.append(values)
train_y = []
for res in preguntas_formulario.iloc[:,-1].str.lower():
    train_y.append(y_index[res.lower()])

X = train_x 
Y = train_y
 
# Separa el dataset en 80% training y 20% testing.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.20, random_state=0)

cambio_algoritmo = True # True Decision Tree ; False KNN

Model_Decicion_BOT = ""

if cambio_algoritmo:
    #Decision Tree Model
    from sklearn.tree import DecisionTreeRegressor
    Model_Decicion_BOT = DecisionTreeRegressor(max_depth=5).fit(X_train,Y_train)
    # model_predict = DT_model.predict(X_test)
else:
    #KNN Model
    from sklearn.neighbors import KNeighborsRegressor
    Model_Decicion_BOT = KNeighborsRegressor(n_neighbors=3).fit(X_train,Y_train)
    # model_predict = KNN_model.predict(X_test)
def respuestas_decision_bot(list_respuestas):

    convetir_lista = []
    
    for res in list_respuestas:
        for key, values in x_index.items():
            if res in key:
                convetir_lista.append(int(values))
                break
    while(True):
        if len(list_respuestas) != len(convetir_lista):
            convetir_lista.append(random.choice(convetir_lista))
        else:
            break
    convetir_lista = np.array(convetir_lista).reshape(1, -1)

    res_DB = Model_Decicion_BOT.predict(convetir_lista)
    print(res_DB)
    destino_rn = ""
    for key, values in y_index.items():
        if values == round(res_DB[0]):
            destino_rn = key
            break
    return ["{0}, Según tus respuestas te recomiendo {1}".format(usuario["nombre"], destino_rn)]

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
    ERROR_THRESHOLD = 0.001 # umbral
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # ordena por mayor probabilidad
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
    #Almacena la respuesta en un archivo, podria ser en BBDD
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
        pregunta = [pregunta[cantidad_respuestas]] #debe ser random por ahora es igual cantidad respuestas
    elif usuario["estado"] == "decision_bot":
        respuestas_rn = []
        file_object=  open(archivo_txt, "r")
        for linea in file_object.readlines():
            if usuario["nombre"]+";siguiente_bot" in linea:
                respuestas_rn.append(linea.split(";")[-1].replace('\n',''))
        pregunta = respuestas_decision_bot(respuestas_rn)
        # predict(respuestas_rn) -> solucion de RN básico con las respuestas encontradas
    elif usuario["estado"] == "final":
        pregunta = chatbot_basico_config["final"]
    return pregunta[0] #mejora podria ser random

def verificar_respuestas(usuario, msg):

    if usuario["estado"] == 'siguiente_bot':
        ints = calculo_prediccion(msg, model)
        if len(ints)==0:
            return False
        print(ints)
        res = obtenerRespuesta(ints, intents)
        print (res) #esto debe reemplazar la última respuesta guardada
    return True

def respuesta_chatbot(usuario, msg):
    #Esquema general de funcionamiento
    guardar = guardar_respuesta(usuario, msg)
    if not verificar_respuestas(usuario, msg):
        #antes de retornar la frase sin respuesta se debe eliminar la última respuesta guardada
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
base.title("Chatbot turismo")
base.geometry("400x500")  
base.resizable(width=FALSE, height=FALSE) 
#Crea ventana de chat
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
#Barra de desplazamiento
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")  
ChatLog['yscrollcommand'] = scrollbar.set  
#Crea boton para enviar mensaje
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )
#Crea caja para ingresar mensaje
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", send)  #Pone todos los componentes en la pantalla
scrollbar.place(x=376,y=6, height=386)  
ChatLog.place(x=6,y=6, height=386, width=370)  
EntryBox.place(x=128, y=401, height=90, width=265)  
SendButton.place(x=6, y=401, height=90)
# pregunta_inicial = hacer_pregunta(usuario)
# ChatLog.insert(END, "Bot: " + pregunta_inicial + '\n\n') 
base.mainloop()
print("las caracteristicas del usuario son:")
print(usuario)