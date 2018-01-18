import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import math
from datetime import datetime

def PlotMacro(data,title,start,end,line=[],bar=[]):
    data['month']=data['month'].astype(str)
    data['month']=data['month'].str.replace('.','-')
    data['month']=pd.to_datetime(data['month'])
    data=data[(data['month'] >= start) & (data['month'] <= end)]
    Trace=[]
    if len(line)>0:
        for item in line:
            Trace.append(go.Scatter(
                x=data['month'],
                y=data[item],
                name=item,
            ))
    if len(bar)>0:
        for item in bar:
            Trace.append(go.Bar(
                x=data['month'],
                y=data[item],
                name=item,
                yaxis='y2',
            ))
        layout = go.Layout(
            showlegend=True,
            legend=dict(orientation="h"),
            title=title,
            margin=go.Margin(
                l=80,
                r=80,
                b=80,
                t=80,
                pad=4
            ),
            yaxis2=dict(
                titlefont=dict(
                    color='rgb(148, 103, 189)'
                ),
                tickfont=dict(
                    color='rgb(148, 103, 189)'
                ),
                overlaying='y',
                side='right'
            )
        )

    layout = go.Layout(
        showlegend=True,
        legend=dict(orientation="h"),
        title=title,
        margin=go.Margin(
            l=80,
            r=80,
            b=80,
            t=80,
            pad=4
        )
    )

    fig = go.Figure(data=Trace,layout=layout)
    py.image.save_as(fig, filename='Chart/'+title+'.png')


def PlotPrice(price,title):
    price['ma5']=price["close"].rolling(window = 5,min_periods=1).mean()
    price['ma10']=price["close"].rolling(window=10,min_periods=1).mean()
    price['ma20'] = price["close"].rolling(window=20,min_periods=1).mean()
    Bar = go.Candlestick(x=price.index,
                        open=price.open,
                        high=price.high,
                        low=price.low,
                        close=price.close,
                        name="Candle Chart",
                         )
    Ma5=go.Scatter(x=price.index,y=price.ma5,name="Ma_5")
    Ma10=go.Scatter(x=price.index,y=price.ma10,name="Ma_10")
    Ma20=go.Scatter(x=price.index,y=price.ma20,name="Ma_20")
    Volume=go.Bar(x=price.index,y=price.volume,name="Volume",yaxis='y2')
    layout=go.Layout(
        title=title+' Price Chart',
        showlegend=False,
        margin=go.Margin(
            l=80,
            r=80,
            b=80,
            t=80,
            pad=4
        ),
        yaxis=dict(
            title='Price'
        ),
        yaxis2=dict(
            scaleanchor="y",
            scaleratio=0.1,
            title='Volume',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            showgrid=False,
            overlaying='y',
            side='right'
        )
    )
    data = [Bar,Ma5,Ma10,Ma20,Volume]
    fig = go.Figure(data=data,layout=layout)
    py.image.save_as(fig, filename='Chart/'+title+'_Price_Chart.png')

def PlotTick(price,title):
    price=price.round({'price':0})
    buy=price.loc[price['type']=='买盘']
    sell=price.loc[price['type']=='卖盘']
    neutral=price.loc[price['type']=='中性盘']
    buy=buy.groupby(by=['price'],as_index=False)['volume'].sum()
    sell=sell.groupby(by=['price'],as_index=False)['volume'].sum()
    neutral=neutral.groupby(by=['price'],as_index=False)['volume'].sum()
    sell['volume']=sell['volume']*-1
    aggregate=buy.copy()
    aggregate['volume']=aggregate['volume']+sell['volume']
    Buytickets = go.Bar(
        x=buy['price'],
        y=buy['volume'],
        name='Buy Ticks'
    )
    Selltickets = go.Bar(
        x=sell['price'],
        y=sell['volume'],
        name='Sell Ticks'
    )
    Aggregate=go.Scatter(
        x=aggregate['price'],
        y=aggregate['volume'],
        name='Aggregate'
    )

    Neutral = go.Scatter(
        x=neutral['price'],
        y=neutral['volume'],
        name='Neutral'
    )

    data = [Buytickets, Selltickets,Aggregate,Neutral]
    layout = go.Layout(
        title=title + ' Volume Chart',
        barmode='relative',
    )
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename= 'Chart/'+title+'Today_Volume_Chart.png')

