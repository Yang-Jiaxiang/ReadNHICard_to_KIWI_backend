# ReadNHICard2MongoDB_python

## Build
``` pyinstaller -F -i logo.ico --noconsole main.py```

## .env
```
MONGODB_URL=mongodb://127.0.0.1
MONGODB_PORT=27017

AUTH_API=http://localhost:3080/nec/auth/login
AUTH_ADDPATIENTAPI=http://localhost:3080/nec/api/patient
```


![未命名绘图 drawio](https://user-images.githubusercontent.com/81738019/227122180-19b3325a-88af-4858-9ed7-763deb797961.png)
