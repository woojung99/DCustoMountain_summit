import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

mtnNameList = [] # 산 이름 리스트

locationNameList = [] # 지역 이름 리스트
leadTimeList = [] # 산행 기간 리스트
mtnHeightList = [] # 산 높이 리스트
mtnDifficultyList = [] # 산 난이도 리스트

class getRunChromeDriver():
    def runChromeDriver(url):
        # 크롬 드라이버 실행
        driver = webdriver.Chrome()
        
        driver.get(url)
        
        response = requests.get(url)
        
        # 에러 디버깅
        response.raise_for_status()
        
        # 10초 안에 웹페이지를 load하면 바로 넘어가거나, 10초를 기다림
        driver.implicitly_wait(10)
        return driver


class getInfo():
    # 산 이름 가져오기
    def mtnName(driver, mtnNameList):
        mtn_names = driver.find_elements(By.CSS_SELECTOR, ".list_info strong")
        for mtn_name in mtn_names:
            mtnNameList.append(mtn_name.text)
        
        return mtnNameList

    # 지역, 산행기간, 산 높이, 산 난이도 가져오기
    def otherInfos(driver, mtn_order):
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")

        # 1: 지역
        result_value = result_name[1].string.replace(" ", "").replace("\t", "").replace("\n", "")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        if result_value != '':
            locationNameList.append(result_value)
        else:
            locationNameList.append(None)
        # 7: 산행기간
        result_value = result_name[7].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            leadTimeList.append(result_value)
        else:
            leadTimeList.append(None)
        # 9: 산높이
        result_value = result_name[9].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            mtnHeightList.append(result_value)
        else:
            mtnHeightList.append(None)
        # 11: 산 난이도
        result_value = result_name[11].string.replace(" ", "").replace("\t", "").replace("\n", "")
        if result_value != '':
            mtnDifficultyList.append(result_value)
        else:
            mtnDifficultyList.append(None)
        
        return locationNameList, leadTimeList, mtnHeightList, mtnDifficultyList

class getMainDriver():
    url1 = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex="
    urlpagenum = 1
    urltail = "&searchMnt=&searchCnd=&mn=AR02_02_05_01&orgId=&mntUnit=10"

    # 산이름GET START
    for urlpagenum in range(1,11):
        driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
        mtnNameList = getInfo.mtnName(driver, mtnNameList)
    print(mtnNameList)
    # 산이름GET END

    # 지역, 산행기간, 산높이, 산 난이도GET START
    for urlpagenum in range(1,11):
        for mtn_order in range(0,10):
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            # 1: 지역
            # 7: 산행기간
            # 9: 산높이
            # 11: 산 난이도
            locationNameList, leadTimeList, mtnHeightList, mtnDifficultyList = getInfo.otherInfos(driver, mtn_order)
    
    print(locationNameList)
    print(leadTimeList)
    print(mtnHeightList)
    print(mtnDifficultyList)
    print('THE END')
    # 지역, 산행기간, 산높이, 산 난이도GET END




