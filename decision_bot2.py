from sklearn.model_selection import train_test_split
import pandas
import numpy as np

# decision final
preguntas_formulario = pandas.read_csv('Formvacacionesconetiquetas.csv', encoding ='latin1')


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
 
# 80% training 20% testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.20, random_state=0)

cambio_algoritmo = True # True Decision Tree ; False KNN

if cambio_algoritmo:
    #Decision Tree
    from sklearn.tree import DecisionTreeRegressor
    DT_model = DecisionTreeRegressor(max_depth=5).fit(X_train,Y_train)
    model_predict = DT_model.predict(X_test)
else:
    # KNN
    from sklearn.neighbors import KNeighborsRegressor
    KNN_model = KNeighborsRegressor(n_neighbors=3).fit(X_train,Y_train)
    model_predict = KNN_model.predict(X_test)


print(model_predict)
print(y_index)
index_ = 0
for result in model_predict:
    print ("resultado predicho {0} resultado esperado {1}".format(round(result),Y_test[index_]) )
    index_ += 1
print(model_predict, Y_test)
