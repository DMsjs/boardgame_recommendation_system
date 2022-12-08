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

    # def category_network(self):
    #     self.category_link = pd.DataFrame({'Source':[], 'Target':[], 'Value':[]})

    #     # define category <-> label
    #     category_to_label = {}
    #     label_to_category = {}
    #     for i, category in enumerate(self.category_set):
    #         category_to_label[category] = i
    #         label_to_category[i] = category

    #     # define category link
    #     for i in tqdm(range(len(self.category_set))):
    #         category_name = label_to_category[i]
    #         game_in_category = []
    #         for game in self.game_dict.keys():
    #             game_ojt = self.game_dict[game]
    #             if category_name in game_ojt.boardgamecategory:
    #                 game_in_category.append(game_ojt.primary)
              
    #         all_pair = list(permutations(game_in_category, 2))
    #         for source, target in tqdm(all_pair):
    #             self.category_link.loc[len(self.category_link)] = [source, target, 1]

    #     # define category network
    #     G = nx.Graph()
    #     for game in self.game_dict.keys():
    #         G.add_node(game, features=self.game_dict[game])
    #     for i in self.category_link.index:
    #         G.add_edge(self.category_link['Source'][i],self.category_link['Target'][i])

    #     return G    
    
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
    
    def mechanic_tsne(self):

        self.mechanic_one_hot_df = self.game_df.copy()

        for mechanic in self.mechanic_set:
            self.mechanic_one_hot_df[mechanic] = 0
        for i in range(len(self.mechanic_one_hot_df)):

            if type(self.mechanic_one_hot_df['boardgamemechanic'].iloc[i]) == float:
                boardgamemechanic = []
            else:
                boardgamemechanic = eval(self.mechanic_one_hot_df['boardgamemechanic'].iloc[i])

            for mechanic in boardgamemechanic:
                self.mechanic_one_hot_df[mechanic][i] = 1
        
        self.mechanic_one_hot_df.drop('boardgamecategory', axis=1)
        self.mechanic_one_hot_df.drop('boardgamemechanic', axis=1)
        self.mechanic_one_hot_df.drop('boardgamefamily', axis=1)
        
        # Tsne
        tsne_np = TSNE(n_components = 2).fit_transform(self.mechanic_one_hot_df[list(self.mechanic_set)])
        self.mechanic_tsne_df = pd.DataFrame(tsne_np, columns = ['mechanic_tsne_0', 'mechanic_tsne_1'])

        return self.mechanic_tsne_df
    
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
        sim_columns = ['minplayers','maxplayers','playingtime','minage','bayesaverage', \
            'Board Game Rank','averageweight', 'category_tsne_0', 'category_tsne_1']

        trigger_df = pd.DataFrame()
        num_trigger = len(triggers)
        for trigger in triggers:
            trigger_df = pd.concat([trigger_df,self.game_df[self.game_df['primary']==trigger]], axis=0)

        filtered_game_df = self.game_df.copy()
        for feature, bound in filter.items():
            if feature in ['minplayers', 'playingtime', 'minage', 'Board Game Rank', 'averageweight']:
                filtered_game_df = filtered_game_df[filtered_game_df[feature]>=bound[0]]
            if feature in ['maxplayers', 'playingtime', 'Board Game Rank', 'averageweight']:
                filtered_game_df = filtered_game_df[filtered_game_df[feature]<=bound[1]]

        # filtered_game_df['cossim_trigger1'] = 0.0
        # filtered_game_df['cossim_trigger2'] = 0.0
        # filtered_game_df['cossim_trigger3'] = 0.0
        for i in range(num_trigger):
            filtered_game_df[f'cossim_trigger{i}'] = 0.0

        for i in range(len(filtered_game_df)):
            for j in range(num_trigger):
                filtered_game_df[f'cossim_trigger{j}'].iloc[i] = cos_sim(filtered_game_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[0, :].apply(float))
            # filtered_game_df['cossim_trigger1'].iloc[i] = cos_sim(filtered_game_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[0, :].apply(float))
            # filtered_game_df['cossim_trigger2'].iloc[i] = cos_sim(filtered_game_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[1, :].apply(float))
            # filtered_game_df['cossim_trigger3'].iloc[i] = cos_sim(filtered_game_df[sim_columns].iloc[i].apply(float), trigger_df[sim_columns].iloc[2, :].apply(float))

        
        return filtered_game_df

    def category_recommendation(self, triggers, filter, recommend_num):
        cos_sim_df = self.category_similarity(triggers, filter)
        recommend_df_dict = {}
        for i in range(len(triggers)):
            recommend_df_dict[triggers[i]] = cos_sim_df.sort_values(by=[f'cossim_trigger{i}'], ascending=False)[:recommend_num]
        # trigger1_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger1'], ascending=False)[:10])
        # trigger2_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger2'], ascending=False)[:10])
        # trigger3_recommend_df = (cos_sim_df.sort_values(by=['cossim_trigger3'], ascending=False)[:10])

        return recommend_df_dict

    def category_recomm_network(self, triggers, filter, recommend_num):
        recommend_df_dict = self.category_recommendation(triggers, filter, recommend_num)

        # define category recommend network
        recomm_G = nx.Graph()

        # add node
        for game in triggers:
            print(game)
            game_info = self.game_dict[game]
            recomm_G.add_node(game, features=game_info)
        for trigger in triggers:
            for game in list(recommend_df_dict[trigger]['primary']):
                game_info = self.game_dict[game]
                recomm_G.add_node(game, features=game_info)
                recomm_G.add_edge(trigger, game)

        return recomm_G




    





