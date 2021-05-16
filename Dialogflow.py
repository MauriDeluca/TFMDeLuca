#!/usr/bin/python
# -*- coding: utf-8 -*-

##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Librerias
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
import google_auth_oauthlib
import requests
import json
from variables import *


##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Variables
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
try:
    apiAccess = "AIzaSyDRgzbcSIvaIimmgMsRc-Bi7JfnMeLDOjI"

except Exception as e:
    print ("Error al cargar tokens de dialogflow: ", type(e), e)

baseURL = "https://dialogflow.cloud.google.com/#/editAgent/newagent-v9vh/"
v = 20210415 # fecha en formato AAAAMMDD
APIAI_LANG = "es"

headers = {
    'Authorization': 'Bearer '+apiAccess,
    "Content-Type":"application/json; charset=utf-8"
    }


##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Funciónes
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sendQuery(texto, chat_id, idioma, nombreUsuario):
    contexto = [{
        "name": "usuario",
        "parameters": { "idioma": idioma, "nombre": nombreUsuario },
        "lifespan": 1
        }]
    payload = {
        "query": texto,
        "v": v,
        "sessionId": chat_id,
        "contexts": contexto,
        "lang": APIAI_LANG
        }

    url = baseURL+"query"

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    return r