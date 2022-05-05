import os
import json
import string
from datetime import datetime
from os import path
import re, csv
#import pandas as pd

def clean_text(text, replace_commas_for_spaces=True):
    text = str(text)
    if not isinstance(text, float) and not isinstance(text, int):
        text = ''.join([c for c in text if c in string.printable])
        if replace_commas_for_spaces:
            text = text.replace('  ',' ').replace('\xa0','').replace("\n", '').replace("\t", '').replace("\r", '').strip()
        else:
            text = text.replace('  ',' ').replace('\xa0','').replace("\n", '').replace("\t", '').replace("\r", '').strip()
    if text == 'nan':
        text = ''
    return text

#constanst
input_path = '/Users/migherize/SourceTree/Insights_chess/src/Data_enginner/input'
workname = 'herize.pgn'
exp_jugadas = r'[0-9]+\.\s*[A-Za-z0-9+-=!?#]+\s[A-Za-z0-9+-=!?#]+|[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_white = r'^[0-9]+\.\s*[A-Za-z0-9+-=!?#]+'
jugadas_black = r'\s+[A-Za-z0-9+-=!?#]+$'

list_event = []
list_site = []
list_date = []
list_white = []
list_black = []
list_result = []
list_time = []
list_eloWhite = []
list_eloBlack = []
list_RatingDiff_W = []
list_RatingDiff_B = []
list_variant = []
list_time_control = []
list_ECO = []
list_Opening = []
list_Termination = []
list_data = []
#Funciones

def prueba(archive):
    lines = archive.readline()
    print("lines",len(lines))
    cont = 0

    if len(lines) > 0:
        for line in archive.readlines():
            cont += 1
            column_aux = re.findall(r'((?:\S\s?)+)',line)
            if column_aux:
                #ignorar = re.findall(r'^Permit #|^BUILDING|^PERMITS|^Zone|^Application Date|Page [0-9]+',line.strip())
                ignorar = False
                if ignorar:
                    continue
                else:
                    row_1 = re.findall(r'^\[Event\s*"((?:\S\s*?)+)"\]',line.strip())
                    row_2 = re.findall(r'^\[Site\s*"((?:\S\s?)+)"\]',line.strip())
                    row_3 = re.findall(r'^\[Date\s*"((?:\S\s?)+)"\]',line.strip())
                    row_4 = re.findall(r'^\[White\s*"((?:\S\s?)+)"\]',line.strip())
                    row_5 = re.findall(r'^\[Black\s*"((?:\S\s?)+)"\]',line.strip())
                    row_6 = re.findall(r'^\[Result\s*"((?:\S\s?)+)"\]',line.strip())
                    row_7 = re.findall(r'^\[UTCDate\s*"((?:\S\s?)+)"\]',line.strip())
                    row_8 = re.findall(r'^\[UTCTime\s*"((?:\S\s?)+)"\]',line.strip())
                    row_9 = re.findall(r'^\[WhiteElo\s*"((?:\S\s?)+)"\]',line.strip())
                    row_10 = re.findall(r'^\[BlackElo\s*"((?:\S\s?)+)"\]',line.strip())
                    row_11 = re.findall(r'^\[WhiteRatingDiff\s*"((?:\S\s?)+)"\]',line.strip())
                    row_12 = re.findall(r'^\[Variant\s*"((?:\S\s?)+)"\]',line.strip())
                    row_13 = re.findall(r'^\[TimeControl\s*"((?:\S\s?)+)"\]',line.strip())
                    row_14 = re.findall(r'^\[ECO\s*"((?:\S\s?)+)"\]',line.strip())
                    row_15 = re.findall(r'^\[Opening\s*"((?:\S\s?)+)"\]',line.strip())
                    row_16 = re.findall(r'^\[Termination\s*"((?:\S\s?)+)"\]',line.strip())
                    row_data = re.findall(r'^1.|^0-1|^1-0',line.strip())
                    #column_fecha = re.findall(r'^[0-9]+/[0-9]+/[0-9]+',line.strip())
                    
                    if row_1:
                        list_event.append(column_aux[0])
                    if row_2:
                        list_site.append(column_aux[0])
                    if row_3:
                        list_date.append(column_aux[0])
                    if row_4:
                        list_white.append(column_aux[0])
                    if row_5:
                        list_black.append(column_aux[0]) 
                    if row_6:
                        list_result.append(column_aux[0])
                    if row_7:
                        list_time.append(column_aux[0])
                    if row_8:
                        list_eloWhite.append(column_aux[0])
                    if row_9:
                        list_eloBlack.append(column_aux[0])
                    '''
                    if row_10:
                        if len(list_event)-1 == len(list_RatingDiff_W):
                            list_RatingDiff_W.append(column_aux[0]) 
                        else:
                            list_RatingDiff_W.append('')     
                    if row_11:
                        if len(list_event)-1 == len(list_RatingDiff_B):
                            list_RatingDiff_B.append(column_aux[0]) 
                        else:
                            print("line",cont)
                            break
                            list_RatingDiff_B.append('') 
                    '''
                    if row_12:
                        list_variant.append(column_aux[0])     
                    if row_13:
                        list_time_control.append(column_aux[0])  
                    if row_14:
                        list_ECO.append(column_aux[0])     
                    if row_15:
                        list_Opening.append(column_aux[0])  
                    if row_16:
                        list_Termination.append(column_aux[0])  
                    if row_data:
                        list_data.append(line) 
                        print("data",line)
                        if len(list_event) != len(list_data):
                            print("line",cont)
                            break

        #separacion de jugadas
        for game in list_data:
            cont1 = 1
            cont2 = 1
            string1 = '{}.'.format(cont1)
            string2 = '{}..'.format(cont2)  
            row_data = re.findall(r'^1.',game)
            
                        
    else:
        print("data vacia")
    
    
# Lectura de task de entrada
def split_color(game):
    tupla_color = []
    moves_white = []
    moves_black = []
    list_white = []
    list_black = []
    
    for g in game:
        result = re.findall(exp_jugadas,g.strip())
        if result:
            #print("result",result)
            #tupla_color.append(result[0])
            tupla_par = []
            for r in result:
                #print(r)
                jugada = re.search(jugadas_white,r.strip())
                if jugada:
                    num = re.search(r'^[0-9]+\.',r.strip())
                    if num:
                        #print("move",r[num.end():jugada.end()].strip(),r[jugada.end():].strip())
                        white = r[num.end():jugada.end()].strip()
                        black = r[jugada.end():].strip()
                        moves = white,black
                        tupla_par.append(moves)
                        moves_white.append(white)
                        moves_black.append(black)
                        #moves_white.append(r[num.end():jugada.end()])
                        #moves_black.append(r[jugada.end():])
            tupla_color.append(tupla_par)
            list_white.append(moves_white)
            list_black.append(moves_black)
        #print("----------------")
    #print("tupla_color",len(tupla_color))
    #print("list_white",len(list_white))
    #print("list_black",len(list_black))
    return tupla_color, list_white, list_black
    
def split_game (pgn):
    list_result = []
    list_game = []
    for ite,game in enumerate(pgn):
        #print(ite,"*",game)
        #print("game",len(game))
        result = re.findall(r'1-0$|0-1$|1/2-1/2$',game.strip())
        if result:
            list_result.append(result[0])
            list_game.append(game.strip().replace(result[0],''))

    return list_result, list_game

def data_split(archive):
    lines = archive.readline()
    cont = 0
    list_titles = []
    list_cabecera = []
    list_data = [] 
    
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
                        list_titles.append(list_cabecera)
                        list_data.append(clean_text(line))                
                        band = False
                    else:
                        list_data[-1] = list_data[-1]+' '+ clean_text(line)
    
    #print("list_titles",len(list_titles))
    #print("list_data",len(list_data))
    return list_titles,list_data

# input_pgn = os.listdir(input_pgn)

if os.path.isfile(path.join(input_path, workname)):
    #main
    archivo = open(path.join(input_path, workname), "r")
    #split_info(list_info)
    list_info, list_game = data_split(archivo)
    resultados, game = split_game(list_game)
    tupla_game, move_white, move_black = split_color(game)
    
    #Tamaños
    print("********* Tamaños *********")
    print("list_info",len(list_info))
    print("list_game",len(list_game))
    print("resultados",len(resultados))
    print("game",len(game))
    print("tupla_game",len(tupla_game))
    print("move_white",len(move_white))
    print("move_black",len(move_black))
    '''
    print("list_event",len(list_event))
    print("list_site",len(list_site))
    print("list_date",len(list_date))
    print("list_white",len(list_white))
    print("list_black",len(list_black))
    print("list_result",len(list_result))
    print("list_time",len(list_time))
    print("list_eloWhite",len(list_eloWhite))
    print("list_eloBlack",len(list_eloBlack))
    print("list_variant",len(list_variant))
    print("list_time_control",len(list_time_control))
    print("list_ECO",len(list_ECO))
    print("list_Opening",len(list_Opening))
    print("list_Termination",len(list_Termination))
    #print("list_data",len(list_data))
    '''
