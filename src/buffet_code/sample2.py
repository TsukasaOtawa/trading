import pandas as pd
from numpy import nan

def slide(present):
    past = present.shift(-1)
    growth_rate  = (present - past)/past *100
    return growth_rate.dropna()

#第2章のデータのクレンジングで使用
def w_ave(x):
    sum_wa = 0
    count=0
    
    #欠損値を削除
    x_dropna = x.dropna()
    
    #シリーズ型のためvalueのみ取り出している
    for quarter in x_dropna.values:
        count += 1
        weight = quarter * count
        sum_wa += weight 
        
    if sum_wa == 0 :
        return nan
    else:
        result = sum_wa / ((1/2)*count*(count+1))
        if result == float('inf') :
            return nan
        else :
            return result

def growth_potential(df_q):
    #売上成長
    gp1_slide = slide(df_q["net_sales"])
    gp1_nsgr =w_ave(gp1_slide)
    #営業利益成長率
    gp2_slide = slide(df_q["operating_income"])
    gp2_oigr =w_ave(gp2_slide)
    return  gp1_nsgr, gp2_oigr

def profitability(df_q):
    #ROE
    pr1_roe = w_ave(df_q["roe"])  
    #営業利益率
    pr2_om = w_ave(df_q["operating_margin"]) 
    return pr1_roe, pr2_om

def labor_productivity(df_q):
    #1人当たり売上高
    lp1_nspe = w_ave(df_q["net_sales_per_employee"])
    #1人当たり営業CF
    lp2_oipe = w_ave(df_q["operating_income_per_employee"])
    return lp1_nspe, lp2_oipe

def efficiency(df_q):
    #総資産回転率
    e1_tat = w_ave(df_q["total_asset_turnover"])
    #<2:CCC(キャッシュコンバージョンサイクル) = 売上債権回転期間 + 棚卸資産回転期間 – 支払債務回転期間)>
    e2_df = df_q[["accounts_receivable_turnover","inventory_turnover","trade_payable_turnover"]]
    e2_ccc = w_ave(e2_df["trade_payable_turnover"])+w_ave(e2_df["inventory_turnover"])-w_ave(e2_df["accounts_receivable_turnover"])
    return e1_tat,e2_ccc

def safety(df_q):
    #自己資本比率 equity_ratio
    s1_er = w_ave(df_q["equity_ratio"])
    #ネットD/Eレシオ = 純有利子負債 net_debt/ 自己資本 equity
    s2_df = df_q[["net_debt","equity"]]
    s2_nder = w_ave(s2_df["net_debt"]/s2_df["equity"])
    return  s1_er, s2_nder

def shareholder_returnability(df_q):
    #<1:配当性向 Dividend payout ratio (%）＝ 1株あたり配当金 Dividends per share ÷1株あたり純利益（EPS）×100>
    sr1_df = df_q[["dividend","eps_actual"]]
    sr1_dpr = w_ave(sr1_df["dividend"] /sr1_df["eps_actual"] * 100)
    #<2:株主資本配当率 DOE(株主資本配当率）＝ 年間総配当額 ÷ 自己資本>
    sr2_doe = w_ave(df_q["doe"])
    return sr1_dpr,sr2_doe

def dc_merge(daily,current):
    if current[0] is None:
        return daily
    else : 
        dcm = pd.concat([daily,current],axis = 0)
        return dcm

def capital_gain(df_day,df_c):
    df_cg = df_day[["market_capital","num_of_shares"]]
    cg_d = df_cg["market_capital"]/df_cg["num_of_shares"]
    cg_c = df_c["stockprice"]
    cg_merge = dc_merge(cg_d,cg_c)
    cg_before = cg_merge
    cg_after = cg_merge.shift(-1)
    #slide関数では100倍するため注意
    cg_ab = (cg_after - cg_before)/cg_before
    cg = w_ave(cg_ab)
    return cg