if __name__ == '__main__':
    '''

    df = pd.read_csv('data/tsne_game_info2.csv')

    game_network = GameNetwork(df)
    # mechanic_tsne_df = game_network.mechanic_tsne()
    # game_network.mechanic_one_hot_df['boardgamemechanic']

    # tsne_df = pd.read_csv('data/tsne_game_info2.csv')

    # df_concated_tsne = pd.concat([tsne_df, mechanic_tsne_df], axis=1)
    # df_concated_tsne = df_concated_tsne.drop([ 'Unnamed: 0'], axis=1)
    # df_concated_tsne.reset_index(drop=True)
    # df_concated_tsne.to_csv('data/tsne_game_info2.csv')

    # import matplotlib.pyplot as plt


    # # target 별 시각화
    # plt.scatter(df_concated_tsne['mechanic_tsne_0'], df_concated_tsne['mechanic_tsne_1'], color = 'pink', s=5)
    # plt.scatter(df_concated_tsne['category_tsne_0'], df_concated_tsne['category_tsne_1'], color = 'blue', s=5)


    # plt.xlabel('component 0')
    # plt.ylabel('component 1')
    # plt.legend()
    # plt.show()




    # trigger cossim
    triggers = ['Puerto Rico', 'Battlestar Galactica: The Board Game', 'Mombasa', 'Twilight Struggle']
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


    recomm_G = game_network.category_recomm_network(triggers=triggers, filter=filter, recommend_num=10)
    # game_network.category_similarity(triggers=triggers, filter=filter)

    print(recomm_G.edges())

    # net visualize
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(recomm_G, k = 0.15)
    nx.draw_networkx(recomm_G,pos, node_size = 25, node_color = 'blue')
    plt.show()
    '''
    ######################
    
    '''
    현종 이 밑으로 따라하면 됨 ㅇㅇㅇㅇ
    '''
    # input data 로드(tsne 칼럼 포함)
    df = pd.read_csv('data/tsne_game_info2.csv')
    # GameNetwork 객체 생성(게임 정보 및 네트워크 핸들링)
    game_network = GameNetwork(df)

    '''
    위에 객체 한번 만들어 놓기만 하면 아래 코드만 반복 실행하면 됨
    '''
    # trigger 설정(1, 2, 3개 설정)(사실 4개 이상도 되긴 함)
    triggers = ['Puerto Rico', 'Battlestar Galactica: The Board Game']
    # filter 설정
    filter = {'minplayers': [2, 99999],'maxplayers':[0, 4],'playingtime': [60, 380],'minage':[4, 1000],'bayesaverage':[4,10],'Board Game Rank':[0, 10000],'averageweight':[2, 4]}
    # 추천 게임 네트워크 도출(GameNetwork 내부 메서드 사용)
    recomm_G = game_network.category_recomm_network(triggers=triggers, filter=filter, recommend_num=10)
    # node 출력
    print(recomm_G.nodes())
    # edge 출력
    print(recomm_G.edges())

    # 추천 게임 네트워크 시각화
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(recomm_G, k = 0.15)
    nx.draw_networkx(recomm_G,pos, node_size = 25, node_color = 'blue')
    plt.show()



