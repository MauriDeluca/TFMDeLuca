import json
import pandas
import stanza

nlp_ = stanza.Pipeline(lang='es', processors='tokenize,pos,lemma')
preguntas_formulario = pandas.read_csv('Formvacacionesconetiquetas.csv')
data = {}
data["intents"]=[]
index_start = 2
version_creacion = 1

if version_creacion == 1:
    for pregunta in preguntas_formulario.columns[2:-1]:
        data["intents"].append(
            {
                "tag":pregunta,
                "patterns":[patt for patt in preguntas_formulario.iloc[:,index_start].str.lower().unique()]
            }
        )
        index_start +=1
elif version_creacion == 2:
    for pregunta in preguntas_formulario.columns[2:-1]:
        for patt in preguntas_formulario.iloc[:,index_start].str.lower().unique():
            if str(patt).lower() == 'nan':
                continue
            data["intents"].append(
                {
                    "tag":patt,
                    "patterns":[patt_ for patt_ in patt.split(';')]
                }
            )
        index_start +=1

elif version_creacion ==3:
    upos = []
    for pregunta in preguntas_formulario.columns[2:-1]:
        for patt in preguntas_formulario.iloc[:,index_start].str.lower().unique():
            if str(patt).lower() == 'nan':
                continue
            doc = nlp_(patt)
            lemmas = ''
            for sentencia in doc.sentences:
                for sen in json.loads(str(sentencia)):
                    try:
                        if sen["upos"] not in ['DET','PUNCT','AUX','PROPN','PRON', 'ADP','CCONJ']:
                            lemmas += sen["lemma"] + ' '
                        # else:
                        #     if sen["upos"] not in upos:
                        #         upos.append(sen["upos"])
                    except KeyError:
                        print("error por sentencia")
                        print(sen)
            duplicado = False
            for d in data["intents"]:
                if lemmas.strip() == d['tag']:
                    duplicado = True
                    d["patterns"].append(patt)
            if not duplicado:
                data["intents"].append(
                    {
                        "tag":lemmas.strip(),
                        "patterns":[patt_ for patt_ in patt.split(';')]
                    }
                )
        index_start +=1
    print(upos)
else:
    print("error en la elección de creación")

with open('intents_esp_auto_{0}.json'.format(version_creacion), 'w') as file:
    json.dump(data, file, indent=4)