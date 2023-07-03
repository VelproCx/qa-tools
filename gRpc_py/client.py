# -*- coding: utf-8 -*-
import json
import logging
import random
import threading
from datetime import timedelta, datetime

import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc
import server
import time
from model.logger import setup_logger
import pytz

# _HOST = 'a5520941d6c304606b40a7c7dd0dbe9b-275250026.ap-northeast-1.elb.amazonaws.com'
# _PORT = '8000'
_HOST = 'traderapi.sit.rsec.oddlotx.com'
_PORT = '443'

setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')


# # # 获取登陆的response
# res_login = server.uat_user()
# # # 定义变量接收token
# access_token = res_login.access_token
# access_token = None


# def login():
#     # 获取登陆的response
#     res_login = server.uat_user()
#     # 定义变量接收token
#     global access_token
#     access_token = res_login.access_token
#     return access_token


def getClOrdID():
    execID = 0
    # "随机数生成ClOrdID"
    execID += 1
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    str1 = ''.join([str(i) for i in random.sample(range(0, 9), 6)])
    return str1 + str(t) + str(execID).zfill(6)


# UAT
# def InsertOrderEntryFirst(type, side, order_qty, symbol, price, clord_id, account, time_in_force):
#     # 获取登陆的response
#     res_login = server.uat_user()
#     # 定义变量接收token
#     access_token = res_login.access_token
#
#     # 证书选择SSL类型
#     creds = grpc.ssl_channel_credentials()
#
#     conn = grpc.secure_channel(target=_HOST + ':' + _PORT, credentials=creds,
#                                options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
#                                         ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )
#     client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
#     client, channel = connect_orderapi(_HOST + ':' + _PORT, is_secure_channel)
#
#     conn = grpc.insecure_channel(target=_HOST + ':' + _PORT)
#     client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
#     # 设置token值
#     meta = [('authorization', access_token)]
#     # 请求消息体
#     response = client.InsertOrder(
#         order_entry_api_pb2.InsertOrderRequest(type=type, side=side, order_qty=order_qty, symbol=symbol,
#                                                price=price,
#                                                clord_id=clord_id,
#                                                account=account,
#                                                time_in_force=time_in_force),
#         metadata=meta)
#     logfix.info(response)


def CancelOrderEntryFirst(symbol, clord_id, order_id):
    # 获取登陆的response
    res_login = server.sit_user_first()

    # 定义变量接收token
    access_token = res_login.access_token

    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    conn = grpc.secure_channel(target=_HOST + ':' + _PORT, credentials=creds,
                               options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                        ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )
    client = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=conn)
    # 设置token值
    meta = [('authorization', access_token)]
    # 请求消息体

    response = client.CancelOrder(
        order_entry_api_pb2.CancelOrderRequest(symbol=symbol,
                                               clord_id=clord_id,
                                               order_id=order_id
                                               ),
        metadata=meta)
    logfix.info(response)


# SIT

def InsertOrderEntry(type, side, order_qty, symbol, price, clord_id, account, time_in_force):
    # 获取登陆的response
    res_login = server.sit_user()
    # 定义变量接收token
    access_token = res_login.access_token
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    conn = grpc.secure_channel(target=_HOST + ':' + _PORT, credentials=creds,
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


# 定义为线程方法传入的参数
# my_tuple = ()
# 创建线程

# def getOrderQty():
#     # 随机生成Qty1-5
#     orderQty = random.randint(1, 5)
#     return orderQty


# def runCase():
#     with open("case.json", "r") as f_json:
#         case_data_list = json.load(f_json)
#         time.sleep(2)
#         num = 0
#         global access_token
#         access_token = login()
#         expiration_time = 14 * 60
#         last_update_time = time.time()
#         while num < 2:
#             current_time = time.time()
#             elapsed_time = current_time - last_update_time
#
#             if elapsed_time >= expiration_time:
#                 # 更新token
#                 access_token = login()
#                 last_update_time = current_time
#             num += 1
#             for row in case_data_list["testCase"]:
#                 if num % 2 == 0:
#                     side = 1
#                     Market = '.EDP'
#                     symbol = str(row["Symbol"]) + Market
#                 else:
#                     side = 2
#                     Market = '.EDP'
#                     symbol = str(row["Symbol"]) + Market
#
#                 InsertOrderEntryFirst(2, side, getOrderQty(), symbol, row["Price"],
#                                       str(getClOrdID()),
#                                       'firms/HRT-Clear-Member/accounts/HRT_UAT_ACCOUNT_1', 1)
#                 time.sleep(0.001)


thread1 = threading.Thread(target=InsertOrderEntry, args=(
    2, 1, 1, '5110.EDP', 1400, str(getClOrdID()), 'firms/HRT-Clear-Member/accounts/HRT_UAT_ACCOUNT_1', 1))
if __name__ == '__main__':
    thread1.start()
    # runCase()
