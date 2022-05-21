import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

dataframe = pd.read_csv(r"analisis.csv")
print(dataframe.head())
print(dataframe.describe())
print(dataframe.groupby('categoria').size())
#print(dataframe.drop(['categoria'],1).hist())
#print(plt.show())
sb.pairplot(dataframe.dropna(), hue='categoria',size=4,vars=["op","ex","ag"],kind='scatter')
'''
def normalizar(lista):
    min_list = int(min(lista))
    max_list = int(max(lista))
    list_normalizer = []
    
    for l in lista:
        z = (int(l) - min_list) / (max_list - min_list)
        list_normalizer.append(z)
    
    return list_normalizer

df = pd.read_csv('data.csv')
print(df)

list_of_single_column1 = list(df['tiempo'])
list_of_single_column2 = list(df['sueldo'])
list_of_single_column3 = list(df['gasto'])

print("list1", list_of_single_column1)
print("list2", list_of_single_column2)
print("list3", list_of_single_column3)

list_normalizado1 = []
list_normalizado2 = []
list_normalizado3 = []

list_normalizado1 = normalizar(list_of_single_column1)
list_normalizado2 = normalizar(list_of_single_column2)
list_normalizado3 = normalizar(list_of_single_column3)

print("Normalizer 1", list_normalizado1)
print("Normalizer 2", list_normalizado2)
print("Normalizer 3", list_normalizado3)

df2 = pd.DataFrame(list(zip(list_normalizado1,list_normalizado2,list_normalizado3)))
print("Dataframe Normalize", df2)
'''

