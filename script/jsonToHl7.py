import requests
from hl7apy.core import Message, Segment, Field
from datetime import datetime
now = datetime.now()

def jsonToHl7(json_data):

    # 創建HL7消息 v2.3.1
    hl7_message = Message("ADT_A01",version="2.3.1")
    data = json_data

    # 參考欄位https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/PID
    # 創建PID段
    pid = hl7_message.add_segment("PID")
    # pid.pid_1 = "1"
    # pid.pid_2 = data['id']
    pid.pid_3.cx_1 = data['id']
    pid.pid_3.cx_5 = 'TW'
    pid.pid_5.xpn_1 = data['name']
    pid.pid_7.ts_1=str(int(data['birthday'][0:2])+1911)+str(data['birthday'][2:6])
    pid.pid_8 = data["sex"]
    # pid.pid_18 = data['id']+now.strftime("%Y%m%d")
    # pid.pid_19 = data['id']+now.strftime("%Y%m%d")

    # 參考欄位https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/MSH
    # 建立 MSH 段
    msh = hl7_message.add_segment("MSH")
    msh.msh_1 = "|"
    msh.msh_2 = "^~\&"
    msh.msh_3 = "HMIS"
    msh.msh_4 = "DUHS"
    msh.msh_5 = "PACS"
    msh.msh_6 = "KIWITEAM"
    msh.msh_7 = now.strftime("%Y%m%d%H%M%S")
    msh.msh_9 = "OMI^O23^OMI_O23"
    msh.msh_10 = now.strftime("%Y%m%d%H%M%S")
    msh.msh_11 = "P"
    msh.msh_12 = "2.3.1"
    msh.msh_18 = "UNICODE UTF-8"

    # 參考欄位https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/ORC
    # 建立 ORC 段
    orc = hl7_message.add_segment("ORC")
    orc.orc_1 = "NW"
    orc.orc_2.ei_1 = data['id']
    orc.orc_2.ei_4 = "TW"
    orc.orc_5 = "SC"
    orc.orc_9 = now.strftime("%Y%m%d%H%M%S")
    orc.orc_12.xcn_1 = data['id']
    orc.orc_12.xcn_2 = data['name'][0:1]
    orc.orc_12.xcn_3 = data['name'][1:3]

    #參考欄位https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/OBR
    #建立 OBR 段
    obr = hl7_message.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_24 = "US"
    hl7 = msh.to_er7()+"\n"+pid.to_er7()+"\n"+orc.to_er7()+"\n"+obr.to_er7()
    return hl7
