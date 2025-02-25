from mountains.models import Mountain

mtn_name_list = [] # 산 이름 리스트

location_name_list = [] # 지역 이름 리스트
leadtime_list = [] # 산행 기간 리스트
mtn_height_list = [] # 산 높이 리스트
mtn_difficulty_list = [] # 산 난이도 리스트

class register_info(mtn_name_list, location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list):
    # Mountain모델 DB등록
    for i in range(100):
        # Mountain 모델의 인스턴스 생성
        mountain = Mountain(
            location = location_name_list[i], 
            name = mtn_name_list[i], 
            height = mtn_height_list[i], 
            mtn_difficulty = mtn_difficulty_list[i], 
            leadtime = leadtime_list[i], 
        )

        # 데이터베이스에 저장
        mountain.save()
