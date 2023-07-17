import calendar
import requests
import json
import warnings
from datetime import datetime

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
    return token


def get_security_master_name(market):
    daydate = datetime.now()
    day_year = daydate.year
    day_month = daydate.month
    day_day = daydate.day
    if day_day == 1:
        # 判断是否为当月第一天，如果是，就去取上个月最后一天的股票文件
        day_month -= 1
        day_day = calendar.monthrange(day_year, day_month)[1]
    else:
        day_day -= 1

    date_staring = f"{day_year}{day_month:02d}{day_day:02d}"
    security_master_name = "/data/HRT/for_FSX/security_master/HRT_trading_universe_{}_{}.csv".format(market,
                                                                                                     date_staring)

    print("股票文件路径：" + security_master_name)
    return security_master_name


def get_symbol_file(market):
    url = "https://adminui.sit.fsx.oddlotx.com//api/statistical-report/download-file"
    data = json.dumps({
        "route": get_security_master_name(market)
    })
    headers = {
        "Authorization": login_admin(),
        "Content-Type": "application/json"
    }
    get_Symbol_date = post_main(url, headers, data)
    date = get_Symbol_date.text

    if date.strip() == "":
        print("接口返回的文本为空,请检查fsxadmin是否已经生成security_master文件")
        return None
    else:
        print(
            "-------------------------------full stock symbols gen success-------------------------------")
        '''
        推导公式表达式：new_list = [expression for item in iterable if condition]
        new_list：生成的新列表，其中包含满足条件的经过表达式处理的元素。
        expression：用于生成新元素的表达式。
        item：从可迭代对象 iterable 中取出的每个元素。
        iterable：可迭代对象，例如列表、字符串等。
        condition（可选）：一个条件，用于过滤元素。
        '''
        # 用换行符将文本数据转换成列表，并且把数据后面带的‘\r’去掉
        data_list = [item.replace('\r', '') for item in date.split('\n') if item.strip()]
        # 去掉列表的第一个数据
        data_list = data_list[1:]
        # 将列表转换成字符串
        json_str = json.dumps(data_list)
        try:
            response_json = json.loads(json_str)
            # response_json 是一个包含接口返回数据的 Python 字典或列表对象
            if not response_json:
                raise Exception("股票列表为空")
        except (json.JSONDecodeError, Exception) as e:
            print(e)
    return response_json




