import os
import json
import string
from datetime import datetime
from os import path
import re, csv
import pandas as pd
import requests

#constanst
input_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/input_request'
split_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/input_split'
output_split_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/output_split'
join_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/join_split'
output = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/output'
workname = 'data.pgn'
token = "lip_0obpMyLkJNap1lEFGZjA"
cabeceras = {'Authorization': 'Bearer lip_0obpMyLkJNap1lEFGZjA'}
base_url = "https://lichess.org/api"

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
        # valores positivos
        if user == str(df['Blancas'][i]).lower() and str(df['Result'][i]) == '1-0':
            win_white += 1
            Eco_white_win.append(str(df['ECO'][i]))
        elif user == str(df['Negras'][i]).lower() and str(df['Result'][i]) == '0-1':
            win_black += 1
            Eco_black_win.append(str(df['ECO'][i]))
        
        # valores neutros
        elif user == str(df['Blancas'][i]).lower() and str(df['Result'][i]) == '1/2-1/2':
            draw_white += 1
            Eco_white_draw.append(str(df['ECO'][i]))
            
        elif user == str(df['Negras'][i]).lower() and str(df['Result'][i]) == '1/2-1/2':
            draw_black += 1
            Eco_black_draw.append(str(df['ECO'][i]))
        
        # valores negativos
        elif user == str(df['Negras'][i]).lower() and str(df['Result'][i]) == '1-0':
            lose_white += 1
            Eco_white_lose.append(str(df['ECO'][i]))
            
        elif user == str(df['Blancas'][i]).lower() and str(df['Result'][i]) == '0-1':
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

    if win_white != 0 and win_black != 0 and draw_white != 0 and draw_black != 0 and lose_white != 0 and lose_black != 0:
        print("Victorias con Blancas",max(set(Eco_white_win), key = Eco_white_win.count), Eco_white_win.count(max(set(Eco_white_win), key = Eco_white_win.count)))        
        print("Victorias con Negras",max(set(Eco_black_win), key = Eco_black_win.count), Eco_black_win.count(max(set(Eco_black_win), key = Eco_black_win.count)))        
        print("tablas con Blancas",max(set(Eco_white_draw), key = Eco_white_draw.count), Eco_white_draw.count(max(set(Eco_white_draw), key = Eco_white_draw.count)))        
        print("tablas con Blancas",max(set(Eco_black_draw), key = Eco_black_draw.count), Eco_black_draw.count(max(set(Eco_black_draw), key = Eco_black_draw.count)))        
        print("Perdi con Blancas",max(set(Eco_white_lose), key = Eco_white_lose.count), Eco_white_lose.count(max(set(Eco_white_lose), key = Eco_white_lose.count)))        
        print("Perdi con Blancas",max(set(Eco_black_lose), key = Eco_black_lose.count), Eco_black_lose.count(max(set(Eco_black_lose), key = Eco_black_lose.count)))        
        codigo_white_win = max(set(Eco_white_win), key = Eco_white_win.count)
        num_white_win = Eco_white_win.count(max(set(Eco_white_win), key = Eco_white_win.count))
        
        codigo_black_win = max(set(Eco_black_win), key = Eco_black_win.count)
        num_black_win = Eco_black_win.count(max(set(Eco_black_win), key = Eco_black_win.count))
        
        codigo_white_draw = max(set(Eco_white_draw), key = Eco_white_draw.count)
        num_white_draw = Eco_white_draw.count(max(set(Eco_white_draw), key = Eco_white_draw.count))
        
        codigo_black_draw = max(set(Eco_black_draw), key = Eco_black_draw.count)
        num_black_draw = Eco_black_draw.count(max(set(Eco_black_draw), key = Eco_black_draw.count))

        codigo_white_lose = max(set(Eco_white_lose), key = Eco_white_lose.count)
        num_white_lose = Eco_white_lose.count(max(set(Eco_white_lose), key = Eco_white_lose.count))

        codigo_black_lose = max(set(Eco_black_lose), key = Eco_black_lose.count)
        num_black_lose = Eco_black_lose.count(max(set(Eco_black_lose), key = Eco_black_lose.count))

    else:
        codigo_white_win = -1
        num_white_win = -1
        codigo_black_win = -1
        num_black_win= -1
        codigo_white_draw= -1
        num_white_draw= -1
        codigo_black_draw= -1
        num_black_draw= -1
        codigo_white_lose= -1
        num_white_lose= -1
        codigo_black_lose= -1
        num_black_lose= -1

    return codigo_white_win, num_white_win, codigo_black_win, num_black_win, codigo_white_draw, num_white_draw, codigo_black_draw, num_black_draw, codigo_white_lose, num_white_lose, codigo_black_lose, num_black_lose, win_white, draw_white,lose_white, win_black, draw_black ,lose_black

