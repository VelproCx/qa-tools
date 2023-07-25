# -*- coding: utf-8 -*-
import json
import logging
import random
import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2_grpc
# import server
import time
from model.logger import setup_logger

AUTH_HOST = 'traderauth.sit.rsec.oddlotx.com:443'
TRADE_HOST = 'traderapi.sit.rsec.oddlotx.com:443'

setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')

USER_INFO = [
    ('HRT_SIT_USER_1', 'hrtsituser1'),
    ('HRT_SIT_USER_2', 'hrtsituser2')
]

ACCOUNT_INFO = [
    'firms/HRT-Clear-Member/accounts/HRT_SIT_ACCOUNT_1',
    'firms/HRT-Clear-Member/accounts/HRT_SIT_ACCOUNT_2'
]


def login(username, password):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(AUTH_HOST, credentials=creds)
    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(username=username, password=password))
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


def InsertOrderEntryFirst(type, side, order_qty, symbol, price, clord_id, account, time_in_force):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    conn = grpc.secure_channel(target=TRADE_HOST, credentials=creds,
                               options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                        ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )
    client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
    # 设置token值
    meta = [('authorization', access_token)]
    # 请求消息体
    response = client.InsertOrder(
        order_entry_api_pb2.InsertOrderRequest(type=type, side=side, order_qty=order_qty, symbol=symbol,
                                               price=price,
                                               clord_id=clord_id,
                                               account=account,
                                               time_in_force=time_in_force),
        metadata=meta)
    logfix.info(response)


def InsertOrderEntrySecond(type, side, order_qty, symbol, price, clord_id, account, time_in_force,
                           selfMatchPreventionId):
    # 获取登陆的response
    res_login = login(USER_INFO[1][0], USER_INFO[1][1])
    # 定义变量接收token
    access_token = res_login.access_token
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    conn = grpc.secure_channel(target=TRADE_HOST, credentials=creds,
                               options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                        ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )
    client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
    # 设置token值
    meta = [('authorization', access_token)]
    # 请求消息体
    response = client.InsertOrder(
        order_entry_api_pb2.InsertOrderRequest(type=type, side=side, order_qty=order_qty, symbol=symbol,
                                               price=price,
                                               clord_id=clord_id,
                                               account=account,
                                               time_in_force=time_in_force,
                                               self_match_prevention_id=selfMatchPreventionId),
        metadata=meta)
    logfix.info(response)


# SIT
# def getOrderQty():
#     # 随机生成Qty1-5
#     orderQty = random.randint(1, 5)
#     return orderQty


def runCase():
    with open('regressionSymbollist.json', 'r') as f_json:
        case_data_list = json.load(f_json)
        time.sleep(1)
        # 循环所有用例，并把每条用例放入runTestCase方法中

        for row in case_data_list["testCase"]:
            # symbol = row["symbol"]
            # print(symbol)
            InsertOrderEntryFirst(2, row['side'], row['order_qty'], row['symbol'], row["price"],
                                  str(genClOrdID()),
                                  ACCOUNT_INFO[0], 1)


if __name__ == '__main__':
    res_login = login(USER_INFO[0][0], USER_INFO[0][1])
    runCase()
