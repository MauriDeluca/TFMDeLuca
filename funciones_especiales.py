#Chatbot solo almacena información y tiene un flujo definido

from tkinter import *
import json
import pandas
chatbot_basico = open('chatbot_basico.json').read()
chatbot_basico_config = json.loads(chatbot_basico)
preguntas_formulario = pandas.read_csv('respuestas_formulario.csv')

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


def estado_usuario(usuario):
    #Actualiza la ubicación de conversación
    actualizar_estado = True
    if estados.index(usuario["estado"])+1 < len(estados):
        if usuario["estado"] == "siguiente_bot":
            cantidad_respuestas = 0
            cantidad_preguntas = 0
            file_object=  open("respuestas_usuarios.txt", "r")
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
    with open("respuestas_usuarios.txt", "a") as file_object:
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
        file_object=  open("respuestas_usuarios.txt", "r")
        for linea in file_object.readlines():
            if usuario["nombre"]+";siguiente_bot" in linea:
                cantidad_respuestas += 1
        pregunta = [pregunta[cantidad_respuestas]]
    elif usuario["estado"] == "decision_bot":
        pregunta = ["respuesta según algoritmo RN"]
    elif usuario["estado"] == "final":
        pregunta = chatbot_basico_config["final"]
    return pregunta[0] #puede ser random

def verificar_respuestas(usuario, msg):

    return True

def respuesta_chatbot(usuario, msg):
    #Esquema general de funcionamiento
    guardar = guardar_respuesta(usuario, msg)
    if not verificar_respuestas(usuario, msg):
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
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")  
ChatLog['yscrollcommand'] = scrollbar.set
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )
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

# file_object=  open("respuestas_usuarios.txt", "r")
# respuestas_rn = []
# for linea in file_object.readlines():
#     if usuario["nombre"]+";siguiente_bot" in linea:
#         respuestas_rn.append(linea)
# for p in chatbot_basico_config["preguntas"]:
#     if p["estado"] == "siguiente_bot":
#         print("las respuestas que se evaluan en RN son")
#         for p_ in p["pregunta"]:
#             print ("{0} -> {1}".format(p_, respuestas_rn[p["pregunta"].index(p_)]))

#Parte para entrenamiento
# print(preguntas_formulario.iloc[:5,2:-1]) #de acá se sacarán los 80/20
print(preguntas_formulario.iloc[:,3].str.lower().unique())

    

