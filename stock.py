import twstock
from twstock import Stock
from twstock import BestFourPoint
#https://github.com/mlouielu/twstock
class TWStock():
    def __init__(self,code):
        self.__code=code
        return


    def getCompanyName(self):
        stock = Stock(self.__code)
        name = twstock.codes[self.__code].name
        return name

    def getPrice(self):
        stock = Stock(self.__code)
        price = stock.price[30]
        return price
