from email import message
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from .api_lichess import *
from .data_enginner import *
import json

# Variable Global
global_message = ''
global_color = 0

#Funcion
def insert_games(user,username):
    if user.nick.kind == 0:
        print("manual")
        change_user(username)

    list_info, list_game = data_split(username)
    list_white, list_black, list_result, list_ECO, list_Opening = split_Header(list_info)
    tupla_color, mov_white, mov_black = split_color(list_game)

    print("list_info", len(list_info))
    print("list_game", len(list_game))
    print("list_white", len(list_white))
    print("list_black", len(list_black))
    print("list_result", len(list_result))
    print("list_ECO", len(list_ECO))
    print("list_Opening", len(list_Opening))
    print("tupla_color", len(tupla_color))
    print("mov_white", len(mov_white))
    print("mov_black", len(mov_black))
    print("usuario", user)
    print("usuario", user.nick)
    print("rated", user.nick.id)

    df = pd.DataFrame(list(zip(list_white, list_black, list_result, list_ECO, list_Opening)), columns=[
                    'Blancas', 'Negras', 'Result', 'ECO', 'Opening'])
    codigo_white_win, num_white_win, codigo_black_win, num_black_win, codigo_white_draw, num_white_draw, codigo_black_draw, num_black_draw, codigo_white_lose, num_white_lose, codigo_black_lose, num_black_lose, win_white, draw_white, lose_white, win_black, draw_black, lose_black = split_dataframe(
        df, str(username))

    science = DataAnalyst.objects.create(games=len(list_game), 
                                        win_w=win_white, 
                                        draw_w=draw_white,
                                        lose_w=lose_white, 
                                        win_b=win_black, 
                                        draw_b=draw_black, 
                                        lose_b=lose_black)

    apertura = opening.objects.create(eco_ww=codigo_white_win,
                                    eco_dw=codigo_white_draw,
                                    eco_lw=codigo_white_lose,
                                    eco_b=codigo_black_win,
                                    eco_db=codigo_black_draw, 
                                    eco_lb=codigo_black_lose,
                                    n_eco_ww=num_white_win,
                                    n_eco_dw=num_white_draw,
                                    n_eco_lw=num_white_lose, 
                                    n_eco_b=num_black_win, 
                                    n_eco_db=num_black_draw, 
                                    n_eco_lb=num_black_lose,
                                    data=science)

    for i in range(0,10):
        game = Games.objects.create(header_game = list_info[i], move_game = list_game[i], perfil_id = user.nick.id)
        titulos = Header.objects.create(event='1',site='2',date='3',white = list_white[i], elo_w= '4',elo_b='6', black = list_black[i] ,result = list_result[i],variant='8', eco = list_ECO[i], opening=list_Opening[i], game_id=game.id, scienc_id = science.id)
        movimientos = Moves.objects.create(white = mov_white[i], black = mov_black[i],game_id=game.id)

    scienc = user.nick.partidas.first().header.scienc_id
    print("scienc", scienc)
    data = DataAnalyst.objects.get(id=int(scienc))
    print("scienc", data.games)

# Vistas de Session

def Home(request):
    return render(request, 'Views/Home.html', {})

def base(request):
    return render(request, 'Views/base.html', {})

def main(request):
    return render(request, 'Views/main.html', {})

def signUp(request):
    global global_message, global_color
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                elo = user.nick.rankings.all()
                return render(request, 'Views/Home.html', {'elo': elo})
            else:
                print("Usuario no Registrado")
                message = "Usuario no Registrado"
                return render(request, 'Views/login.html', {'message': message})

        else:
            print("Formulario Invalido")
            message = "Formulario Invalido"
            return render(request, 'Views/login.html', {'message': message})

    else:
        print("Formulario No post")
        message = global_message
        color = global_color
        return render(request, 'Views/login.html', {'message': message, 'color':color})