def split_Header(info):
    list_white = []
    list_black = []
    list_ECO = []
    list_opening = []
    list_result = []
    
    for i in info:
        for j in i:
            aux1 = re.findall(r'^White\s',str(j))
            aux2 = re.findall(r'^Black\s',str(j))
            aux3 = re.findall(r'^Result',str(j))
            aux4 = re.findall(r'^ECO',str(j))
            aux5 = re.findall(r'^Opening',str(j))
            if aux1:
                list_white.append(clean_text(j.replace(aux1[0],'')).strip())
            if aux2:
                list_black.append(clean_text(j.replace(aux2[0],'')).strip())
            if aux3:
                list_ECO.append(clean_text(j.replace(aux3[0],'').replace('?','-1')))
            if aux4:
                list_opening.append(clean_text(j.replace(aux4[0],'').replace('?','-1')))
            if aux5:
                list_result.append(clean_text(j.replace(aux5[0],'').replace('?','-1')))
    
    return list_white,list_black,list_ECO,list_opening,list_result

def select_split():
    # Lectura de png
    input_split = os.listdir(split_path)
    for num,name in enumerate(input_split):
        if name == '.DS_Store':
            input_split.pop(num)
    return input_split

def data_split(archive):
    lines = archive.readline()
    cont = 0
    list_titles = []
    list_data = [] 
    list_cabecera = []
    
    if lines:
        for line in archive.readlines():
            #print("line",line)
            cont += 1
            column_aux = re.findall(r'((?:\S\s?)+)',line)
            if column_aux:
                row_1 = re.findall(r'^\[((?:\S\s*?)+)\]',line.strip())
                #row_2 = re.findall(r'^\[((?:\S\s*?)+)\]',line.strip())
                if row_1:
                    list_cabecera.append(row_1[0])
                    band = True
                    
                else:
                    if band:
                        #print("list_cabecera",list_cabecera)
                        list_titles.append(list_cabecera)
                        #print("list_titles",list_titles)
                        list_data.append(clean_text(line))                
                        band = False
                        list_cabecera = []
                        #numero = input("continuar")
                    else:
                        list_data[-1] = list_data[-1]+' '+ clean_text(line)
    
        #print("list_titles afuera",list_titles)
        #numero = input("continuar ")
    
    return list_titles,list_data


def all_games(df):
    list_user = []
    for i in df.index:
        print(i, df['Users'][i])
        list_user.append(str(df['Users'][i]))
        
    return list_user

def select_api(user):
    #https://lichess.org/@/mherize/download
    #nick = requests.get(base_url+'/games/user/mherize?analysed=false&tags=true&clocks=true&evals=true&opening=true&perfType=ultraBullet%2Cbullet%2Cblitz%2Crapid%2Cclassical',headers=cabeceras)
    complement = '/games/user/{}?tags=true&clocks=false&evals=false&opening=true'.format(user)
    nick = requests.get(base_url+complement,headers=cabeceras)
    print(nick.status_code)
    #print(nick.content)
    print("----------------")
    with open(os.path.join(split_path,('{}.pgn'.format(user))), 'w') as f:
        f.writelines(nick.text)
    return nick

