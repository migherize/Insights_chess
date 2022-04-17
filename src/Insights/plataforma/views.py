from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from .api_lichess import *
import json
# Create your views here.


# Create your views here.
def Home(request):
    return render(request, 'Views/base.html', {})

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
                elo = user.perfil.rankings.all()
                return render(request, 'Views/Home.html', {'elo': elo })
            else:
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
                    Foto.objects.create(ruta='../static/img/user.jpg',username=perfil)
                    print("list_blitz",list_blitz)
                    Elo.objects.create(nombre=list_blitz[0],games=int(list_blitz[1]), rating=int(list_blitz[2]), rd=int(list_blitz[3]), prog=int(list_blitz[4]), username=perfil)
                    Elo.objects.create(nombre=list_bullet[0],games=int(list_bullet[1]), rating=int(list_bullet[2]), rd=int(list_bullet[3]), prog=int(list_bullet[4]), username=perfil)
                    Elo.objects.create(nombre=list_rapid[0],games=int(list_rapid[1]), rating=int(list_rapid[2]), rd=int(list_rapid[3]), prog=int(list_rapid[4]), username=perfil)
                    Elo.objects.create(nombre=list_classical[0],games=int(list_classical[1]), rating=int(list_classical[2]), rd=int(list_classical[3]), prog=int(list_classical[4]), username=perfil)
                    login(request, user)
                    elo = user.perfil.rankings.all()
                    print("elo",elo)
                    # informacion de todas las partidas
                    partidas = all_games()
                    print("partidas",partidas.status_code)
                    print("partidas",partidas.text)
                    return render(request, 'Views/Home.html', {'elo': elo})
                else:
                    print("fallo en api lichess")
                    return render(request, 'Views/login.html', {})
        
    return render(request, 'Views/login.html', {})

def main(request):
    return render(request, 'Views/Home.html', {})