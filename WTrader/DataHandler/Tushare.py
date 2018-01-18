import tushare as ts

def get_trading_data(ticker,startdate,enddate):
    data={}
    price=ts.get_h_data(ticker,start=startdate,end=enddate)
    tick=ts.get_today_ticks(ticker)
    index=ts.get_index()
    data["price"]=price
    data["tick"]=tick
    data["index"]=index
    return data

def get_fundamental_data(year,quarter):
    fundamental = {}
    fundamental['basic'] =ts.get_stock_basics()
    fundamental['report']=ts.get_report_data(year, quarter)
    fundamental['profit']=ts.get_profit_data(year, quarter)
    fundamental['operation']=ts.get_operation_data(year, quarter)
    fundamental['cashflow']=ts.get_cashflow_data(year, quarter)
    fundamental['growth']=ts.get_growth_data(year, quarter)
    fundamental['debt']=ts.get_debtpaying_data(year, quarter)
    return fundamental

def get_news(ticker):
    return ts.get_notices(ticker)

def get_macro():
    Macro={}
    Macro['Depo']=ts.get_deposit_rate()
    Macro['Loan']=ts.get_loan_rate()
    Macro['RRR']=ts.get_rrr()
    Macro['MoneySupply']=ts.get_money_supply()
    Macro['MoneyBalance']=ts.get_money_supply_bal()
    Macro['GDPYOY']=ts.get_gdp_year()
    Macro['GDPQOQ']=ts.get_gdp_quarter()
    Macro['GDPFOR']=ts.get_gdp_for()
    Macro['GDPPULL']=ts.get_gdp_pull()
    Macro['GDPCON']=ts.get_gdp_contrib()
    Macro['CPI']=ts.get_cpi()
    Macro['PPI']=ts.get_ppi()
    Macro['SHIBO']=ts.shibor_data()
    return Macro