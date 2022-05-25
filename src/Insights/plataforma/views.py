from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

#Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import *
from .models import *
from .api_lichess import *
from .data_enginner import *
import json
# Create your views here.


# Create your views here.
def base(request):
    return render(request, 'Views/base.html', {})

def main(request):
    return render(request, 'Views/main.html', {})

def register(request):
    return render(request, 'Views/Register.html', {})

def signUp(request):
    print("entre",request.method)
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                elo = user.nick.rankings.all()
                return render(request, 'Views/Home.html', {'elo': elo })
            else:
                print("voy a registrar")
                get_account = account()
                if get_account.status_code == 200:
                    list_blitz = []
                    list_bullet = []
                    list_rapid = []
                    list_classical = []
                    dict_count = {}
                    elos = get_account.json()['perfs']
                    for n, e in enumerate(elos):
                        if e == 'blitz':
                            list_blitz.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_blitz.append(get_account.json()['perfs'][e][key])
                        elif e == 'bullet':
                            list_bullet.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_bullet.append(get_account.json()['perfs'][e][key])
                        elif e == 'rapid':
                            list_rapid.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_rapid.append(get_account.json()['perfs'][e][key])
                        elif e == 'classical':
                            list_classical.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_classical.append(get_account.json()['perfs'][e][key])
                    
                    url_nick = str(get_account.json()['url'])
                    print("url",url_nick)
                    count = get_account.json()['count']
                    for key, value in count.items():
                        if key == 'rated' or key == 'draw' or key == 'loss' or key == 'win':
                            dict_count[key] = value
                    
                    
                    # insert en DB
                    email = 'correo@gmail.com'
                    user = User.objects.create_user(username, email, password)
                    perfil = Perfil.objects.create(url= url_nick,rated=dict_count['rated'],n_draw=dict_count['draw'],n_loss=dict_count['loss'],n_win=dict_count['win'],username=user)
                    Foto.objects.create(ruta='../static/img/user.jpg',picture=perfil)
                    print("list_blitz",list_blitz)
                    Elo.objects.create(name=list_blitz[0],games=int(list_blitz[1]), rating=int(list_blitz[2]), rd=int(list_blitz[3]), prog=int(list_blitz[4]), ranking=perfil)
                    Elo.objects.create(name=list_bullet[0],games=int(list_bullet[1]), rating=int(list_bullet[2]), rd=int(list_bullet[3]), prog=int(list_bullet[4]), ranking=perfil)
                    Elo.objects.create(name=list_rapid[0],games=int(list_rapid[1]), rating=int(list_rapid[2]), rd=int(list_rapid[3]), prog=int(list_rapid[4]), ranking=perfil)
                    Elo.objects.create(name=list_classical[0],games=int(list_classical[1]), rating=int(list_classical[2]), rd=int(list_classical[3]), prog=int(list_classical[4]), ranking=perfil)
                    login(request, user)
                    elo = user.nick.rankings.all()
                    print("elo",elo)
                    # informacion de todas las partidas
                    return render(request, 'Views/Home.html', {})
                else:
                    print("fallo en api lichess")
                    return render(request, 'Views/login.html', {})
        
    return render(request, 'Views/login.html', {})

def games(request, username):
    print("entre",username)
    # revisa si existe
    search_png = select_png(username)
    print("search_png",search_png)
    print("username",username)

    if search_png == 0:
        png = all_games(username)
        print("png",png.status_code)

    #elif search_png == 1:
    #    opcion = input("¿Desea actualizar?")

    list_info, list_game = data_split(username)
    list_white, list_black, list_result, list_ECO, list_Opening = split_Header(list_info)
    tupla_color, mov_white, mov_black = split_color(list_game)
    print("list_info",len(list_info))
    print("list_game",len(list_game))
    print("list_white",len(list_white))
    print("list_black",len(list_black))
    print("list_result",len(list_result))
    print("list_ECO",len(list_ECO))
    print("list_Opening",len(list_Opening))
    print("tupla_color",len(tupla_color))
    print("mov_white",len(mov_white))
    print("mov_black",len(mov_black))
    perfil = Perfil.objects.all()
    for c in perfil:
        print("c",c)
        print("c",c.username)
        nombre = c.username
        print("c",type(c.username))
    
    #consulta = Perfil.objects.filter(username=nombre)
    #print("consulta",consulta)

    nick = User.objects.get(username=username)
    print("usuario",nick)
    print("usuario",nick.nick)
    print("usuario",nick.nick.rated)
    apertura = opening.objects.create(eco_ww = '1', eco_dw = '2',eco_lw = '3',eco_b = '4',eco_db = '5',eco_lb = '6',n_eco_ww = 1,n_eco_dw=2,n_eco_lw = 3,n_eco_b = 4,n_eco_db = 5,n_eco_lb = 6)
    science = DataAnalyst.objects.create(games = '1', win_w = 1,draw_w = 1,lose_w = 1,win_b = 1,draw_b = 1,lose_b = 1,opening=apertura)
    titulos = Header.objects.create(event='1',site='2',date='3',white = '3', elo_w= '4',elo_b='6', black = '5' ,result = '7',variant='8', eco = '9', opening='10',scienc=science)
    movimientos = Moves.objects.create(white = '1', black = '2')
    partidas = Games.objects.create(header_game = '1', move_game = '2', header = titulos, moves = movimientos)
    nick.nick.num_game = partidas
    print("nick.nick.num_game",nick.nick.num_game)
    nick.save()
    #perfil = Perfil.objects.filter(username=nombre)
    #print("perfil",perfil)

    '''for i in len(list_info):
        print("i",i)
        movimientos = Moves.objects.create(white = mov_white[i], black = mov_black[i])
        titulos = Header.objects.create(white = list_white[i], black = list_black[i], result = list_result[i], eco = list_ECO[i], opening= list_Opening[i])
        perfil = Games.objects.create(header_game = list_info[i], move_game = list_game[i], header = titulos, moves = movimientos)
        usario(num_game=perfil)'''


    #print("Termino de registrar",usario)
    return render(request, 'Views/games.html', {})

def Home(request):
    return render(request, 'Views/Home.html', {})