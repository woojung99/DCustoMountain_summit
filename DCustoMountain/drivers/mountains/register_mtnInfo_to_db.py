import sqlite3

mtn_name_list = [] # 산 이름 리스트
location_name_list = [] # 지역 이름 리스트
leadtime_list = [] # 산행 기간 리스트
mtn_height_list = [] # 산 높이 리스트
mtn_difficulty_list = [] # 산 난이도 리스트

con = sqlite3.connect(r'C:\Users\ITSC\git\DCustoMountain_summit\DCustoMountain\db.sqlite3')

cur = con.cursor()

sql_columns = f"""INSERT INTO mountains_mountain(location,name,height,mtn_difficulty,leadtime) values"""
print(sql_columns)

for i in range(len(mtn_name_list)):
    cur.execute(f"""INSERT INTO mountains_mountain(location,name,height,mtn_difficulty,leadtime) values ('{location_name_list[i]}', '{mtn_name_list[i]}', '{mtn_height_list[i]}', '{mtn_difficulty_list[i]}', '{leadtime_list[i]}');""")
    con.commit()

con.close()


