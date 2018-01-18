from WindPy import w
from WTrader.DataHandler import datahandler as dh
import pandas as pd
import datetime


class Handler(object):
    # def UpdateEco(self):
    #     Ticker=self.GetTicker('ECO')
    #     Start=self.GetLastUpdateTime('ECO')
    #     End=datetime.datetime.today()
    #     ECO=LoadEco(Ticker,Start,End)
    #     if isinstance(ECO,pd.DataFrame):
    #         self.UpdateDatabase(ECO,'ECO')
    #     else:
    #         print(ECO)
    #         return

    def Updatess(self,Ticker,start):
        SS=LoadSS(Ticker,start)
        if isinstance(SS,pd.DataFrame):
            self.UpdateDatabase(SS,'Securities')
        else:
            print(SS)
            return

    def UpdateTS(self,End):
        Type=self.GetTicker('STOCK')
        Ticker = dh.load_obj('Securities')['wind_code'].tolist()
        Timetable=dh.load_obj('TimeTable')
        for item in Type:
            if item in Timetable.keys():
                Start=Timetable[item]
            else:
                Timetable[item]='2010-01-01'
                Start=Timetable[item]
            if End>Start:
                TS = LoadTimeSeries(Ticker,item, Start,End)
                if isinstance(TS, pd.DataFrame):
                    self.UpdateDatabase(TS, item)
                    Timetable[item]=End
                else:
                    print(TS)
                    return
        dh.save_obj(Timetable,'TimeTable')

    def DisplayData(self,title):
        data=dh.load_obj(title)
        print(data)

    def UpdateDatabase(self,data,title):
        if dh.obj_exist(title):
            Historicaldata=dh.load_obj(title)
            result = pd.concat([Historicaldata, data])
            result=result.drop_duplicates()
        else:
            result = data
        dh.save_obj(result,title)

    def CreateTicker(self,Title, List):
        dh.save_obj(List, Title + 'TickerList')

    def GetTicker(self,Title):
        Ticker = dh.load_obj(Title + 'TickerList')
        return Ticker

    # def GetLastUpdateTime(self,Type):
    #     if dh.obj_exist('TimeTalbe'):
    #         TimeTable = dh.load_obj('TimeTable')
    #     else:
    #         TimeTable=self.CreateTimeTable()
    #     if Type in TimeTable.keys():
    #         return TimeTable[Type]
    #     else:
    #         TimeTable[Type]='2010-01-01'
    #         return TimeTable[Type]

    def CreateTimeTable(self):
        TimeTable={}
        TimeTable['ECO']='2010-01-01'
        TimeTable['Price']='2010-01-01'
        TimeTable['Fundamental']='2010-01-01'
        TimeTable['SecuritySet']='2010-01-01'
        dh.save_obj(TimeTable,'TimeTable')

# Transfrom Wind data to pandas
def WindtoPandas(data):
    if len(data.Times)>1:
        if len(data.Codes)>1:
            fm = pd.DataFrame(data.Data, index=data.Codes, columns=data.Times)
        else:
            fm = pd.DataFrame(data.Data, index=data.Fields, columns=data.Times)
    else:
        fm=pd.DataFrame(data.Data,index=data.Fields,columns=data.Codes)
    return fm.T

def LoadEco(Ticker,start,end):
    if w.isconnected() == False:
        w.start()
    data=w.edb(Ticker, start, end)
    if data.ErrorCode==0:
        pd=WindtoPandas(data)
    else:
        pd=data.ErrorCode
    return pd

def LoadSS(Ticker,start):
    if w.isconnected() == False:
        w.start()
    code='date='+start+';sectorid='+Ticker
    data=w.wset('sectorconstituent',code)
    if data.ErrorCode==0:
        pd=WindtoPandas(data)
    else:
        pd=data.ErrorCode
    return pd

def LoadTimeSeries(Ticker,Type,Start,End):
    if w.isconnected() == False:
        w.start()
    data=w.wsd(Ticker, Type, Start,End, "Period=W;PriceAdj=F")
    if data.ErrorCode==0:
        pd=WindtoPandas(data)
    else:
        pd=data.ErrorCode
    return pd

