import pandas as pd
import numpy as np
from tqdm import tqdm
import networkx as nx
from sklearn.manifold import TSNE
from itertools import permutations

from network_utils import cos_sim


class Game():
    def __init__(self, df):
        self.primary = df['primary']
        self.players = {'minplayers': df['minplayers'], 'maxplayers': df['maxplayers']}
        self.minage = df['minage']
        if type(df['boardgamecategory']) == float:
            self.boardgamecategory = []
        else:
            self.boardgamecategory = eval(df['boardgamecategory'])

        if type(df['boardgamemechanic']) == float:
            self.boardgamemechanic = []
        else:
            self.boardgamemechanic = eval(df['boardgamemechanic'])

        if type(df['boardgamefamily']) == float:
            self.boardgamefamily = []
        else:
            self.boardgamefamily = eval(df['boardgamefamily'])

        self.bayesaverage = df['bayesaverage']
        if type(df['Board Game Rank']) == str:
            self.rank = 99999
        else:
            self.rank = df['Board Game Rank']
        self.averageweight = df['averageweight']

class GameNetwork():
    def __init__(self, df):
        self.game_df = df
        self.game_dict = {}
        self.category_set = set()
        self.mechanic_set = set()
        self.family_set = set()
        for i in range(len(df)):
            self.game_dict[df.iloc[i, 1]] = Game(df.iloc[i, :])
            self.category_set.update(self.game_dict[df.iloc[i, 1]].boardgamecategory)
            self.mechanic_set.update(self.game_dict[df.iloc[i, 1]].boardgamemechanic)
            self.family_set.update(self.game_dict[df.iloc[i, 1]].boardgamefamily)
    def category_network(self):
        self.category_link = pd.DataFrame({'Source':[], 'Target':[], 'Value':[]})

        # define category <-> label
        category_to_label = {}
        label_to_category = {}
        for i, category in enumerate(self.category_set):
            category_to_label[category] = i
            label_to_category[i] = category

        # define category link
        for i in tqdm(range(len(self.category_set))):
            category_name = label_to_category[i]
            game_in_category = []
            for game in self.game_dict.keys():
                game_ojt = self.game_dict[game]
                if category_name in game_ojt.boardgamecategory:
                    game_in_category.append(game_ojt.primary)
              
            all_pair = list(permutations(game_in_category, 2))
            for source, target in tqdm(all_pair):
                self.category_link.loc[len(self.category_link)] = [source, target, 1]

        # define category network
        G = nx.Graph()
        for game in self.game_dict.keys():
            G.add_node(game, features=self.game_dict[game])
        for i in self.category_link.index:
            G.add_edge(self.category_link['Source'][i],self.category_link['Target'][i])

        return G    
    
    def category_tsne(self):

        self.category_one_hot_df = self.game_df.copy()

        for category in self.category_set:
            self.category_one_hot_df[category] = 0
        for i in range(len(self.category_one_hot_df)):

            if type(self.category_one_hot_df['boardgamecategory'].iloc[i]) == float:
                boardgamecategory = []
            else:
                boardgamecategory = eval(self.category_one_hot_df['boardgamecategory'].iloc[i])

            for category in boardgamecategory:
                self.category_one_hot_df[category][i] = 1
        
        self.category_one_hot_df.drop('boardgamecategory', axis=1)
        self.category_one_hot_df.drop('boardgamemechanic', axis=1)
        self.category_one_hot_df.drop('boardgamefamily', axis=1)
        
        # Tsne
        tsne_np = TSNE(n_components = 2).fit_transform(self.category_one_hot_df[list(self.category_set)])
        self.category_tsne_df = pd.DataFrame(tsne_np, columns = ['category_tsne_0', 'category_tsne_1'])

        return self.category_tsne_df
    
    def category_similarity(self, triggers, filter):
        '''
        filter:
        - minplayers
        - maxplayers
        - playingtime
        - minage
        - Board Game Rank
        - averageweight
        '''
        tsne_df = pd.read_csv('data/tsne_game_info.csv')


        sim_columns = ['minplayers','maxplayers','playingtime','minage','bayesaverage', \
            'Board Game Rank','averageweight', 'category_tsne_0', 'category_tsne_1']

        trigger_df = pd.DataFrame()
        for trigger in triggers:
            trigger_df = pd.concat([trigger_df,new_df[new_df['primary']==trigger]], axis=0)

        for feature, bound in filter.items():
            if feature in ['minplayers', 'playingtime', 'minage', 'Board Game Rank', 'averageweight']:
                tsne_df = tsne_df[tsne_df[feature]>=bound[0]]
            if feature in ['maxplayers', 'playingtime', 'Board Game Rank', 'averageweight']:
                tsne_df = tsne_df[tsne_df[feature]<=bound[1]]

        tsne_df['cossim_trigger1'] = 0.0
        tsne_df['cossim_trigger2'] = 0.0
        tsne_df['cossim_trigger3'] = 0.0

        for i in range(len(tsne_df)):
            tsne_df['cossim_trigger1'].iloc[i] = cos_sim(tsne_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[0, :].apply(float))
            tsne_df['cossim_trigger2'].iloc[i] = cos_sim(tsne_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[1, :].apply(float))
            tsne_df['cossim_trigger3'].iloc[i] = cos_sim(tsne_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[2, :].apply(float))

        
        return tsne_df

    def category_recommendation(self, triggers, filter):
        cos_sim_df = self.category_similarity(triggers, filter)
        trigger1_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger1'], ascending=False)[:10])
        trigger2_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger2'], ascending=False)[:10])
        trigger3_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger3'], ascending=False)[:10])

        return trigger1_recommend_df, trigger2_recommend_df, trigger3_recommend_df

    def category_recomm_network(self, triggers, filter):
        trigger1_recommend_df, trigger2_recommend_df, trigger3_recommend_df = self.category_recommendation(triggers, filter)
        trigger1_recommend_list, trigger2_recommend_list, trigger3_recommend_list = list(trigger1_recommend_df['primary']), list(trigger2_recommend_df['primary']), list(trigger3_recommend_df['primary'])

        # define category recommend network
        recomm_G = nx.Graph()
        for game in trigger1_recommend_list+trigger2_recommend_list+trigger3_recommend_list:
            recomm_G.add_node(game, features=self.game_dict[game])
        for game in trigger1_recommend_list:
            recomm_G.add_edge(triggers[0],game)
        for game in trigger2_recommend_list:
            recomm_G.add_edge(triggers[1],game)
        for game in trigger3_recommend_list:
            recomm_G.add_edge(triggers[2],game)

        return recomm_G




    





