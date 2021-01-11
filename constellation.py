import requests
import xml.etree.cElementTree as et
from bs4 import BeautifulSoup

#region 參考資料
#https://ithelp.ithome.com.tw/articles/10246383
#endregion
class Constellation():
    def __init__(self):

        # 星座轉換字典
        self.__zodiacDict = {
            '牡羊座': 'Aries',
            '金牛座': 'Taurus',
            '雙子座': 'Gemini',
            '巨蟹座': 'Cancer',
            '獅子座': 'Leo',
            '處女座': 'Virgo',
            '天秤座': 'Libra',
            '天蠍座': 'Scorpio',
            '射手座': 'Sagittarius',
            '摩羯座': 'Capricorn',
            '水瓶座': 'Aquarius',
            '雙魚座': 'Pisces'
        }

    def getToday(self, name):
        outputText = "無此星座"
        url = "https://www.daily-zodiac.com/mobile/zodiac/%s" % (
            self.__zodiacDict[name])
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            sp = BeautifulSoup(response.text, 'html.parser')
            zodiacSigns_name = sp.select(".middle .name .name")[0].text  # 星座名稱
            zodiacSigns_date = sp.select(".middle .name .date")[0].text  # 星座日期
            today_date = sp.select(".today li")[1].text  # 今日日期
            today_horoscope_weather = sp.select(
                ".today .weather")[0].text  # 今日心情

            # 移除字串開頭的空格 str.lstrip()
            # 移除字串末尾的空格 str.rstrip()
            today_horoscope = sp.select("section article")[0].text.lstrip()

            # 印出結果
            outputText = '[%s %s 今日運勢]\n' % (
                zodiacSigns_name, zodiacSigns_date)
            outputText += '今日日期:%s\n' % (today_date)
            outputText += '今日心情:%s\n' % (today_horoscope_weather)
            outputText += '今日評語:\n%s' % (today_horoscope)

        return outputText
