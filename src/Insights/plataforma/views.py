from email import message
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
# Django Rest Framework
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from .api_lichess import *
from .data_enginner import *
import json
# engine data
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import scipy.cluster.hierarchy as shc
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering

# Variable Global
global_message = ''
global_color = 0

#Funciones
def insert_games(user,username):
    if user.nick.kind == 0:
        print("manual")
        change_user(username)

    list_info, list_game = data_split(username)
    list_white, list_black, list_ECO, list_Opening, list_result = split_Header(list_info)
    tupla_color, mov_white, mov_black = split_color(list_game)

    #print("list_info", len(list_info))
    #print("list_game", len(list_game))
    #print("list_white", len(list_white))
    #print("list_black", len(list_black))
    #print("list_result", len(list_result))
    #print("list_ECO", len(list_ECO))
    #print("list_Opening", len(list_Opening))
    #print("tupla_color", len(tupla_color))
    #print("mov_white", len(mov_white))
    #print("mov_black", len(mov_black))
    print("usuario", user)
    print("usuario", user.nick)
    print("rated", user.nick.id)

    df = pd.DataFrame(list(zip(list_white, list_black, list_result, list_ECO, list_Opening)), columns=[
                    'Blancas', 'Negras', 'Result', 'ECO', 'Opening'])
    codigo_white_win, num_white_win, codigo_black_win, num_black_win, codigo_white_draw, num_white_draw, codigo_black_draw, num_black_draw, codigo_white_lose, num_white_lose, codigo_black_lose, num_black_lose, win_white, draw_white, lose_white, win_black, draw_black, lose_black,opening_white_win,opening_black_win,opening_white_draw,opening_black_draw,opening_white_lose,opening_black_lose = split_dataframe(
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
                                    name_eco_ww=opening_white_win,
                                    name_eco_dw=opening_black_win,
                                    name_eco_lw=opening_white_draw,
                                    name_eco_b=opening_black_draw,
                                    name_eco_db=opening_white_lose,
                                    name_eco_lb=opening_black_lose,
                                    data=science)

    #print("LLEGUE")
    #print(len(list_ECO),"list_ECO",list_ECO)
    #print(len(list_Opening),"list_Opening",list_Opening)
    #print(len(list_result),"list_result",list_result)
    #print(len(list_white),"list_white", list_white)
    #print(len(list_black),"list_black",list_black)

    for i in range(0,50):
        game = Games.objects.create(header_game = list_info[i], move_game = list_game[i], perfil_id = user.nick.id)
        titulos = Header.objects.create(event='1',site='2',date='3',white = list_white[i], elo_w= '4',elo_b='6', black = list_black[i] ,result = list_result[i],variant='8', eco = list_ECO[i], opening=list_Opening[i], game_id=game.id, scienc_id = science.id)
        movimientos = Moves.objects.create(white = mov_white[i], black = mov_black[i],game_id=game.id)

    scienc = user.nick.partidas.first().header.scienc_id
    print("scienc", scienc)
    data = DataAnalyst.objects.get(id=int(scienc))
    print("scienc", data.games)

def clean_dataframe(df):
    #dataframe = df.replace('-1', None).dropna()
    dataframe = df.replace('-1','0')
    dataframe = dataframe.set_index('Jugador')
    for index, column in enumerate(tuple(dataframe.columns)):
        if column == 'Jugador':
            continue
        
        if index < 7:
            continue
        
        for j,i in enumerate(dataframe[column]):
            data = float(i.replace('A','1.').replace('B','2.').replace('C','3.').replace('D','4.').replace('E','5.'))
            dataframe.iloc[j, index] = data
    
    print("salida clean_dataframe")
    print(dataframe)
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
        plt.axhline(y=20000,color='r',linestyle='--')
        plt.show()
        return

    plt.figure(figsize=(10,5))
    plt.title("Dendrograms")
    dend = shc.dendrogram(Clustering_Jeraruico)
    clusters = shc.fcluster(Clustering_Jeraruico, t=3, criterion='distance')
    print("clusters",clusters)
    plt.show()

#__________________________________________________________________
# cluster
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def do_cluster(df):
    #print(df.dtypes)
    cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    predict = cluster.fit_predict(df)
    #print("predict",predict)
    #print("predict",len(predict))
    
    # Grafica de Victoriass
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,7))
    plt.title('Cluster de victorias')
    plt.scatter(
        df['eco_ww_1'],
        df['eco_b_1'],
        c=cluster.labels_
    )
    #plt.show()
    plt.tight_layout()
    graph = get_graph()
    plt.savefig("cluster.png")
    
    '''
    # Grafica de derrotas
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,7))
    plt.scatter(
        df['Perdidas Blancas'],
        df['Perdidas Negras'],
        c=cluster.labels_
    )
    #plt.show()
    plt.savefig("cluster_2.png")
    '''
    bank_cust = df.reset_index()
    clusterDF = pd.DataFrame(predict)
    clusterDF.columns = ['Cluster_predicted']
    combineDF = pd.concat([bank_cust,clusterDF],axis = 1).reset_index()
    combineDF = combineDF.drop(['index'],axis=1)
    print("combineDF")
    print(combineDF)
    return graph, predict

#__________________________________________________________________
# Ejecucion de codigo
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
    print("Vista Games")
    # Metodo manual
    if request.method == 'POST':
        print("archivo", request.FILES['title'].name)
        print("tamaño", request.FILES['title'].size)
        name = username + '.pgn'
        fs = FileSystemStorage()
        fs.save(name, request.FILES['title'])
            
    # Busca el PGN si existe
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

    else:
        user = User.objects.get(username=username)
        print("kind",user.nick.kind)
        insert_games(user,username)
    
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
    print("aperturas",type(data.data_ciencia))
    return render(request, 'Views/estadisticas.html', {'elo': elo , 'data': data})

