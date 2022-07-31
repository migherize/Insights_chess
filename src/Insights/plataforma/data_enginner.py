import os
import json
import string
from datetime import datetime
from os import path
import re, csv
import pandas as pd
import requests
from collections import Counter

exp_jugadas = r'[0-9]+\.\s*[A-Za-z0-9+-=!?#]+\s[A-Za-z0-9+-=!?#]+|[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_white = r'^[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_black = r'\s+[A-Za-z0-9+-=!?#]+$'

#constanst
split_path = '/Users/migherize/Sourcetree/InsightsChess/src/Insights/media'



input_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/input_request'
output_split_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/output_split'
join_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/join_split'
output = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/output'
workname = 'data.pgn'
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
    user = user.lower()
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



def split_color(game):
    tupla_color = []
    moves_white = []
    moves_black = []
    list_white = []
    list_black = []
    
    for g in game:
        #print("-----------------")
        #print("Nueva Partida",g)
        result = re.findall(exp_jugadas,g.strip())
        if result:
            #print("par de jugadas",result)
            tupla_color.append(result[0])
            tupla_par = []

            for r in result:
                #print(r)
                jugada = re.search(jugadas_white,r.strip())
                if jugada:
                    num = re.search(r'^[0-9]+\.',r.strip())
                    if num:
                        white = r[num.end():jugada.end()].strip()
                        black = r[jugada.end():].strip()
                        moves = white,black
                        #print("moves",moves)
                        #print("white",white)
                        #print("black",black)
                        tupla_par.append(moves)
                        moves_white.append(white)
                        moves_black.append(black)
            
            #print("moves",tupla_par)
            #print("white",moves_white)
            #print("black",moves_black)
            
            tupla_color.append(tupla_par)
            list_white.append(moves_white)
            list_black.append(moves_black)
            tupla_par = []
            moves_white = []
            moves_black = []

        else:
            print("no entro",g.strip())
            #print("list_white",len(list_white))
            moves = 'Forfeit',g.strip()
            tupla_color.append(moves)
            list_white.append(g.strip())
            list_black.append(g.strip())
        #print("----------------")
    #print("tupla_color",len(tupla_color))
    #print("list_white",len(list_white))
    #print("list_black",len(list_black))
    return tupla_color, list_white, list_black
    

def change_user(user):
    lista = []
    archive = open(path.join(split_path, ('{}.pgn'.format(user))), "r")
    lines = archive.readline()
    if lines:
        for line in archive.readlines():
            column_aux = re.findall(r'((?:\S\s?)+)',line)
            if column_aux:
                #print("line",column_aux)
                jugadores = re.findall(r'^White\s|^Black\s',column_aux[0].replace('[','').replace(']',''))
                if jugadores:
                    jugadores = re.findall(r'\"((?:\S\s?)+)\"',column_aux[0])
                    print("jugadores",jugadores)
                    lista.append(jugadores[0].replace('[','').replace(']','').replace('"','').replace('"',''))

        print(Counter(lista).most_common()[0][0])
        archive.close()
        with open(path.join(split_path, ('{}.pgn'.format(user))), 'r+') as f:
            text = f.read()
            text = re.sub(Counter(lista).most_common()[0][0], user, text)
            f.seek(0)
            f.write(text)
            f.truncate()

    #print(Counter(lista).most_common()[0][1])
    #print(Counter(lista).most_common())
    #return Counter(lista).most_common()[0][0]

def data_split(user):
    archive = open(path.join(split_path, ('{}.pgn'.format(user))), "r")
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
