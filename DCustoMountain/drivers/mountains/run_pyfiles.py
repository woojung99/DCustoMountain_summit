import crawling_mtnInfo_driver
import register_mtnInfo_to_db

def run_files():
    # 크롤링정보GET
    mtn_name_list, location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list = crawling_mtnInfo_driver.get_main_driver.init_driver()

    # 크롤링한 정보를 DB에 등록
    register_mtnInfo_to_db.register_info(mtn_name_list, location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list)