def insight(request, username):
    user = User.objects.get(username=username)
    elo = user.nick.rankings.all()
    scienc = user.nick.partidas.first().header.scienc_id
    user_info = DataAnalyst.objects.get(id=int(scienc))

    v_blanca = str(user_info.data_ciencia.eco_ww).split(',')
    v_nombre_blanca = str(user_info.data_ciencia.name_eco_ww).split(',')
    v_num_blanca = str(user_info.data_ciencia.n_eco_ww).split(',')
    v_negra = str(user_info.data_ciencia.eco_b).split(',')
    v_nombre_negra = str(user_info.data_ciencia.name_eco_b).split(',')
    v_num_negra = str(user_info.data_ciencia.n_eco_b).split(',')

    user_aperturas = []
    user_aperturas.append(v_blanca[0])
    user_aperturas.append(v_nombre_blanca[0])
    user_aperturas.append(v_num_blanca[0])
    user_aperturas.append(v_negra[0])
    user_aperturas.append(v_nombre_negra[0])
    user_aperturas.append(v_num_negra[0])

    dias =["v_blanca","v_nombre_blanca","v_num_blanca","v_negra","v_nombre_negra","v_num_negra"]
    list_aperturas = {dias:temp for (dias,temp) in zip(dias,user_aperturas)}
    
    # DataAnalyst
    data = DataAnalyst.objects.all().select_related('data_ciencia')
    list_value = list(data.values())
    
    # Aperturas
    data2 = opening.objects.all()
    list_value2 = list(data2.values())

    result = data.values()
    list_result = [entry for entry in result]
    list_user = []

    for d in data:
        if d.data_analisis.first():
            user = d.data_analisis.first().game.perfil.username.username
        else:
            print("No existe",d)
        list_user.append(user)

   

    df = pd.DataFrame(list_value)
    df2 = pd.DataFrame(list_value2)

    # Limpieza para calculo de Insight
    df2 = df2.drop(['name_eco_ww', 'name_eco_dw', 'name_eco_lw','name_eco_b','name_eco_db','name_eco_lb','n_eco_ww','n_eco_dw','n_eco_lw','n_eco_b','n_eco_db','n_eco_lb'], axis=1)
    
    # Separar las 3 mejores aperturas por color
    df2[['eco_ww_1','eco_ww_2','eco_ww_3']] = df2.eco_ww.str.split(pat=',',expand=True)
    df2[['eco_dw_1','eco_dw_2','eco_dw_3']] = df2.eco_dw.str.split(pat=',',expand=True)
    df2[['eco_lw_1','eco_lw_2','eco_lw_3']] = df2.eco_lw.str.split(pat=',',expand=True)
    df2[['eco_b_1','eco_b_2','eco_b_3']] = df2.eco_b.str.split(pat=',',expand=True)
    df2[['eco_db_1','eco_db_2','eco_db_3']] = df2.eco_db.str.split(pat=',',expand=True)
    df2[['eco_lb_1','eco_lb_2','eco_lb_3']] = df2.eco_lb.str.split(pat=',',expand=True)
    
    # Borrar informacion no relevante para estudio
    df2 = df2.drop(['eco_ww', 'eco_dw', 'eco_lw','eco_b','eco_db','eco_lb'], axis=1)
    
    # Join en las 2 tablas de informacion
    inner_join = pd.merge(df, df2, how='inner',left_on='id',right_on='data_id')
    
    # Borrar id extras
    dataframe = inner_join.drop(['id_y','data_id'], axis=1)
    dataframe = dataframe.rename(columns= {'id_x':'Jugador'})

    # Limpieza de data valores indeseados (-1, none)  
    try:
        dataframe = clean_dataframe(dataframe)
    except Exception as e:
        print(e)
        print('Error en la funcion "clean_dataframe"\n')   

    print("clean_dataframe")
    print(dataframe)
    dataframe.to_csv('example.csv')
    
    NORMALIZE = False
    try:
        if NORMALIZE:
            dataframe_normalize = normalize(dataframe)
        else:
            dataframe_normalize = dataframe
    
    except Exception as e:
        print(e)
        print('Error en la normalizacion')
    
    scaled_df = pd.DataFrame(dataframe_normalize, columns= dataframe.columns)
    print(scaled_df.columns)
    print("scaled_df")
    print(scaled_df)

    scaled_df2 = scaled_df[[
       'eco_ww_1', 'eco_dw_1', 
       'eco_lw_1', 'eco_b_1',
       'eco_db_1', 'eco_lb_1']]
    
    print("scaled_df2",scaled_df2)

    #dividing_line = True
    #corte_t = 0.06

    try:
       graph, cluster = do_cluster(scaled_df2)
    except Exception as e:
        print(e)
        print('Error en la funcion "do_cluster"\n')
    
    print("user",username)
    for y,x in enumerate(list_result):
        x["user"] = list_user[y]
        x["cluster"] = cluster[y]
        if x["user"] == username:
            user_estilo = str(x["cluster"])

    print("user_estilo",user_estilo)

    len_user = len(list_result)
    return render(request, 'Views/estilo.html', {'elo': elo , 'data': data, 'list_aperturas':list_aperturas,'user_info':user_info, 'user_estilo': user_estilo, 'list_result':list_result, 'len_user':len_user, 'graph':graph})