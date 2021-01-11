import os
import sys
from flask import Flask, request, abort, jsonify
import requests
from flask_cors import CORS
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from weather import Weather
from stock import TWStock
from constellation import Constellation

# region 參考資料
# heroku web 額外設定 https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running
# https://www.learncodewithmike.com/2020/07/python-line-bot-deploy-to-heroku.html
# endregion

app = Flask(__name__)
CORS(app)

line_bot_api = LineBotApi(
    "8zO3/dR90NeH6XMN+tAwDCFx3iJyuSzJBzk5uZW9mOHV0639Lj716fzZ+0RWz5RrYk9c/ez5A4/sI7NdR2HjDOoW/+kFYof4m7+fCt6EyL4Xb0v53qnu3IWgn7Gftv0LQiMlWvoqxRQisrzTToh7OgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("238aefeb037616db8cbaf6aee72599a9")


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    inputText = event.message.text
    outputText = ""

    if inputText == '查詢匯率':
        resp = requests.get('https://tw.rter.info/capi.php')
        currency_data = resp.json()
        usd_to_twd = currency_data['USDTWD']['Exrate']
        outputText = f'美元 USD 對台幣 TWD：1:{usd_to_twd}'

    elif inputText == "今天天氣":
        weather = Weather()
        outputText = weather.getTodayWeather()

    elif inputText.find("誰最帥") != -1:
        outputText = "廖員外最帥!!"

    elif inputText.find("股價") != -1:
        code = inputText.split("股價")[0]
        stock = TWStock(code)
        name = stock.getCompanyName()
        price = stock.getPrice()
        outputText = name+" 股價為:"+str(price)

    elif inputText.find("運勢") != -1:
        zociac = Constellation()
        name = inputText.split("運勢")[0]
        outputText = zociac.getToday(name)

    else:
        outputText = ""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=outputText))


if __name__ == "__main__":
    app.run()
