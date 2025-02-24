import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

class getMtnName():
    # 산 이름 가져오기
    def mtnName(driver, mtnNameList):
        mtn_names = driver.find_elements(By.CSS_SELECTOR, ".list_info strong")
        for mtn_name in mtn_names:
            mtnNameList.append(mtn_name.text)
        
        return mtnNameList

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
    

class mainDriver():
    url1 = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex="
    urlnum = "1"
    urltail = "&searchMnt=&searchCnd=&mn=AR02_02_05_01&orgId=&mntUnit=10"
    mtnNameList = []

    driver = getRunChromeDriver.runChromeDriver(url1+urlnum+urltail)
    
    # 산 이름 가져오기
    mtnNameList = getMtnName.mtnName(driver, mtnNameList)

    print(mtnNameList)