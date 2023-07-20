import calendar
import requests
import json
import warnings
from datetime import datetime
import pandas as pd
from io import StringIO
import time


# 封装登陆接口
def post_main(url, headers, data=None):
    warnings.filterwarnings("ignore")
    response = requests.post(url=url, headers=headers, data=data, verify=False)
    return response


def login_admin():
    url = 'https://adminui.sit.fsx.oddlotx.com//api/admin/auth/login'

    data = json.dumps({
        "email": "zhenghuaimao@farsightedyu.com",
        "password": "Zhm19961225.",
        "verifyCode": 00
    })

    headers = {
        "Content-Type": "application/json"
    }
    get_token = post_main(url, headers, data).json()
    tokendate = get_token["accessToken"]
    token = "Bearer {}".format(tokendate)
    print(
        "-------------------------------login admin success-------------------------------")
    return token


# 生成需要获取的股票文件名
def get_security_master_name():
    daydate = datetime.now()
    day_year = daydate.year
    # day_month = daydate.month
    day_month = 6
    # day_day = daydate.day
    day_day = 30
    if day_day == 1:
        # 判断是否为当月第一天，如果是，就去取上个月最后一天的股票文件
        day_month -= 1
        day_day = calendar.monthrange(day_year, day_month)[1]
    # else:
    # day_day -= 1

    date_staring = f"{day_year}{day_month:02d}{day_day:02d}"
    security_master_name = "/data/RSec/for_FSX/security_master/RSec_security_master_{}.csv".format(date_staring)

    return security_master_name


def get_symbol_data():
    url = "https://adminui.sit.fsx.oddlotx.com//api/statistical-report/download-file"
    data = json.dumps({
        "route": get_security_master_name()
    })
    headers = {
        "Authorization": login_admin(),
        "Content-Type": "application/json"
    }
    get_Symbol_date = post_main(url, headers, data)
    date = get_Symbol_date.text
    print(
        "-------------------------------full stock symbols gen success-------------------------------")
    # 将接口返回的csv文件进行数据转换
    df = pd.read_csv(StringIO(date))
    # 将数据写入fullStockSymbol.xlsx文件中
    df.to_excel("fullStockSymbol.xlsx", index=False)
    # return
    df = pd.read_excel("fullstock_symbol.xlsx")

    return df
