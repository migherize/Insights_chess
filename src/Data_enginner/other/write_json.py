import enum
import json
import pandas as pd
import matplotlib.pyplot as plt
diccionario = {}
diccionario2 = {}
lis_encabezado = ['Opponent strength','Rating gain','Number of games']
cont = 0
list_item = []
encabezado = 3
data = [
    'Much weaker', -0.97, 341,
    'Weake', -0.97, 356,
    'Similar', 0.71, 232,
]
		
for d in range(0,len(data),encabezado):
    diccionario[cont] = []
    for i in range(d,(d+encabezado)):
        print("d",d)
        print("i",data[i])
        diccionario[cont].append(data[i])
    cont+=1

print(diccionario)
df = pd.DataFrame(diccionario,lis_encabezado)
df = df.transpose()
print("df",df)

grafico = df.groupby('Rating gain')['Number of games'].sum().plot(kind='bar', legend='Reverse')
print(grafico)
'''
value_list = ['Johnny', '27', 'New York']
print("key_list",type(key_list))
dict_from_list = dict(zip(key_list, value_list))
print(dict_from_list)
data = {}



data['clients'] = []
data['clients'].append({
    'first_name': 'Sigrid',
    'last_name': 'Mannock',
    'age': 27,
    'amount': 7.17})
data['clients'].append({
    'first_name': 'Joe',
    'last_name': 'Hinners',
    'age': 31,
    'amount': [1.90, 5.50]})
data['clients'].append({
    'first_name': 'Theodoric',
    'last_name': 'Rivers',
    'age': 36,
    'amount': 1.11})

'''
with open('data.json', 'w') as file:
    json.dump(diccionario, file, indent=4)
