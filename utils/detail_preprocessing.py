import pandas as pd
import numpy as np
import re
from itertools import permutations
import pickle 
from collections import OrderedDict

# list of columns
features = ['primary','minplayers','maxplayers', 'playingtime','minage','boardgamecategory','boardgamemechanic','boardgamefamily', \
'bayesaverage','Board Game Rank','averageweight']

# load games data
game_raw_data = pd.read_csv('data/games_detailed_info.csv')[features]
game_raw_data_len = len(game_raw_data)
# game_raw_data.to_csv('data/preprocessed_games_info.csv')

# define features type 
features_dict = {}

for feature in features:
    data_type = type(game_raw_data[feature][0])
    features_dict[feature] = data_type

# with open("data/features_dict.pickle","wb") as f:
#     pickle.dump(features_dict, f)

# drop features with features type
game_raw_data['drop'] = False

for feature in features:
    for i in range(game_raw_data_len):
        if feature == 'Board Game Rank':
            continue
        if type(game_raw_data[feature][i]) != features_dict[feature] and str(game_raw_data[feature][i]) != 'nan':
            game_raw_data['drop'][i] = True
            # print(f'problem at {feature} in raw {i}')

print(game_raw_data[game_raw_data['drop'] == True])

print(type(game_raw_data['Board Game Rank'][21630]))

# check indented data raw
for i in game_raw_data['suggested_language_dependence']:
    # if i == 30:
    if type(i) == float or type(i) == int or 'Order' not in i:
    # if type(i) != int:
        print(f'type: {type(i)} / item: {i}')

# check boardgamecategory # 283
nan_category_count = 0
for i in game_raw_data['boardgamecategory']:
    if str(i) == 'nan':
        print(f'type: {type(i)} / item: {i}')
        nan_category_count += 1

# check min/max player # 0
nan_player_count = 0
for i in game_raw_data['maxplayers']:
    if str(i) == 'nan' or type(i) != int:
        print(f'type: {type(i)} / item: {i}')
        nan_player_count += 1

# check playingtime # 0
nan_playingtime_count = 0
for i in game_raw_data['playingtime']:
    if str(i) == 'nan' or type(i) != int:
        print(f'type: {type(i)} / item: {i}')
        nan_playingtime_count += 1

# check minage # 0
nan_minage_count = 0
for i in game_raw_data['minage']:
    if str(i) == 'nan' or type(i) != int:
        print(f'type: {type(i)} / item: {i}')
        nan_minage_count += 1

# check bayesaverage # 0
nan_bayesaverage_count = 0
for i in game_raw_data['bayesaverage']:
    if str(i) == 'nan' or type(i) != float:
        print(f'type: {type(i)} / item: {i}')
        nan_bayesaverage_count += 1

# check boardgame Rank # NotRanked=5
## fix data type (str -> int)
nan_rank_count = 0
for i in range(len(game_raw_data['Board Game Rank'])):
    item = game_raw_data['Board Game Rank'][i]
    if type(item) == str and item != 'Not Ranked':
        game_raw_data['Board Game Rank'][i] = int(item)
    item = game_raw_data['Board Game Rank'][i]
    if str(item) == 'nan' or type(item) != int:
        print(f'type: {type(i)} / item: {item}')
        nan_rank_count += 1

# check averageweight # 0
nan_averageweight_count = 0
for i in game_raw_data['averageweight']:
    if str(i) == 'nan' or type(i) != float:
        print(f'type: {type(i)} / item: {i}')
        nan_averageweight_count += 1


game_raw_data.to_csv('data/preprocessed_games_info.csv')



