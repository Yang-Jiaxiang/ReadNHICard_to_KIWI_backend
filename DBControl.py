from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime,timezone,timedelta
import json


load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")
MONGODB_PORT=os.getenv("MONGODB_PORT")

DBclient = MongoClient(MONGODB_URL+"/"+MONGODB_PORT)

DB_name="nec"

def Check_DB_Onnection():
    dblient=DBclient.list_database_names()

    if DB_name in dblient:
        return 200
    else:
        return 500

def Insert_DB(data):
    mydb = DBclient[DB_name]
    mycol = mydb["patients"]
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    now = dt2.strftime("%Y-%m-%d %H:%M:%S")
    roc_date_str = data['birth']
    # 將民國年轉換為西元年
    year = int(roc_date_str[:2]) + 1911
    print(year)
    # 將民國日期字串轉換為西元日期字串
    ad_date_str = str(year) + roc_date_str[2:]
    # 將西元日期字串轉換為datetime格式
    ad_date = datetime.strptime(ad_date_str, "%Y%m%d")

    # data = json.loads(json_data)
    data['gender'] = data['gender'].lower()
    data.pop('code')
    data.pop('cardDate')
    data["birth"]= ad_date
    data["createdAt"] = now
    data["updatedAt"] = now
    data["phone"]=""
    data["department"]=""

    try:
        # 查询数据库中是否已经存在该id
        existing_data = mycol.find_one({'id': data["id"]})
        # 如果存在，则不插入，否则插入数据
        if existing_data is None:
            mycol.insert_one(data)
            print("数据插入成功！")
        else:
            print("数据已存在，不需要插入。")
        return 200
    except:
        return 500