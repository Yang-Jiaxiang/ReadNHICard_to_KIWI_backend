from tkinter import *
from datetime import datetime
import pprint
import DBControl
import script.cardReader
from PIL import Image
from pystray import MenuItem as item
import pystray
import icon,os,base64
from icon import img

window = Tk()
window.geometry('300x400')
window.resizable(False, False)
window.title("奇異鳥健保卡讀卡元件")
tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
window.iconbitmap("tmp.ico")
os.remove("tmp.ico")

def quit_window(icon, item):
    icon.stop()
    window.destroy()
    window.quit()

def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)

def withdraw_window():
    window.withdraw()
    image = Image.open("logo.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()
#視窗關閉
window.protocol('WM_DELETE_WINDOW', withdraw_window)
def add_Log_Message(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    logValue.insert(INSERT, dt_string + ":"+"\n"+message+"\n=============================\n")

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
        pretty_print_json = pprint.pformat(cardContent).replace("'", '"')
        add_Log_Message(pretty_print_json)
        DB_insertState = DBControl.Insert_DB(cardContent)

        if  DB_insertState== 200 :
            add_Log_Message("新增資料庫成功")
        if  DB_insertState== 500 :
            add_Log_Message("新增資料庫失敗")

# 檢查資料庫連線
Check_DB_button = Button(window, text='檢查連線資料庫連線',command=Check_DB_Button)
Check_DB_button.pack()

#讀取卡片
cardReadbutton = Button(window, text='讀取卡片/手動加入病患',command=readCard_button_event)
cardReadbutton.pack()

# 下方log message
logValue = Text(window)
logValue.pack(fill='x')

window.mainloop()