if __name__ == '__main__':

    df = pd.read_csv('data/preprocessed_games_info.csv')
    # filter
    # df = df[df['minplayers']>=4]
    # df = df[df['maxplayers']<=8]
    # df = df.reset_index(drop=True)
    game_network = GameNetwork(df)
    # category_tsne_df = game_network.category_tsne()
    # game_network.category_one_hot_df['boardgamecategory']

    # df_concated_tsne = pd.concat([df, category_tsne_df], axis=1)
    # df_concated_tsne.to_csv('data/tsne_game_info.csv')

    # import matplotlib.pyplot as plt


    # # target 별 시각화
    # plt.scatter(category_tsne_df['component 0'], category_tsne_df['component 1'], color = 'pink')


    # plt.xlabel('component 0')
    # plt.ylabel('component 1')
    # plt.legend()
    # plt.show()




    # trigger cossim
    new_df = pd.concat([df, category_tsne_df], axis=1)
    triggers = ['Puerto Rico', 'Battlestar Galactica: The Board Game', 'Catan']
    # trigger_df = pd.DataFrame()
    # for trigger in triggers:
    #     trigger_df = pd.concat([trigger_df,new_df[new_df['primary']==trigger]], axis=0)
    
    # sim_columns = ['minplayers','maxplayers','playingtime','minage','bayesaverage','Board Game Rank','averageweight']
    # new_df['cossim_category_trigger1'] = 0.0
    # for i in range(len(new_df)):
    #     new_df['cossim_category_trigger1'].iloc[i] = cos_sim(new_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[0, :].apply(float))

    # new_df.sort_values(by=['cossim_category_trigger1'], ascending=False)['primary']

    filter = {'minplayers': [2, 99999],'maxplayers':[0, 4],'playingtime': [60, 380],'minage':[4, 1000],'bayesaverage':[4,10],'Board Game Rank':[0, 10000],'averageweight':[2, 4]}

    # temp =  game_network.category_similarity(triggers, filter)

    # temp = temp.reset_index(drop=True)
    # temp.sort_values(by=['cossim_trigger2'], ascending=False)['boardgamecategory'][:10].to_csv('data/temp.csv')
    # temp.sort_values(by=['cossim_trigger1'], ascending=False)['primary'][:10]
    # temp.sort_values(by=['cossim_trigger2'], ascending=False)['primary'][:10]
    # temp.sort_values(by=['cossim_trigger3'], ascending=False)['primary'][:10]


    recomm_G = game_network.category_recomm_network(triggers=triggers, filter=filter)
    print(recomm_G.edges())

    # net visualize
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(recomm_G, k = 0.15)
    nx.draw_networkx(recomm_G,pos, node_size = 25, node_color = 'blue')
    plt.show()

    # recommend df
    recomm_df = game_network.category_recommendation(triggers=triggers, filter=filter)