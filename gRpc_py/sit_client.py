# -*- coding: utf-8 -*-
import json
import logging
import random
import threading

import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc
import server
import time
from model.logger import setup_logger

_HOST = 'traderapi.sit.rsec.oddlotx.com'
_PORT = '443'

setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')


# # # 获取登陆的response
# res_login = server.uat_user()
# # # 定义变量接收token
# access_token = res_login.access_token

def login():
    # 获取登陆的response
    res_login = server.sit_user()
    # 定义变量接收token
    access_token = res_login.access_token
    return access_token


access_token = login()


def getClOrdID():
    execID = 0
    # "随机数生成ClOrdID"
    execID += 1
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    str1 = ''.join([str(i) for i in random.sample(range(0, 9), 6)])
    return str1 + str(t) + str(execID).zfill(6)


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


# SIT
def getOrderQty():
    # 随机生成Qty1-5
    orderQty = random.randint(1, 5)
    return orderQty


def runCase():
    InsertOrderEntry(2, 2, 1000, '5110.EDP', 1400,
                     str(getClOrdID()),
                     'firms/HRT-Clear-Member/accounts/HRT_SIT_ACCOUNT_1', 1)
    time.sleep(0.001)


if __name__ == '__main__':
    login()
    runCase()
