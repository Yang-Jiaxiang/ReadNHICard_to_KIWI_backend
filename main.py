from tkinter import *
from datetime import datetime
import DBControl
import script.cardReader
import script.jsonToHl7

window = Tk()
window.title('GUI')
window.geometry('300x400')
window.resizable(False, False)

def add_Log_Message(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    logValue.insert(INSERT, dt_string + ":"+message+"\n")

def Check_DB_Button():
    if DBControl.Check_DB_Onnection() == 200 :
        add_Log_Message("資料庫連線成功")
    else:
        add_Log_Message("資料庫連線失敗！！！")

def readCard_button_event() :
    cardContent = script.cardReader.readCard()
    carCode = str(cardContent)[9:12]
    if carCode == "500":
        add_Log_Message("尚未讀取到卡片")
    if carCode =="200":
        add_Log_Message("讀取卡片成功")
        add_Log_Message(str(cardContent))
        DB_insertState = DBControl.Insert_DB(cardContent)

        if  DB_insertState== 200 :
            add_Log_Message("新增資料庫成功")
        if  DB_insertState== 500 :
            add_Log_Message("新增資料庫失敗")

# 檢查資料庫連線
Check_DB_button = Button(window, text='檢查連線',command=Check_DB_Button)
Check_DB_button.pack()

#讀取卡片
cardReadbutton = Button(window, text='讀取卡片',command=readCard_button_event)
cardReadbutton.pack()


# 下方log message
logValue = Text(window)
logValue.pack(fill='x')

window.mainloop()