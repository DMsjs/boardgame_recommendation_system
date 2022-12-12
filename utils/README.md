# boardgame_recommendation_system
2022-2 서울대학교 [데이터 분석과 시각화] 최종 프로젝트를 위한 repository입니다.


[API 사용 가이드]
  
1. utils/get_from_api.py  
    - API에서 받아온 raw data들을 가공하여 output을 내는 함수들을 모아놓은 파일입니다.
    - 소스코드 각 함수 아래에 output 형식을 메모해두었습니다. import 해서 사용 시 참고 바랍니다.
    - network 입력 데이터: df = direct_network_input()

2. API 바로 이용(requests 라이브러리 사용)
    1) data 폴더에 아래 csv 파일 저장
        - 2022-01-08.csv: 게임 기본 데이터
        - review_lang_included.csv: 게임 리뷰 데이터
        - detailed_with_tsne.csv: 게임 상세 데이터 (network input에 필요한 추가 컬럼 포함)
        - games.csv
        - tsne_game_info5.csv: network 입력 데이터
    2) app.py 실행 (app.py가 있는 경로에서 $ flask run)
    3) requests 라이브러리 이용하여 API 호출
        - 기본/리뷰/상세 데이터: http://127.0.0.1:5000/api 주소로 시작, data-source 및 기타 key와 함께 요청 (입력값은 무조건 전체 string)
            requests.get('http://127.0.0.1:5000/api?data-source=detailed-data&game-id=30549').json()
        - 전체 게임 id 리스트:
            requests.get('http://127.0.0.1:5000/game_list?mode=all').json()