# Lectura de task de entrada
input_api = os.listdir(input_path)
for num,name in enumerate(input_api):
    if name == '.DS_Store':
        input_api.pop(num)

list_user = []

if len(input_api) > 0:
    df = pd.read_csv(os.path.join(input_path,input_api[0]))
    print(df)
    #print("Vamos a consultar a la Api")
    nick = all_games(df)
    #for n in nick:
    #    data = select_api(n)
    pgn = select_split()
    if len(pgn) > 0:
        '''for num,p in enumerate(pgn):
            list_user = []
            print("vamos a separar", p)
            archivo = open(path.join(split_path, p), "r")
            list_info, list_game = data_split(archivo)
            print("nick.index(p.replace('.pgn',''))",nick.index(p.replace('.pgn','')))
            print("list_info",len(list_info))
            print("list_game",len(list_game))
            usuario = p.replace('.pgn','')
            print("usuario",usuario)
            for i in list_info:
                list_user.append(usuario)
            
            df = pd.DataFrame(list(zip(list_user,list_info,list_game)), columns = ['ID User','Headers','Move'])
            df.to_csv(path.join(output_split_path,'{}_TableGame.csv'.format(usuario)), index = False)
    
            list_white, list_black, list_result, list_ECO, list_Opening = split_Header(list_info)
            print("White",len(list_white))
            print("list_black",len(list_black))
            print("list_result",len(list_result))
            print("list_ECO",len(list_ECO))
            print("list_Opening",len(list_Opening))
            
            df = pd.DataFrame(list(zip(list_white,list_black,list_result,list_ECO,list_Opening)), columns = ['Blancas','Negras','Result','ECO','Opening'])
            print(df)
            df.to_csv(path.join(join_path,'{}_TableHeader.csv'.format(usuario)), index = False)
            '''
        # Join
        input_join = os.listdir(join_path)
        for num,name in enumerate(input_join):
            if name == '.DS_Store':
                input_join.pop(num)
        
        print("input_join",len(input_join))
        for i,j in enumerate(input_join):
            print("i",i,j)
            nick = re.findall(r'((?:\S\s?)+)_', j)
            user = str(nick[0]).lower()
            df = pd.read_csv(path.join(join_path, j))
            print(user,"path.join(join_path, i)",path.join(join_path, j))
            print(df.replace('\"',''))
            
            codigo_white_win, num_white_win, codigo_black_win, num_black_win, codigo_white_draw, num_white_draw, codigo_black_draw, num_black_draw, codigo_white_lose, num_white_lose, codigo_black_lose, num_black_lose, win_white, draw_white,lose_white, win_black, draw_black ,lose_black = split_dataframe(df,user) 
            if i == 0:
                df2 = pd.DataFrame(columns = ['Jugador','Partidas','Victoria Blancas','Tablas Blancas','Perdidas Blancas','Victorias Negras','Tablas Negras','Perdidas Negras','No. Victorias Blancas','No. Tablas Blancas','No. Perdidas Blancas','No. Victorias Negras','No. Tablas Negras','No. Perdidas Negras', 'Cod. Victorias Blancas','Cod. Tablas Blancas','Cod. Perdidas Blancas','Cod. Victorias Negras','Cod. Tablas Negras','Cod. Perdidas Negras'],index=range(100))
                df2.iloc[i] = (user,len(df),win_white,draw_white,lose_white,win_black,draw_black,lose_black, num_white_win, num_white_draw, num_white_lose, num_black_win, num_black_draw, num_black_lose, codigo_white_win, codigo_white_draw, codigo_white_lose, codigo_black_win, codigo_black_draw, codigo_black_lose)
            else:
                df2.iloc[i] = (user,len(df),win_white,draw_white,lose_white,win_black,draw_black,lose_black, num_white_win, num_white_draw, num_white_lose, num_black_win, num_black_draw, num_black_lose, codigo_white_win, codigo_white_draw, codigo_white_lose, codigo_black_win, codigo_black_draw, codigo_black_lose)
                
            print(df2)
            df2.to_csv(path.join(output,'Cluster.csv'), index = False)