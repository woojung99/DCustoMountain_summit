import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

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

    # 지역 가져오기
    def locationName(driver, locationNameList, mtn_order):
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        result_value = result_name[1].string.strip()
        if result_value != '':
            locationNameList.append(result_value)
        else:
            locationNameList.append(None)

        return locationNameList

    # 산행기간 가져오기
    def periodMtnName(driver, periodList, mtn_order):
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        result_value = result_name[7].string.strip()
        if result_name != '':
            periodList.append(result_value)
        else:
            periodList.append(None)

        return periodList
    
    # 산 높이 가져오기
    def mtnHeight(driver, mtnHeightList, mtn_order):
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        result_value = result_name[9].string.strip()
        if result_name != '':
            mtnHeightList.append(result_value)
        else:
            mtnHeightList.append(None)

        return mtnHeightList
    
    # 산 난이도 가져오기
    def mtnDifficulty(driver, mtnDifficultyList, mtn_order):
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[mtn_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        result_name = soup.select("table.tbl td")
        # 결괏값이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        result_value = result_name[11].string.strip()
        if result_name != '':
            mtnDifficultyList.append(result_value)
        else:
            mtnDifficultyList.append(None)

        return mtnDifficultyList



class getMainDriver():
    url1 = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex="
    urlpagenum = 1
    urltail = "&searchMnt=&searchCnd=&mn=AR02_02_05_01&orgId=&mntUnit=10"
    mtnNameList = [] # 산 이름 리스트
    locationNameList = [] # 지역 이름 리스트
    periodList = [] # 산행 기간 리스트
    mtnHeightList = []
    mtnDifficultyList = []

    # 산이름GET START
    for urlpagenum in range(1,11):
        driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
        mtnNameList = getInfo.mtnName(driver, mtnNameList)
    print(mtnNameList)
    # 산이름GET END

    # 지역이름GET START
    for urlpagenum in range(1,11):
        for mtn_order in range(0,10):
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            locationNameList = getInfo.locationName(driver, locationNameList, mtn_order)

    print(locationNameList)
    # 지역이름GET END

    # 산행기간GET START
    for urlpagenum in range(1,11):
        for mtn_order in range(0,10):
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            periodList = getInfo.periodMtnName(driver, periodList, mtn_order)

    print(periodList)
    # 산행기간GET END

    # 산높이GET START
    for urlpagenum in range(1,11):
        for mtn_order in range(0,10):
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            mtnHeightList = getInfo.periodMtnName(driver, mtnHeightList, mtn_order)

    print(mtnHeightList)
    # 산높이GET END
    
    # 난이도GET START
    for urlpagenum in range(1,11):
        for mtn_order in range(0,10):
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            mtnDifficultyList = getInfo.mtnDifficulty(driver, mtnDifficultyList, mtn_order)

    print(mtnDifficultyList)
    # 난이도GET END




