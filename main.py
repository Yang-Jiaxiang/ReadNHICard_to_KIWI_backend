import tkinter as tk
from datetime import datetime
import pprint
import script.cardReader
from PIL import Image
from pystray import MenuItem as item
import pystray
import icon,os,base64
from icon import img
import requests
from dotenv import load_dotenv
import json
from tkinter import messagebox
import pickle

load_dotenv()
BACK_END_URL=os.getenv("BACK_END_URL")

api_token=""
isLoging = False

class LoginWindow:

    def __init__(self, parent):

        self.parent = parent
        self.login_window = tk.Toplevel(parent)  # 創建登錄視窗
        self.login_window.title("登錄")  # 設置登錄視窗的標題
        self.login_window.geometry("200x80")
        self.login_window.resizable(0, 0)

        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.login_window.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

        # 創建用戶名和密碼標籤和輸入框
        self.username_label = tk.Label(self.login_window, text="用戶名:")
        self.username_entry = tk.Entry(self.login_window)

        self.password_label = tk.Label(self.login_window, text="密碼:")
        self.password_entry = tk.Entry(self.login_window, show="*")

        # 創建登錄按鈕
        self.login_button = tk.Button(self.login_window, text="登錄", command=self.login)

        # 使用網格布局排列控件
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        self.login_button.grid(row=2, column=1, columnspan=2)
        self.session = requests.Session()


    def login(self):
        global api_token
        global isLoging
        # 在這裡添加您的登錄邏輯，例如驗證用戶名和密碼是否正確
        # 如果登錄成功，則關閉登錄窗口並顯示主窗口
        userName = self.username_entry.get()
        passWork = self.password_entry.get()
        url = BACK_END_URL + "/auth/login"
        myobj = {'username': userName, "password": passWork}
        x = requests.post(url, json=myobj)
        if (x.status_code == 200):
            isLoging=True
            api_token = json.loads(x.text)['token']
            self.login_window.destroy()
            self.parent.deiconify()
        else:
            messagebox.showerror('登入錯誤', json.loads(x.text)['message'])

class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x400')
        self.root.resizable(False, False)
        self.root.title("奇異鳥健保卡讀卡元件")
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        global isLoging

        # 創建一個登錄視窗實例，但是不顯示它
        self.login = LoginWindow(self.root)

        def add_Log_Message(message):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            logValue.insert(tk.INSERT, dt_string + ":" + "\n" + message + "\n=============================\n")

        def readCard_button_event():
            if(isLoging==False):
                self.login = LoginWindow(self.root)
            else:
                cardContent = script.cardReader.readCard()
                carCode = str(cardContent)[9:12]
                if carCode == "500":
                    add_Log_Message("尚未讀取到卡片")
                if carCode == "200":
                    add_Log_Message("讀取卡片成功")
                    pretty_print_json = pprint.pformat(cardContent).replace("'", '"')
                    url = BACK_END_URL+"/api/patient"
                    cookies = {'accessToken': api_token}
                    x = requests.post(url, cookies=cookies, json=cardContent)
                    if(x.status_code==200):
                        add_Log_Message("新增資料庫成功")
                    else:
                        if("E11000" in json.loads(x.text)["message"]):
                             add_Log_Message("已存在資料庫")
                        else:
                            add_Log_Message("其他錯誤，請重啟讀卡程式")

        # 讀取卡片
        cardReadbutton = tk.Button(self.root,
                                    text='讀取卡片/加入病患',
                                    font=('Arial',18,'bold'),
                                    padx=10,
                                    pady=10,
                                    activeforeground='#f00',
                                    command=readCard_button_event)
        cardReadbutton.pack()

        # 下方log message
        logValue = tk.Text(self.root)
        logValue.pack(fill='x')

        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()