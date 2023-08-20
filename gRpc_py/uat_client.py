# -*- coding: utf-8 -*-
import json
import logging
import random
import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2_grpc
import time
from model.logger import setup_logger
import pytz

AUTH_HOST = 'traderauth.uat.rsec.oddlotx.com:443'
TRADE_HOST = 'a5520941d6c304606b40a7c7dd0dbe9b-275250026.ap-northeast-1.elb.amazonaws.com:8000'

setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')

# edp
USER_INFO = [
    ('HRT_UAT_EDP_USER_AMM', 'hrtuatedpuseramm'),
]

ACCOUNT_INFO = [
    'firms/HRT-Clear-Member/accounts/HRT_UAT_EDP_ACCOUNT_1',
]


def login(username, password):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(AUTH_HOST, credentials=creds)
    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(username=username, password=password))
    print(response)
    # print(basic_auth_api_pb2.LoginRequest(username=username, password=password))
    return response


# 获取登陆的response
res_login = login(USER_INFO[0][0], USER_INFO[0][1])
# 定义变量接收token
access_token = res_login.access_token


def genClOrdID():
    execID = 0
    # "随机数生成ClOrdID"
    execID += 1
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    str1 = ''.join([str(i) for i in random.sample(range(0, 9), 6)])
    return str1 + str(t) + str(execID).zfill(6)


# UAT
def InsertOrderEntry(type, side, order_qty, symbol, price, clord_id, account, time_in_force, client_account_id):
    # 证书选择SSL类型
    res_login = login(USER_INFO[0][0], USER_INFO[0][1])
    # 定义变量接收token
    access_token = res_login.access_token

    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    conn = grpc.insecure_channel(target=TRADE_HOST)
    client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
    # 设置token值
    meta = [('authorization', access_token)]
    # 请求消息体
    response = client.InsertOrder(
        order_entry_api_pb2.InsertOrderRequest(type=type, side=side, order_qty=order_qty, symbol=symbol,
                                               price=price,
                                               clord_id=clord_id,
                                               account=account,
                                               time_in_force=time_in_force, client_account_id=client_account_id),
        metadata=meta)
    logfix.info(response)


def genOrderQty():
    # 随机生成Qty1-5
    orderQty = random.randint(1, 5)
    return orderQty


def runCase():
    InsertOrderEntry(2, 2, 2000, '5110.EDP', 12000, str(genClOrdID()), ACCOUNT_INFO[0], 1, 'P.1.4')
    # with open("case.json", "r") as f_json:
    #     case_data_list = json.load(f_json)
    #     time.sleep(2)
    #     num = 0
    #     global access_token
    #     access_token = login()
    #     expiration_time = 14 * 60
    #     last_update_time = time.time()
    #     while num < 188:
    #         current_time = time.time()
    #         elapsed_time = current_time - last_update_time
    #
    #         if elapsed_time >= expiration_time:
    #             # 更新token
    #             access_token = login()
    #             last_update_time = current_time
    #         num += 1
    #         for row in case_data_list["testCase"]:
    #             if num % 2 == 0:
    #                 side = 1
    #                 Market = '.REXB'
    #                 symbol = str(row["Symbol"]) + Market
    #             else:
    #                 side = 2
    #                 Market = '.REXS'
    #                 symbol = str(row["Symbol"]) + Market
    #
    #             InsertOrderEntryFirst(2, side, getOrderQty(), symbol, row["Price"],
    #                                   str(getClOrdID()),
    #                                   'firms/HRT-Clear-Member/accounts/HRT_UAT_ACCOUNT_1', 1)
    #             time.sleep(0.001)


# thread1 = threading.Thread(target=InsertOrderEntryFirst, args=(
#     2, 1, 1, '7267.ROLS', 2999, str(getClOrdID()), 'firms/HRT-Clear-Member/accounts/HRT_UAT_ACCOUNT_1', 1))
if __name__ == '__main__':
    # thread1.start()
    runCase()
