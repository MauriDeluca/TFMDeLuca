#!/usr/bin/python
# -*- coding: utf-8 -*-

##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Librerias
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
import json

from variables import *
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Variables
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# try:
#     WebHook_URL = WebHook_URL
# except Exception as e:
#     print time.strftime("%c"), "- Error al cargar la URL del WebHook: ", type(e), e


def buscarRespuestaWH(r):

    res = requests.post(WebHook_URL, data=json.dumps(r))

    return res
