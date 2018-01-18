import pandas as df
import numpy as np
from WTrader.DataHandler import datahandler as dh
from datetime import datetime
class Evaluation(object):
    def __init__(self,strats):
        self.Data=dict()
        self.Ticker=list()
        self.strats=strats
        self.Time=list()

    def UpdateTicker(self,name):
        self.Ticker=dh.load_obj(name)['wind_code'].tolist()
        self.strats.UpdateTicker(self.Ticker)

    def UpdateData(self,type):
        self.Data[type]=dh.load_obj(type)
        self.strats.UpdateData(self.Data)

    def GeneratePosition(self,date):
        self.strats.UpdateDate(date)
        Position =self.strats.run()
        return Position

    def Evaluate(self,start,end):
        close=self.Data['close']
        Time=df.to_datetime(close.index)
        Time= Time[(Time> start) & (Time <= end)]
        Position=df.DataFrame(data=None,index=Time,columns=self.Ticker)
        for date in Position.index:
            pos=self.GeneratePosition(date)
            Position.loc[date] = pos.loc[date]
        return Position
        # UpdatePerformance
        # UpdateRiskManager


class Strategy(object):
    def __init__(self):
        self.Data=dict()
        self.Ticker=list()
    def UpdateTicker(self,Ticks):
        self.Ticker=Ticks
    def UpdateDate(self,date):
        self.Date=date
    def UpdateData(self,data):
        self.Date=data
    def run(self):
        NumberofStock=len(self.Ticker)
        data=np.ones(NumberofStock)/NumberofStock
        Position=df.DataFrame(data=data,columns=[self.Date],index=self.Ticker)
        return Position.T
