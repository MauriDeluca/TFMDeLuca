dicCast = {
# telegram.py //////////////////////////////////////////////////////////////////
    "botInactivo": "Ahora mismo estoy en mantenimiento! Vuelve a hablarme más tarde por favor.",
    "comandoStart": 'Hola, como estas?',
    "errorNoTexto": "¿Podrías repetirlo, por favor?",
# busquedaRespuesta.py /////////////////////////////////////////////////////////
    "resErrorRespApiai": 'El servicio no esta disponible en este momento, vuelve a intentarlo más tarde.',
    "resErrorRespWH": "Los datos no están disponibles en este momento. Vuelve a mandar tu pregunta en unos minutos, por favor.",
    "resComplemento.Saludo": "¡Buenos días!",
    "resinput.unknown": "No he encontrado una respuesta para esa pregunta, disculpa.",
}

##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Funcion
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def busquedaTexto(key,idioma):
    text = dicCast[key]

    return text
