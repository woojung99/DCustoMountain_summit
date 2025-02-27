import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import sqlite3

mtn_name_list = [] # 산 이름 리스트

location_name_list = [] # 지역 이름 리스트
leadtime_list = [] # 산행 기간 리스트
mtn_height_list = [] # 산 높이 리스트
mtn_difficulty_list = [] # 산 난이도 리스트
mtn_img_list = [] # 산 사진주소 리스트
detail_info_list = [] # 상세정보 리스트

class get_run_chrome_driver():
    def run_chrome_driver(url):
        # 크롬 드라이버 실행
        driver = webdriver.Chrome()
        
        driver.get(url)
        
        response = requests.get(url)
        
        # 에러 디버깅
        response.raise_for_status()
        
        # 10초 안에 웹페이지를 load하면 바로 넘어가거나, 10초를 기다림
        driver.implicitly_wait(10)
        return driver


class get_info():
    # 산 이름 가져오기
    def mtn_name(driver, mtn_name_list):
        mtn_names = driver.find_elements(By.CSS_SELECTOR, ".list_info strong")
        for mtn_name in mtn_names:
            mtn_name_list.append(mtn_name.text)
        
        return mtn_name_list

    # 지역, 산행기간, 산 높이, 산 난이도 가져오기
    def other_infos(driver, mtn_order):
        mtn_title = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtn_title[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")

        # 1: 지역
        result_value = result_name[1].string.replace(" ", "").replace("\t", "").replace("\n", "")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 공백('')을 추가
        if result_value != '':
            location_name_list.append(result_value)
        else:
            location_name_list.append('')
        # 7: 산행기간
        result_value = result_name[7].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            leadtime_list.append(result_value)
        else:
            leadtime_list.append('')
        # 9: 산높이
        result_value = result_name[9].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            mtn_height_list.append(result_value)
        else:
            mtn_height_list.append('')
        # 11: 산 난이도
        result_value = result_name[11].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            mtn_difficulty_list.append(result_value)
        else:
            mtn_difficulty_list.append('')
        
        return location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list
    
class getImg():
    def imgs(driver, mtn_order):
        mtn_title = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtn_title[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        defaltaddr = 'https://www.forest.go.kr'
        tag = soup.select("div.ps-list a")
        # 첫 번째 이미지의 주소
        imgsrc = tag[0].find("img")
        imgaddr = imgsrc.get("src")

        if imgaddr != '':
            mtn_img_list.append(defaltaddr + imgaddr)
        else:
            mtn_img_list.append('')

        return mtn_img_list
    
class get_detail_info():
    def detail_info(driver, mtn_order):
        mtn_title = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtn_title[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        tag = soup.select("div#txt p")

        if len(tag) > 1:
            detail_info_list.append(tag[1].text)
        else:
            detail_info_list.append('')

        return detail_info_list



url1 = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex="
urlpagenum = 1
urltail = "&searchMnt=&searchCnd=&mn=AR02_02_05_01&orgId=&mntUnit=10"

# 산이름GET START
for urlpagenum in range(1,11):
    driver = get_run_chrome_driver.run_chrome_driver(url1+f'{urlpagenum}'+urltail)
    mtn_name_list = get_info.mtn_name(driver, mtn_name_list)
print(mtn_name_list)
# 산이름GET END

# 지역, 산행기간, 산높이, 산 난이도GET START
for urlpagenum in range(1,11):
    for mtn_order in range(0,10):
        driver = get_run_chrome_driver.run_chrome_driver(url1+f'{urlpagenum}'+urltail)
        # 1: 지역
        # 7: 산행기간
        # 9: 산높이
        # 11: 산 난이도
        location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list = get_info.other_infos(driver, mtn_order)

for urlpagenum in range(1,11):
    for mtn_order in range(0,10):
        driver = get_run_chrome_driver.run_chrome_driver(url1+f'{urlpagenum}'+urltail)
        mtn_img_list = getImg.imgs(driver, mtn_order)

for urlpagenum in range(1,11):
    for mtn_order in range(0,10):
        driver = get_run_chrome_driver.run_chrome_driver(url1+f'{urlpagenum}'+urltail)
        detail_info_list = get_detail_info.detail_info(driver, mtn_order)


print(location_name_list)
print(leadtime_list)
print(mtn_height_list)
print(mtn_difficulty_list)
print(mtn_img_list)
print(detail_info_list)

# 지역, 산행기간, 산높이, 산 난이도GET END
#return mtn_name_list, location_name_list, leadtime_list, mtn_height_list, mtn_difficulty_list

con = sqlite3.connect(r'C:\Users\ITSC\git\DCustoMountain_summit\DCustoMountain\db.sqlite3')

cur = con.cursor()

# sql_columns = f"""INSERT INTO mountains_mountain(location,name,height,mtn_difficulty,leadtime,mtn_image) values"""
# print(sql_columns)

for i in range(len(mtn_name_list)):
    cur.execute(f"""INSERT INTO mountains_mountain(location,name,height,mtn_difficulty,leadtime,mtn_image, detail_info) values ('{location_name_list[i]}', '{mtn_name_list[i]}', '{mtn_height_list[i]}', '{mtn_difficulty_list[i]}', '{leadtime_list[i]}', '{mtn_img_list[i]}', '{detail_info_list[i]}');""")
    con.commit()

con.close()
