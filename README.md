# ReadNHICard2MongoDB_python

## 說明
使用python透過晶片讀卡機讀取健保卡卡面資料，登入使用kiwi系統backend auth api完成。將病患基本資料使用kiwi系統backend api 
 
## Build
``` pyinstaller -F -i logo.ico --add-data ".env;." --noconsole  main.py ```

## Deployment
create ".env" file in folder   
```BACK_END_URL=http://tws-kiwi-cloud-api.luckypig.net/nec```


![未命名绘图 drawio](https://user-images.githubusercontent.com/81738019/227122180-19b3325a-88af-4858-9ed7-763deb797961.png)
