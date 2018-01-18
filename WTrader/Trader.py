from WTrader.DataHandler import Wind
from WTrader.Strategy import Strategy
# DataHandler=Wind.Handler()
# DataHandler.CreateTicker('STOCK',"pre_close,open,high,low,close,volume,vwap,adjfactor,turn,free_turn,trade_status".split(','))
# DataHandler.UpdateEco()
# DataHandler.Updatess('a001010100000000','2018-01-17')
# DataHandler.CreateTimeTable()
# DataHandler.UpdateTS('2018-01-18')
# DataHandler.DisplayData('vwap')
# Wind.LoadEco('M5567876','2010-01-01','2017-01-01')

strats=Strategy.Strategy()
Eval=Strategy.Evaluation(strats)
Eval.UpdateTicker('Securities')
Eval.UpdateData('close')
pos=Eval.Evaluate('2017-01-01','2018-01-01')
print(pos)