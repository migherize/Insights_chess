import requests
import os 

token = os.getenv('token_lichess')
cabeceras = {'Authorization': 'Bearer {}'.format(token)}
split_path = '/Users/migherize/Sourcetree/InsightsChess/src/Insights/input'
base_url = "https://lichess.org/api"

def account(user):
    print("acoount")
    nick = requests.get(base_url+'/user/{}'.format(user),headers=cabeceras)
    print(nick.status_code)
    print(nick.content)
    print("----------------")
    return nick

def all_games(user):
    complement = '/games/user/{}?tags=true&clocks=false&evals=false&opening=true'.format(str(user).lower)
    print("complement",complement)
    nick = requests.get(base_url+complement,headers=cabeceras)
    print(nick.status_code)
    print("----------------")
    with open(os.path.join(split_path,('{}.pgn'.format(user))), 'w') as f:
        f.writelines(nick.text)
    return nick

def select_png(user):
    # Lectura de task de entrada
    input_api = os.listdir(split_path)
    for num,name in enumerate(input_api):
        if name == '.DS_Store':
            input_api.pop(num)

    if ('{}.pgn'.format(user)) in input_api:
        return 1
    
    return 0

#account()