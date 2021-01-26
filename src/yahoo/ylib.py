import requests
from bs4 import BeautifulSoup
import urllib
import time
import pandas as pd

import boto3
from boto3.dynamodb.conditions import Key # Boto 3 SDK によって Attr が自動的に作成される

# P1 - P6(300社分) HTML取得
PAGE_START = 1
PAGE_END = 6
COLUMNS = ['rank','ticker','market','name','date_time','stock_price','fiscal_month','DPS','dividend','掲示板']

def get_ranking_html(kd:int, out_dir:str):
    for page in list(range(PAGE_START,PAGE_END)):
        load_url = f"https://info.finance.yahoo.co.jp/ranking/?kd={kd}&tm=d&vl=a&mk=1&p={page}"
        html = requests.get(load_url)
        filename = f"{page}.html"
        out_path = out_dir.joinpath(filename)
        with open(out_path, mode="wb") as f:
            f.write(html.content)
        time.sleep

def get_stocks(out_dir:str, page):
    filename = f"{page}.html"
    file_path = out_dir.joinpath(filename)
    with open(file_path, mode="r") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        rankingTable = soup.find(class_="rankingTable")
        stocks = []
        for tr in rankingTable.find_all("tr", class_="rankingTabledata"):
            stock = []
            for data in tr.find_all("td"):
                stock.append(data.text)
            stocks.append(stock)
    return stocks

def store_stocks(stocks:pd.DataFrame, dynamodb=None):
    # Key フォーマットの調整
    stocks["rank"] = stocks["rank"].astype(int)
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('HighDividends')
    for index, row in stocks.iterrows():
        table.put_item(Item=row.to_dict())