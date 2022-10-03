import os 

token = os.getenv('token_lichess')
cabeceras = {'Authorization': 'Bearer {}'.format(token)}

# constanst
base_url = "https://lichess.org/api"
split_path = '/Users/migherize/Sourcetree/InsightsChess/src/Insights/media'
input_path = '/Users/migherize/SourceTree/InsightsChess/src/Data_enginner/input_request'
output_split_path = '/Users/migherize/SourceTree/InsightsChess/src/Data_enginner/output_split'
join_path = '/Users/migherize/SourceTree/InsightsChess/src/Data_enginner/join_split'
output = '/Users/migherize/SourceTree/InsightsChess/src/Data_enginner/output'