def register(request):
    global global_message, global_color
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                print("Usuario ya registrado")
                message = "Usuario ya registrado"
                return render(request, 'Views/Register.html', {})
            else:
                print("Registro manual")
                # insert en DB
                email = 'correo@gmail.com'
                user = User.objects.create_user(username, email, password)
                perfil = Perfil.objects.create(url='None', rated='0', n_draw='0', n_loss='0', n_win='0',kind=0, username=user)
                Foto.objects.create(ruta='../static/img/user.jpg', perfil=perfil)
                Elo.objects.create(name='0', games=int('0'), rating=int('0'), rd=int('0'), prog=int('0'), perfil=perfil)
                message = "!Registro manual Exitoso!"
                color = 1
                global_message = message
                global_color = color
                return HttpResponseRedirect('/login/')

        else:
            print("formulario fallo")
            message = "formulario fallo"
            return render(request, 'Views/Register.html', {})

    return render(request, 'Views/Register.html', {})

def register_lichess(request):
    global global_message, global_color

    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("usario",username)
            user = authenticate(username=username, password=password)
            if user:
                print("Usuario ya registrado")
                return render(request, 'Views/login.html', {})
            else:
                print("Api")
                get_account = account(username)
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
                                list_blitz.append(
                                    get_account.json()['perfs'][e][key])
                        elif e == 'bullet':
                            list_bullet.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_bullet.append(
                                    get_account.json()['perfs'][e][key])
                        elif e == 'rapid':
                            list_rapid.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_rapid.append(
                                    get_account.json()['perfs'][e][key])
                        elif e == 'classical':
                            list_classical.append(e)
                            for key in get_account.json()['perfs'][e]:
                                list_classical.append(
                                    get_account.json()['perfs'][e][key])
            
                    url_nick = str(get_account.json()['url'])
                    count = get_account.json()['count']
                    for key, value in count.items():
                        if key == 'rated' or key == 'draw' or key == 'loss' or key == 'win':
                            dict_count[key] = value

                    # insert en DB
                    email = 'correo@gmail.com'
                    user = User.objects.create_user(username, email, password)
                    perfil = Perfil.objects.create(
                        url=url_nick, rated=dict_count['rated'], n_draw=dict_count['draw'], n_loss=dict_count['loss'], n_win=dict_count['win'],kind=1, username=user)
                    Foto.objects.create(
                        ruta='../static/img/user.jpg', perfil=perfil)
                    Elo.objects.create(name=list_blitz[0], games=int(list_blitz[1]), rating=int(
                        list_blitz[2]), rd=int(list_blitz[3]), prog=int(list_blitz[4]), perfil=perfil)
                    Elo.objects.create(name=list_bullet[0], games=int(list_bullet[1]), rating=int(
                        list_bullet[2]), rd=int(list_bullet[3]), prog=int(list_bullet[4]), perfil=perfil)
                    Elo.objects.create(name=list_rapid[0], games=int(list_rapid[1]), rating=int(
                        list_rapid[2]), rd=int(list_rapid[3]), prog=int(list_rapid[4]), perfil=perfil)
                    Elo.objects.create(name=list_classical[0], games=int(list_classical[1]), rating=int(
                        list_classical[2]), rd=int(list_classical[3]), prog=int(list_classical[4]), perfil=perfil)
                    
                    print("Usuario registrado desde lichess")
                    message = "!Usuario registrado desde lichess Exitoso!"
                    color = 1
                    global_message = message
                    global_color = color
                    return HttpResponseRedirect('/login/')

                else:
                    print("fallo en api lichess")
                    print("Error: ", get_account.status_code)
                    return render(request, 'Views/Register.html', {})
        else:
            print("fallo en api lichess")
            return render(request, 'Views/Register.html', {})
    
    return render(request, 'Views/Register_lichess.html', {})

