import pandas as pd
import re
from itertools import permutations
import pickle 

temp = "['Area Majority / Influence', 'Map Addition', 'Tile Placement']"

# list of columns
features = ['primary','alternate','yearpublished','minplayers','maxplayers','suggested_num_players','suggested_playerage', \
'suggested_language_dependence','playingtime','minage','boardgamecategory','boardgamemechanic','boardgamefamily', \
'average','bayesaverage','Board Game Rank','averageweight']
# dict of features and data type
features_dict = {}



def csv_str_to_list(csv_str):

    csv_str = re.sub("[|]|'", "", csv_str)
    csv_str = re.sub(" / ", "/", csv_str)
    csv_str_list = csv_str[1:-1].split(', ')

    return csv_str_list

if __name__ == '__main__':
    temp_csv_file = pd.read_csv('data\games_detailed_info.csv')
#     print(type(temp_csv_file['boardgamecategory'].apply(csv_str_to_list)[1]))
    # dict of features and data type
    features_dict = {}

    for feature in features:
        data_type = type(temp_csv_file[feature][0])
        features_dict[feature] = data_type
    print(features_dict)


    with open("data/features_dict.pickle","wb") as f:
        pickle.dump(features_dict, f)