def PlotSingleFundamental(data,fundamental='pe',area=None,industry=None):
    if area!=None:
        data=data.loc[data['area']==area]
    else:
        area='全地区'

    if industry!=None:
         data=data.loc[data['industry']==industry]
         data=data.sort_values(fundamental)
         Fundamental = go.Bar(
            x=data['name'],
            y=np.log(data[fundamental].abs()+1)*np.sign(data[fundamental]),
            name=fundamental,
            text = data[fundamental],
            textposition = 'auto',
            opacity=0.6
        )
    else:
        data=data.groupby(by=['industry'],as_index=False)[fundamental].mean()
        data=data.sort_values(fundamental)
        Fundamental=go.Bar(
            x=data['industry'],
            y=np.log(data[fundamental].abs()+1)*np.sign(data[fundamental]),
            name=fundamental,
            text=data[fundamental],
            textposition='auto',
            opacity=0.6
        )
        industry='分行业'
    chartdata = [Fundamental]

    num = len(data.index)
    if num > 15:
        w = 1600
        h = 1024
    else:
        w = 800
        h = 600

    RANGE=list(range(int(math.floor(np.log(abs(data[fundamental].min())+1))*np.sign(data[fundamental].min())),int(math.ceil(np.log(abs(data[fundamental].max()+1))*np.sign(data[fundamental].max())))))
    VAL=np.round((np.exp(np.abs(RANGE))-1)*np.sign(RANGE)).tolist()

    layout = go.Layout(
        title=area+industry+fundamental + '比较',
        yaxis=go.YAxis(
            title=fundamental,
            tickvals=RANGE,
            ticktext=VAL,
        )
    )
    fig = go.Figure(data=chartdata, layout=layout)
    py.image.save_as(fig, filename='Chart/'+area+industry+fundamental+ '比较.png')


def PlotMultiFundamental(data,f1='pe',f2='gpr',f3='totalAssets',f4='profit',area=None,industry=None):
    if area != None:
        data = data.loc[data['area'] == area]
    else:
        area='全地区'

    if industry != None:
        data = data.loc[data['industry'] == industry]

        RANGE4 = list(range(int(math.floor(np.log(abs(data[f4].min()) + 1)) * np.sign(data[f4].min())),
                           int(math.ceil(np.log(abs(data[f4].max() + 1)) * np.sign(data[f4].max())))))
        VAL4 = np.round((np.exp(np.abs(RANGE4)) - 1) * np.sign(RANGE4)).tolist()

        Fundamental = go.Scatter(
            x=np.log(data[f1].abs()+1)*np.sign(data[f1]),
            y=np.log(data[f2].abs()+1)*np.sign(data[f2]),
            text=data['name'],
            textposition='bottom',
            marker=dict(
                size=np.log(data[f3]+1)/np.log(data[f3].max()+1)*20,
                color=np.log(data[f4].abs()+1)*np.sign(data[f4]),
                colorscale='Jet',
                colorbar=go.ColorBar(
                    title=f4,
                    tickmode = 'array',
                    tickvals = RANGE4,
                    ticktext = VAL4,
                    ticks = 'outside'
                ),
                showscale=True,
                opacity=0.6
            ),
            name='Fundamental Comparison',
            mode='markers+text'
        )
    else:
        data=data.groupby(by=['industry'],as_index=False).mean()
        RANGE4 = list(range(int(math.floor(np.log(abs(data[f4].min()) + 1)) * np.sign(data[f4].min())),
                            int(math.ceil(np.log(abs(data[f4].max() + 1)) * np.sign(data[f4].max())))))
        VAL4 = np.round((np.exp(np.abs(RANGE4)) - 1) * np.sign(RANGE4)).tolist()
        Fundamental = go.Scatter(
            x=np.log(data[f1].abs() + 1) * np.sign(data[f1]),
            y=np.log(data[f2].abs() + 1) * np.sign(data[f2]),
            text=data['industry'],
            textposition='bottom',
            marker=dict(
                size=np.log(data[f3])/np.log(data[f3].max())*20,
                color=np.log(data[f4].abs()+1)*np.sign(data[f4]),
                colorscale='Jet',
                colorbar=go.ColorBar(
                    title=f4,
                    tickmode='array',
                    tickvals=RANGE4,
                    ticktext=VAL4,
                    ticks='outside'
                ),
                showscale=True,
                opacity=0.6
            ),
            name='Fundamental Comparison',
            mode='markers+text'
        )
        industry = '全行业'

    chartdata = [Fundamental]
    num=len(data.index)
    if num>15:
        w=1600
        h=1024
    else:
        w=800
        h=600
    RANGE2 = list(range(int(math.floor(np.log(abs(data[f2].min()) + 1)) * np.sign(data[f2].min())),
                        int(math.ceil(np.log(abs(data[f2].max() + 1)) * np.sign(data[f2].max())))))
    VAL2 = np.round((np.exp(np.abs(RANGE2)) - 1) * np.sign(RANGE2)).tolist()

    RANGE1 = list(range(int(math.floor(np.log(abs(data[f1].min()) + 1)) * np.sign(data[f1].min())),
                        int(math.ceil(np.log(abs(data[f1].max() + 1)) * np.sign(data[f1].max())))))
    VAL1 = np.round((np.exp(np.abs(RANGE1)) - 1) * np.sign(RANGE1)).tolist()

    layout = go.Layout(
        title=area+industry+'基本面比较',
        xaxis=go.XAxis(
            title=f1,
            tickvals=RANGE1,
            ticktext=VAL1,

        ),
        yaxis=dict(
            title=f2,
            tickvals = RANGE2,
            ticktext = VAL2,
        ),
        width=w,
        height=h,
    )
    fig = go.Figure(data=chartdata, layout=layout)
    py.image.save_as(fig, filename='Chart/'+area+industry+'基本面比较.png')
