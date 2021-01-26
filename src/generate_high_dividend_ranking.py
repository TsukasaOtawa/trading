from yahoo import ylib
from pathlib import Path
from datetime import date
import pandas as pd

# generate high_diviends html from yahoo
# 8 : high_diviends
kd_idx = 8
kd_name = "high_diviends"

day = date.today().strftime("%Y%m%d")
out_dir = Path(f"html/{kd_name}/{day}/")
out_dir.mkdir(exist_ok=True)

# get high_diviends page from yahoo
get_ranking_html(kd_idx, out_dir)
df_stock = pd.DataFrame()

# find stock date from html ranking
df_concat = pd.DataFrame()
for page in list(range(ylib.PAGE_START, ylib.PAGE_END)):
    df_stock   = ylib.get_stocks(out_dir, 1)
    df_stock   = pd.DataFrame(df_stock, columns=ylib.COLUMNS)
    df_stock   = df_stock.drop(["掲示板", "date_time"], axis=1)
    df_stock["date"] = day
    df_concat = pd.concat([df_concat,df_stock], ignore_index=True)

# store into DynamoDB
ylib.store_stocks(df_concat)