# ReadNHICard2MongoDB_python

## Build
``` pyinstaller -F -i logo.ico --noconsole main.py```

## ENV
```
MONGODB_URL=mongodb://127.0.0.1
MONGODB_PORT=27017

AUTH_API=http://localhost:3080/nec/auth/login
AUTH_ADDPATIENTAPI=http://localhost:3080/nec/api/patient
```
