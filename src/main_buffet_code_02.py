from buffet_code import sample2
import pandas as pd
from numpy import nan

processed_df = []
# ticker_data = input() #7974,9983,1547
ticker_data = ["7974"]

for i in range(len(ticker_data)):
    ticker = ticker_data[i]
    if not ticker.isdecimal():
        break
    df_q = pd.read_csv(f"csv/df_q/{ticker_data[i]}.csv")
    df_day = pd.read_csv(f"csv/df_d/{ticker_data[i]}.csv")
    df_c = pd.read_csv(f"csv/df_c/{ticker_data[i]}.csv")

    
    gp1_nsgr, gp2_oigr = sample2.growth_potential(df_q)
    pr1_roe, pr2_om = sample2.profitability(df_q)
    lp1_nspe, lp2_oipe= sample2.labor_productivity(df_q)
    e1_tat,e2_ccc = sample2.efficiency(df_q)
    s1_er, s2_nder = sample2.safety(df_q)
    sr1_dpr,sr2_doe = sample2.shareholder_returnability(df_q)
    #cg = sample2.capital_gain(df_day,df_c)
    

    company = df_q.loc[ :,"company_name"]
    df_q.index.name = company[0]
    df_list =pd.DataFrame({
        "company":[df_q.index.name],
        "code":[ticker],
        "sales_growth_rate":[gp1_nsgr],
        "operating_income_growth_rate":[gp2_oigr],
        "roe":[pr1_roe],
        "operating_margin":[pr2_om],
        "net_sales_per_employee":[lp1_nspe],
        "operating_income_per_employee":[lp2_oipe],
            "total_assets_turnover":[e1_tat],
        "ccc":[e2_ccc],
        "equity_ratio":[s1_er],
        "net_d/e_ratio":[s2_nder],
        "dividend_payout_ratio":[sr1_dpr],
            "doe":[sr2_doe],
        #"capital_gain":[cg]
    })
    processed_df.append(df_list)
    break

processed_data =  pd.concat([processed_df[0]])
processed_data.to_csv(f"./csv/{ticker_data[0]}_processedData.csv",index = False,encoding = "utf_8_sig")