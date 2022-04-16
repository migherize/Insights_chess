import requests
import json
import os 

token = "lip_0obpMyLkJNap1lEFGZjA"
cabeceras = {'Authorization': 'Bearer lip_0obpMyLkJNap1lEFGZjA'}
base_url = "https://lichess.org/api"

def account():
    print("acoount")
    nick = requests.get(base_url+'/account',headers=cabeceras)
    print(nick.status_code)
    print(nick.content)
    print("----------------")
    return nick

def all_games():
    print("all_games")
    nick = requests.get(base_url+'/games/user/mherize?analysed=false&tags=true&clocks=true&evals=true&opening=true&perfType=ultraBullet%2Cbullet%2Cblitz%2Crapid%2Cclassical',headers=cabeceras)
    print(nick.status_code)
    print(nick.text)
    with open(os.path.join(os.getcwd(),'my-data.pgn'), "w") as f:
        f.write(nick.text)
    return nick