import requests
import json
import pandas as pd
from datetime import *

BC_API_ENDPOINT_QUARTER = "https://api.buffett-code.com/api/v2/quarter"
BC_API_ENDPOINT_DAILY = "https://api.buffett-code.com/api/v2/daily"
BC_API_ENDPOINT_INDICATOR = "https://api.buffett-code.com/api/v2/indicator"

APIKEY = '{api_key}'

START_Q = '2020Q1'
END_Q = '2021Q4'

def fetch(bc_endpoint, ticker=None, from_q=None, to_q=None):
    if not ticker:
        print('tickerを設定する')
        return
    response = requests.get(
        url=bc_endpoint,
        params={
            'tickers': ticker,
            'from': from_q,
            'to': to_q,
        },
        headers={
            'x-api-key': APIKEY,
        },
    )
    return response

def make_df(ticker:str):
    res_q = fetch(BC_API_ENDPOINT_QUARTER, ticker, START_Q, END_Q)
    json_data_q = json.loads(res_q.text)
    df_q = pd.DataFrame.from_dict(json_data_q[ticker])
    # 日付データを datetime型に変換
    df_q['to_datetime'] = pd.to_datetime(df_q['edinet_updated_date'])
    df_sorted = sorted(df_q['to_datetime'] )
    df_concat = pd.DataFrame()
    for sort_num in range(len(df_sorted)):
        datetime_data = df_q[df_q['to_datetime'] == df_sorted[sort_num]]
        df_concat = pd.concat([df_concat, datetime_data], axis=0)

    year = 2020
    month = 1
    START_DAY = f"{year}-0{month}-01" #2019年度の第1四半期の時系列と合わせる
    END_DAY =  "2020-12-31" #2019年度の第4四半期の時系列と合わせる
    res_day = fetch(BC_API_ENDPOINT_DAILY, ticker, START_DAY, END_DAY)
    json_data_day = json.loads(res_day.text)
    df_d = pd.DataFrame.from_dict(json_data_day[ticker])
    
    # 4分割し平均化したデータをリスト化する
    df_day_list = []
    # 日付データを datetime型に変換
    df_d['to_datetime'] = pd.to_datetime(df_d['day'])
    df_merge = pd.DataFrame()
    # 最初の検索月
    sCondMonth = month - 1
    # +3 値更新月
    sCondMonthIncrement = 3
    sCondYear = year
    count = 0
    while True:
        count += 1
        #4回分割したら終了(1年分）
        if 4 + 1 <= count:
            break
        # 検索条件（From）～年～月１日より期間スタート
        sCondDatetimeFrom = datetime(sCondYear, sCondMonth + 1, 1, tzinfo=timezone.utc)

        # 検索期間の月と年を更新する
        sCondMonth = (sCondMonth + sCondMonthIncrement) % 12
        # 12で割ったあまりが1(13月 = 10月 + 3月)になった際、年を更新させる
        if sCondMonth < sCondMonthIncrement:
            sCondYear += 1
            # 検索条件（To）～年～(+3)月 で期間をストップ
        sCondDatetimeTo = datetime(sCondYear, sCondMonth + 1, 1, tzinfo=timezone.utc)   
        #検索期間内にあるデータを抽出
        df_dq = df_d[(sCondDatetimeFrom <= df_d['to_datetime']) & (df_d['to_datetime'] < sCondDatetimeTo)]
        #四半期ごとのデータを平均化しmergeさせる
        df_dq_mean = df_dq.mean(numeric_only=True)
        df_DQ = pd.DataFrame(df_dq_mean)
        df_merge = pd.concat([df_merge,df_DQ],axis = 1)
        #4分割し平均化したデータをリスト化する
        df_day_list.append(df_merge.T) #day

    #期間を指定せず、時点(直近営業日)を指定しいているため"None"を記入
    res_c = fetch(BC_API_ENDPOINT_INDICATOR, ticker, None, None)
    json_data_c = json.loads(res_c.text)
    #バフェットコードの仕様で一回当たり最大3社が取得可能な為対応
    df_c= pd.DataFrame.from_dict(json_data_c[ticker]) 
    return df_q, df_d, df_c