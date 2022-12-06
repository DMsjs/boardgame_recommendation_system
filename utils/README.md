# boardgame_recommendation_system
2022-2 서울대학교 [데이터 분석과 시각화] 최종 프로젝트를 위한 repository입니다.


[utils 내부 파일 사용 가이드]
  
1. get_from_api.py  
    - id_name_df(): 게임 id, name 각각을 column으로 하는 dataframe 반환. 이 때 id에 해당하는 column은 각 값들이 리스트 형식으로 들어가있음 (예를들어 30549 -> [30549])
    - id_name_dict(): 게임 id를 key, name을 value로 하는 dictionary 반환
    - name_id_dict(): 게임 name을 key, id를 value로 하는 dictionary 반환