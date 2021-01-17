from buffet_code import sample

# CSV へ保存
# ticker_code = input() #7974,9983,1547
ticker = '7974'
df_q, df_d, df_c = sample.make_df(ticker)
df_q.to_csv(f"csv/df_q/{ticker}.csv")
df_d.to_csv(f"csv/df_d/{ticker}.csv")
df_d.to_csv(f"csv/df_c/{ticker}.csv")