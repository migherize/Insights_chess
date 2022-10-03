import enum
import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import opAssoc
import scipy.cluster.hierarchy as shc
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import base64
from io import BytesIO
from matplotlib import pyplot
#__________________________________________________________________
# Inicio del script

def main():

    path_document = '../output' 
    document_name = 'Cluster.csv'
    corte_t = 0.35

    try:
        
        dataframe_input = pd.read_csv(f"{path_document}/{document_name}")

        # Sin limpieza
        #see_info_dataframe(dataframe, document_name, '\nSin limpieza:')
        
        try:
            dataframe = clean_dataframe(dataframe_input)
        except Exception as e:
            print(e)
            print('Error en la funcion "clean_dataframe"\n')    

        # Con limpieza
        #see_info_dataframe(dataframe, document_name, 'Con limpieza:')
        print("dataframe",dataframe)
        df1 = dataframe.loc[:,:'No. Perdidas Negras']
        print("df1",df1)
        
        NORMALIZE = True
        try:
            if NORMALIZE:
                dataframe_normalize = normalize(dataframe)
                #dataframe_normalize = dataframe
            else:
                dataframe_normalize = ''

        except Exception as e:
            print(e)
            print('Error en la normalizacion')
        
        #dataframe.loc[:,:'No. Perdidas Negras'] = dataframe_normalize
        print("normalizado",dataframe)
        
        scaled_df = pd.DataFrame(dataframe_normalize, columns= dataframe.columns)
        print("scaled_df",scaled_df)

        dividing_line = True
        try:
            see_graph(dataframe, dividing_line, NORMALIZE, dataframe_normalize,corte_t)
            pass
        except Exception as e:
            print(e)
            print('Error en la funcion "see_graph"\n') 

        try:
            do_cluster(scaled_df)
        except Exception as e:
            print(e)
            print('Error en la funcion "do_cluster"\n')


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
        print("i",index,column)
        if column == 'Jugador':
            continue
        
        if index < 14:
            continue
        
        for j,i in enumerate(dataframe[column]):
            i = float(i.replace('A','1.').replace('B','2.').replace('C','3.').replace('D','4.').replace('E','5.'))
            dataframe[column][j] = i
        #dataframe[column] = dataframe[column].apply( lambda data: data.encode('utf-8').hex() )

        #else:
            #dataframe[column] = dataframe[column].apply( lambda data: data.encode('utf-8').hex() )
            #dataframe[column]= dataframe.apply(lambda data: log(data,10))

    return dataframe

#__________________________________________________________________
# Grafica del dataframe

def see_graph(df, dividing_line, NORMALIZE, df_normalize,corte_t):
    if NORMALIZE:
        data_escaled = pd.DataFrame(df_normalize, columns=df.columns)
        info = 'con data normalizada'
    else:
        data_escaled = df
        info = 'sin data normalizada'

    #print(df,NORMALIZE)
    Clustering_Jeraruico = shc.linkage(data_escaled,method="ward")

    if dividing_line:
        plt.figure(figsize=(14,7))
        plt.title(f"Dendograma {info}".strip())
        dend = shc.dendrogram(Clustering_Jeraruico)
        clusters = shc.fcluster(Clustering_Jeraruico, t=corte_t, criterion='distance')
        print("clusters",clusters)
        max_value = max(clusters)
        print("max_value",max_value)
        plt.axhline(y=0.22,color='r',linestyle='--')
        #plt.show()
        plt.savefig("tree.png")
        return

    #plt.figure(figsize=(10,5))
    #plt.title("Dendrograms")
    #dend = shc.dendrogram(Clustering_Jeraruico)
    #clusters = shc.fcluster(Clustering_Jeraruico, t=3, criterion='distance')
    #print("clusters",clusters)
    #plt.savefig("tree_2.png")
    #plt.show()

def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

#__________________________________________________________________
# cluster
def do_cluster(df):
    print(df.dtypes)
    cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    predict = cluster.fit_predict(df)
    print("predict",predict)
    print("predict",len(predict))

    # Grafica de Victoriass
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,7))
    plt.title('Cluster de victorias')
    plt.scatter(
        df['Victoria Blancas'],
        df['Victorias Negras'],
        c=cluster.labels_
    )
    #plt.show()
    plt.tight_layout()
    graph = get_graph()
    plt.savefig("cluster.png")
    return graph

#__________________________________________________________________
# Ejecucion de codigo
main()