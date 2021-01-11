import requests
import xml.etree.cElementTree as et

class Weather():
    def __init__(self):
        self.__userKey = "CWB-57BD655A-326F-4AC9-BF6C-0D350A14A2B1"
        self.__docName = "F-C0032-001"

    def getTodayWeather(self):
        apiLink = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s" % (
            self.__docName, self.__userKey)
        report = requests.get(apiLink).text
        xmlNamespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
        root = et.fromstring(report)
        dataset = root.find(xmlNamespace+"dataset")
        locationsInfo = dataset.findall(xmlNamespace+"location")
        location = "臺中市"
        targetIdx = -1
        for idx, ele in enumerate(locationsInfo):
            locationName = ele[0].text
            if locationName == location:
                targetIdx = idx
                break

        if targetIdx != -1:
            outputText = location+"天氣狀況:\n"
            tlist = ["天氣狀況", "最高溫", "最低溫", "舒適度", "降雨機率"]
            for i in range(5):
                element = locationsInfo[targetIdx][i+1]
                timeblock = element[1]
                data = timeblock[2][0].text
                outputText = outputText+tlist[i]+":"+data+"\n"
        else:
            outputText = "無此縣市資料"

        return outputText


 
