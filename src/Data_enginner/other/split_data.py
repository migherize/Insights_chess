import os
import json
import string
from datetime import datetime
from os import path
import re, csv
import pandas as pd

def clean_text(text, replace_commas_for_spaces=True):
    text = str(text)
    if not isinstance(text, float) and not isinstance(text, int):
        text = ''.join([c for c in text if c in string.printable])
        if replace_commas_for_spaces:
            text = text.replace('  ',' ').replace('\xa0','').replace("\n", '').replace("\t", '').replace("\r", '').replace('"', '').strip()
        else:
            text = text.replace('  ',' ').replace('\xa0','').replace("\n", '').replace("\t", '').replace("\r", '').replace('"', '').strip()
    if text == 'nan':
        text = ''
    return text
    
def split_dataframe(df,user):
    win_white = 0
    win_black = 0
    draw_white = 0
    draw_black = 0
    lose_white = 0
    lose_black = 0
    
    
    Eco_white_win = []
    Eco_black_win = []
    
    Eco_white_draw = []
    Eco_black_draw = []
    
    Eco_white_lose = []
    Eco_black_lose = []
    
    for i in df.index: 
        #print("Result: ", str(df['Result'][i]), "ECO: ", str(df['ECO'][i]))
        #print("Blancas: ", str(df['Blancas'][i]), "Negras: ", str(df['Negras'][i]))
        
        # valores positivos
        if user == df['Blancas'][i] and str(df['Result'][i]) == '1-0':
            win_white += 1
            Eco_white_win.append(str(df['ECO'][i]))
        elif user == df['Negras'][i] and str(df['Result'][i]) == '0-1':
            win_black += 1
            Eco_black_win.append(str(df['ECO'][i]))
        
        # valores neutros
        elif user == df['Blancas'][i] and str(df['Result'][i]) == '1/2-1/2':
            draw_white += 1
            Eco_white_draw.append(str(df['ECO'][i]))
            
        elif user == df['Negras'][i] and str(df['Result'][i]) == '1/2-1/2':
            draw_black += 1
            Eco_black_draw.append(str(df['ECO'][i]))
        
        # valores negativos
        elif user == df['Negras'][i] and str(df['Result'][i]) == '1-0':
            lose_white += 1
            Eco_white_lose.append(str(df['ECO'][i]))
            
        elif user == df['Blancas'][i] and str(df['Result'][i]) == '0-1':
            lose_black += 1
            Eco_black_lose.append(str(df['ECO'][i]))
            
        else:
            print(str(df['Result'][i]),str(df['Negras'][i]))
            print(str(df['Blancas'][i]),str(df['Result'][i]))

    print("win_white:",win_white)
    print("win_black:",win_black)
    print("draw_white:",draw_white)
    print("draw_black:",draw_black)
    print("lose_white:",lose_white)
    print("lose_black:",lose_black)
    
    print("Victorias con Blancas",max(set(Eco_white_win), key = Eco_white_win.count), Eco_white_win.count(max(set(Eco_white_win), key = Eco_white_win.count)))        
    print("Victorias con Negras",max(set(Eco_black_win), key = Eco_black_win.count), Eco_black_win.count(max(set(Eco_black_win), key = Eco_black_win.count)))        
    
    print("tablas con Blancas",max(set(Eco_white_draw), key = Eco_white_draw.count), Eco_white_draw.count(max(set(Eco_white_draw), key = Eco_white_draw.count)))        
    print("tablas con Blancas",max(set(Eco_black_draw), key = Eco_black_draw.count), Eco_black_draw.count(max(set(Eco_black_draw), key = Eco_black_draw.count)))        

    print("Perdi con Blancas",max(set(Eco_white_lose), key = Eco_white_lose.count), Eco_white_lose.count(max(set(Eco_white_lose), key = Eco_white_lose.count)))        
    print("Perdi con Blancas",max(set(Eco_black_lose), key = Eco_black_lose.count), Eco_black_lose.count(max(set(Eco_black_lose), key = Eco_black_lose.count)))        

    return win_white, draw_white,lose_white, win_black, draw_black ,lose_black


def data_split(archive):
    lines = archive.readline()
    cont = 0
    list_titles = []
    list_cabecera = []
    list_data = [] 
    list_white = []
    list_black = []
    list_ECO = []
    list_opening = []
    list_result = []
    
    if lines:
        for line in archive.readlines():
            #print("line",line)
            cont += 1
            column_aux = re.findall(r'((?:\S\s?)+)',line)
            if column_aux:
                row_1 = re.findall(r'^\[((?:\S\s*?)+)\]',line.strip())
                if row_1:
                    #print("guardo",row_1[0])
                    list_cabecera.append(row_1[0])
                    aux1 = re.findall(r'^White\s',str(row_1[0]))
                    aux2 = re.findall(r'^Black\s',str(row_1[0]))
                    aux3 = re.findall(r'^Result',str(row_1[0]))
                    aux4 = re.findall(r'^ECO',str(row_1[0]))
                    aux5 = re.findall(r'^Opening',str(row_1[0]))
                    if aux1:
                        list_white.append(clean_text(row_1[0].replace(aux1[0],'')).strip())
                    if aux2:
                        list_black.append(clean_text(row_1[0].replace(aux2[0],'')).strip())
                    if aux3:
                        list_ECO.append(clean_text(row_1[0].replace(aux3[0],'')))
                    if aux4:
                        list_opening.append(clean_text(row_1[0].replace(aux4[0],'')))
                    if aux5:
                        list_result.append(clean_text(row_1[0].replace(aux5[0],'')))
    
                    band = True
                    
                else:
                    if band:
                        list_titles.append(list_cabecera)
                        list_data.append(clean_text(line))                
                        band = False
                    else:
                        list_data[-1] = list_data[-1]+' '+ clean_text(line)
    
    return list_white,list_black,list_ECO,list_opening,list_result,list_titles,list_data
    
    
input_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/input'
workname = 'mherize.pgn'
exp_jugadas = r'[0-9]+\.\s*[A-Za-z0-9+-=!?#]+\s[A-Za-z0-9+-=!?#]+|[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_white = r'^[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_black = r'\s+[A-Za-z0-9+-=!?#]+$'
user = 'mherize'
# Consulta la data
if os.path.isfile(path.join(input_path, workname)):
    archivo = open(path.join(input_path, workname), "r")
    list_white, list_black, list_result, list_ECO, list_Opening, list_info, list_game = data_split(archivo)
    #Tamaños
    print("********* Tamaños *********")
    print("list_info",len(list_info))
    print("list_game",len(list_game))
    print("list_white",len(list_white))
    print("list_black",len(list_black))
    print("list_result",len(list_result))
    print("list_ECO",len(list_ECO))
    print("list_Opening",len(list_Opening))
    df = pd.DataFrame(list(zip(list_white,list_black,list_result,list_ECO,list_Opening)), columns = ['Blancas','Negras','Result','ECO','Opening'])
    print(df)
    win_white, draw_white,lose_white, win_black, draw_black ,lose_black = split_dataframe(df,user)
    
    df2 = pd.DataFrame(columns = ['Jugador','Partidas','Victoria Blancas','Tablas Blancas','Perdidas Blancas','Victorias Negras','Tablas Negras','Perdidas Negras'],index=range(100))
    df2.iloc[0] = (user,len(list_game),win_white,draw_white,lose_white,win_black,draw_black,lose_black)
    print(df2)
    df.to_csv("output/data.csv", index = False)
    df2.to_csv("output/data2.csv", index = False)
    
    
    #print("game",len(game))