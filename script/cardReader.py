from smartcard.System import readers
import json
import datetime

def readCard():
    try:
        # define the APDUs used in this script
        SelectAPDU = [ 0x00, 0xA4, 0x04, 0x00, 0x10, 0xD1, 0x58, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00 ]

        ReadProfileAPDU = [ 0x00, 0xca, 0x11, 0x00, 0x02, 0x00, 0x00 ]

        # get all the available readers
        r = readers()

        reader = r[0]

        connection = reader.createConnection()
        connection.connect()

        data, sw1, sw2 = connection.transmit(SelectAPDU)

        data, sw1, sw2 = connection.transmit(ReadProfileAPDU)

        name = str.strip(bytes(data[12:18]).decode("big5").rstrip('\x00'))

        Year = ("".join(chr(i) for i in data[42:45])).encode("utf-8").decode("utf-8")
        Month = ("".join(chr(i) for i in data[45:47])).encode("utf-8").decode("utf-8")
        Day = ("".join(chr(i) for i in data[47:49])).encode("utf-8").decode("utf-8")
        date_str = str(int(Year)+1911) + "-" + Month + "-" + Day
        return {
            "code":200,
            "id": ("".join(chr(i) for i in data[32:42])).encode("utf-8").decode("utf-8"),
            "name":name,
            "birth": date_str,
            "gender": ("".join(chr(i) for i in data[49:50])).encode("utf-8").decode("utf-8").lower(),
            "cardDate": ("".join(chr(i) for i in data[51:57])).encode("utf-8").decode("utf-8"),
            "phone":"0912345678",
            "department":"cyLab"
        }
    except:
        return {
            "code":500,
            "error":"card reader is not working"
        }