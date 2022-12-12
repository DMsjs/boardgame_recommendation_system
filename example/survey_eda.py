import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('mode.chained_assignment',  None)

survey_df = pd.read_csv('data/survey.csv')
survey_df.columns = ['time', 'gender', 'age', 'children', 'exp', 'hardship', 'will', 'comment']

def text2list(t):
    t_list = t.split(', ')
    return t_list

survey_df['hardship'] = survey_df['hardship'].apply(text2list)

hardship_set = []
for i in range(len(survey_df)):
    hardship_set += survey_df['hardship'][i]

hardship_set = set(hardship_set)
hardship_set
formal_hardship_list = [
    '보드게임 정보를 알기 어려웠다',
    '보드게임 룰 설명을 물어보기 어려웠다',
    '어떤 보드게임을 해야 할 지 모르겠다',
    '전에 했던 보드게임 이름을 몰라 찾지 못했다',
    '보드게임을 같이 할 사람을 구하지 못했다',
    '보드게임을 빌려서 다른 장소에서도 이용하고 싶었다',
    '없음'
]


for hardship_type in formal_hardship_list:
    survey_df[hardship_type] = 0

for i in range(len(survey_df)):
    for hardship_type in survey_df['hardship'][i]:
        if hardship_type in formal_hardship_list:
            survey_df[hardship_type][i] = 1

survey_df.to_csv('data/preprocessed_survey.csv')

hardship_summary = pd.DataFrame(survey_df[formal_hardship_list].sum()).T
hardship_count_df = pd.DataFrame({'hardship':[]})

for hardship_type in formal_hardship_list:
    for i in range(hardship_summary[hardship_type][0]):
        hardship_count_df.loc[len(hardship_count_df)] = [hardship_type]


import seaborn as sns

plt.figure(figsize=(15, 4))
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.xticks(rotation=0, fontsize=5)
sns.set_palette('Paired')
ax = sns.countplot(data=hardship_count_df, x='hardship')

for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2., height + 3, int(height), ha = 'center', size = 6)
# ax.set_ylim(0, 1200)
plt.savefig('data/Survey_Figure_1.png', dpi=300)

