#!/usr/bin/python
# -*- coding: utf-8 -*-


##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Librerias
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
import telepot #Framework para Telegram Bot API
from funciones import *
from textos import *

##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Funciónes
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def idiomaCast(bot, query_id, idUsuario, query_data):
    # Actualizar los datos de idioma
    resultado = actualizarIdioma(idUsuario, query_data)

    if resultado == True:
        bot.answerCallbackQuery(query_id, text=busquedaTexto('pulsarBotonIdioma','Cast'))
        bot.sendMessage(idUsuario, busquedaTexto('respuestaCambioIdioma','Cast'))
    else:
        bot.sendMessage(idUsuario, busquedaTexto('respuestaCambioIdiomaError','Cast'))

