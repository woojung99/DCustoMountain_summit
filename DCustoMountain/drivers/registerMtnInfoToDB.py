import crawlingMtnInfoDriver

class registerInfo():
    # 크롤링한 정보를 취득
    mtnNameList, locationNameList, leadTimeList, mtnHeightList, mtnDifficultyList = crawlingMtnInfoDriver.getMainDriver.initDriver()

    # 산정보 등록