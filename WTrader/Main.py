import datetime
import GetData as gd
import PlotData as pd
import SaveData as sd

class Trader(object):
    def UpdateMacro(self):
        Macro = gd.get_macro()
        sd.save_obj(Macro, 'Macro')

    def UpdateFundamental(self,year,quarter):
        Fundamental=gd.get_fundamental_data(year,quarter)
        sd.save_obj(Fundamental, str(year)+str(quarter)+ 'fundamental')

    def UpdateStock(self,ticker,start,end):
        Price=gd.get_trading_data(ticker, start, end)
        sd.save_obj(Price, ticker+'price')

    def UpdateNews(self,ticker):
        News=gd.get_news(ticker)
        sd.save_obj(News,ticker+'news')

    def ShowFundamental(self,year,quarter,area=None,industry=None):
        data=sd.load_obj(str(year)+str(quarter)+'Qfundamental')
        pd.PlotSingleFundamental(data['basic'],'profit',area,industry)
        pd.PlotMultiFundamental(data['basic'],'pe','rev','totals','profit',area,industry)

    def ShowPrice(self,ticker):
        data=sd.load_obj(ticker+'price')
        pd.PlotPrice(data['price'],ticker)
        pd.PlotTick(data['tick'],ticker)

    def ShowMacro(self):
        data=sd.load_obj('Macro')
        pd.PlotMacro(data['MoneySupply'],'M2', '2016-1-1','2017-11-1', ['m2'])

trader=Trader()
# trader.UpdateStock('600519','2017-01-01','2018-01-15')
# trader.UpdateNews('600519')
# trader.UpdateMacro()
# trader.UpdateFundamental(2017,2)
# trader.ShowFundamental(2017,3,industry='软饮料')
# trader.ShowPrice('600519')
data=sd.load_obj('price')
print(data)