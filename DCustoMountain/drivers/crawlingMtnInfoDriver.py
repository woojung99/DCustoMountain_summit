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

# 산 이름 가져오기
class getMtnName():
    def mtnName(driver, mtnNameList):
        mtn_names = driver.find_elements(By.CSS_SELECTOR, ".list_info strong")
        for mtn_name in mtn_names:
            mtnNameList.append(mtn_name.text)
        
        return mtnNameList

# 지역 가져오기
class getRegionName():
    def regionName(driver, regionNameList, region_order):
        
        mtnTitle = driver.find_elements(By.CSS_SELECTOR, "ul.lst_thumb a")
        mtnTitle[region_order].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        region_name = soup.select("table.tbl td")
        # 지역명이 있는 경우만 리스트에 추가, 없는 경우는 None을 추가
        if region_name is not None or '':
            regionNameList.append(region_name[1].string.strip())
        else:
            regionNameList.append(None)

        return regionNameList



class getMainDriver():
    url1 = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex="
    urlpagenum = 1
    urltail = "&searchMnt=&searchCnd=&mn=AR02_02_05_01&orgId=&mntUnit=10"
    mtnNameList = [] # 산 이름 리스트
    regionNameList = [] # 지역 이름 리스트

    for urlpagenum in range(1,11):
        driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
        
        # 산 이름 가져오기
        mtnNameList = getMtnName.mtnName(driver, mtnNameList)
    
    # 산 이름 리스트
    print(mtnNameList)


    for urlpagenum in range(1,11):
        for region_order in range(0,10):
            # 지역
            driver = getRunChromeDriver.runChromeDriver(url1+f'{urlpagenum}'+urltail)
            regionNameList = getRegionName.regionName(driver, regionNameList, region_order)

    # 지역 이름 리스트
    print(regionNameList)


