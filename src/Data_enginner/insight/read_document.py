import enum
import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import opAssoc
import scipy.cluster.hierarchy as shc
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering

#__________________________________________________________________
# Inicio del script

def main():

    path_document = '../output' 
    document_name = 'Cluster.csv'

    try:
        
        dataframe = pd.read_csv(f"{path_document}/{document_name}")

        # Sin limpieza
        #see_info_dataframe(dataframe, document_name, '\nSin limpieza:')
        
        try:
            dataframe = clean_dataframe(dataframe)
        except Exception as e:
            print(e)
            print('Error en la funcion "clean_dataframe"\n')    

        # Con limpieza
        #see_info_dataframe(dataframe, document_name, 'Con limpieza:')

        NORMALIZE = True
        try:
            if NORMALIZE:
                dataframe_normalize = normalize(dataframe)
            else:
                dataframe_normalize = ''

        except Exception as e:
            print(e)
            print('Error en la normalizacion')

        dividing_line = True
        try:
            see_graph(dataframe, dividing_line, NORMALIZE, dataframe_normalize)
            pass
        except Exception as e:
            print(e)
            print('Error en la funcion "see_graph"\n') 

        try:
            do_cluster(dataframe)
        except Exception as e:
            print(e)
            print('Error en la funcion "see_graph"\n')


    except Exception as e:
        print(e)
        print('Error en la funcion main\n')

#__________________________________________________________________
# Informacion del dataframe

def see_info_dataframe(df, document_name, flag):
    print(flag)
    print(f'\n{"#"*60}')
    print(f'\t\tInformacion del documento "{document_name}":\n')
    print(df.info())
    print(f'{"_"*100}\n')
    print(df.head())
    print(f'\n{"#"*60}\n')

#__________________________________________________________________
# Limpieza del dataframe

def clean_dataframe(df):

    dataframe = df.replace('-1', None).dropna()
    dataframe = dataframe.set_index('Jugador')
    
    for index, column in enumerate(tuple(df.columns)):
        if index < 14:
            continue
        dataframe[column] = dataframe[column].apply( lambda data: data.encode('utf-8').hex() )

    return dataframe

#__________________________________________________________________
# Grafica del dataframe

def see_graph(df, dividing_line, NORMALIZE, df_normalize):
    
    if NORMALIZE:
        data_escaled = pd.DataFrame(df_normalize, columns=df.columns)
        info = 'con data normalizada'
    else:
        data_escaled = df
        info = 'sin data normalizada'

    if dividing_line:
        plt.figure(figsize=(14,7))
        plt.title(f"Dendograma {info}".strip())
        dend = shc.dendrogram(shc.linkage(data_escaled,method="ward"))
        plt.axhline(y=20000,color='r',linestyle='--')
        plt.show()
        return
        
    plt.figure(figsize=(10,5))
    plt.title("Dendrograms")
    dend = shc.dendrogram(shc.linkage(data_escaled,method="ward"))
    plt.show()

#__________________________________________________________________
# cluster
def do_cluster(df):

    cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    predict = cluster.fit_predict(df)
    print(len(predict))

    plt.figure(figsize=(10,7))
    plt.scatter(
        df['Victoria Blancas'],
        df['Victorias Negras'],
        c=cluster.labels_
    )
    plt.show()

    bank_cust = df.reset_index()
    clusterDF = pd.DataFrame(predict)

    clusterDF.columns = ['Cluster_predicted']
    combineDF = pd.concat([bank_cust,clusterDF],axis = 1).reset_index()
    combineDF = combineDF.drop(['index'],axis=1)

    for index, column in enumerate(tuple(df.columns)):
        if index < 14:
            continue
        combineDF[column] = combineDF[column].apply( lambda data: bytes.fromhex(data).decode('utf-8') )

    print(combineDF)

#__________________________________________________________________
# Ejecucion de codigo
main()