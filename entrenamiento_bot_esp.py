
import json
import stanza

# stanza.download('es')
# nlp = stanza.Pipeline(lang='es') #tokenize, mwt, pos,lemma,depparse
nlp_ = stanza.Pipeline(lang='es', processors='tokenize,pos,lemma')

chatbot_basico = open('chatbot_basico.json').read()
chatbot_basico_config = json.loads(chatbot_basico)
for p in chatbot_basico_config["preguntas"]:
    for pregunta in p["pregunta"]:
        print(pregunta)
        # doc = nlp_(pregunta)
        doc = nlp_('sola, y si alguien se suma mejor!')
        for sentencia in doc.sentences:
            for sen in json.loads(str(sentencia)):
                print("text: {0}, lemma: {1}, upos: {2}".format(sen["text"],sen["lemma"],sen["upos"]))