def signOut(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# Vistas de usuario
def games(request, username):
    print("entre")
    if request.method == 'POST':
        print("archivo", request.FILES['title'].name)
        print("tamaño", request.FILES['title'].size)
        name = username + '.pgn'
        fs = FileSystemStorage()
        fs.save(name, request.FILES['title'])
            
    # revisa si existe
    search_png = select_png(username)
    print("search_png", search_png)
    print("username", username)

    if search_png == 0:
        png = all_games(username)
        print("png", png.status_code)
        if len(png.text) == 0:
            print("No existe partidas o 0 partidas")
            user = User.objects.get(username=username)
            elo = user.nick.rankings.all()
            message = "!No existe partidas o 0 partidas!"
            return render(request, 'Views/games.html', {'elo': elo, 'message':message})

        else:
            user = User.objects.get(username=username)
            print("kind",user.nick.kind)
            insert_games(user,username)
            return HttpResponseRedirect('/view_games/%s/' % user)


    # elif search_png == 1:
    #    opcion = input("¿Desea actualizar?")
    print("pase")
    print("pase",username)
    return HttpResponseRedirect('/view_games/%s/' % username)


def view_games(request, username):
    if request.method == 'GET':
        print("request.method",request.method)
        user = User.objects.get(username=username)
        games = user.nick.partidas.first()
        print("games",games)
        if games:
            user = User.objects.get(username=username)
            elo = user.nick.rankings.all()
            scienc = user.nick.partidas.first().header.scienc_id
            data = DataAnalyst.objects.get(id=int(scienc))
            print("enviar")
            return render(request, 'Views/view_games.html', {'elo': elo , 'data': data})
        
        else:
            message = "No hay partidas"
            print(message)
            return render(request, 'Views/games.html', {'message': message })
    
    if request.method == 'POST':
        print("archivo", request.FILES['title'].name)
        print("tamaño", request.FILES['title'].size)
        name = username + '.pgn'
        fs = FileSystemStorage()
        fs.save(name, request.FILES['title'])
        message = "Partidas Cargadas"
        print(message)
        user = User.objects.get(username=username)
        if user.nick.kind == 0:
            print("verificar user")

        insert_games(user,username)
        return HttpResponseRedirect('/view_games/%s/' % user)

    
def estadisticas(request, username):
    user = User.objects.get(username=username)
    print("kind",user.nick.kind)
    elo = user.nick.rankings.all()
    scienc = user.nick.partidas.first().header.scienc_id
    data = DataAnalyst.objects.get(id=int(scienc))
    print("Id",scienc)
    #data = opening.objects.get(id=int(aperturas.opening))
    return render(request, 'Views/estadisticas.html', {'elo': elo , 'data': data})

def insight(request, username):
    user = User.objects.get(username=username)
    elo = user.nick.rankings.all()
    # Insight
    data = DataAnalyst.objects.all()
    result = data.values()
    list_result = [entry for entry in result]
    list_user = []

    for d in data:
        if d.data_analisis.first():
            print("user",d.data_analisis.first())
            user = d.data_analisis.first().game.perfil.username.username
        else:
            print("No existe",d)
        list_user.append(user)

    #print("parse",data.values())
    #result = data.values()
    print(type(list_result),"list_result",list_result)
    print("list_user",type(list_user),list_user)

    for y,x in enumerate(list_result):
        x["user"] = list_user[y]
        print(type(x),"l",x)

    len_user = len(list_result)

    return render(request, 'Views/estilo.html', {'elo': elo , 'data': data, 'list_result':list_result, 'len_user':len_user})

    #models.objects.count()
    #models.objects.first()
    #models.objects.last()



    #print("query",str(data.query))
    
    #for d in data:
    #    #print("todo",d)
    #    #print("id",d.id, type(d.id))
    #    #print("user",d.data_analisis.first().game.perfil.username.username)
    #    #print("user",type(d.data_analisis.first().game.perfil.username.username))
        
    #filter = DataAnalyst.objects.filter(data_analisis__game_id__perfil_id__id=1)
    #print("filter",str(filter.query))
    
    #filter = DataAnalyst.objects.all().select_related('data_ciencia')
    #print("select_related",str(filter.query))

    #print("filter",filter)

    #busqueda = DataAnalyst.objects.filter(opening = 67)
    #print("busqueda",busqueda)
    
    #result = DataAnalyst.objects.values()
    #list_result = [entry for entry in result]
    #print("list_result",list_result)
    #for l in list_result:
    #    print("l",l)
    #    print("l",l.data_analisis.first().game.perfil.username.username)

    #data = opening.objects.get(id=int(aperturas.opening))