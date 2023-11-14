# -*- coding: utf-8 -*-
from multiprocessing import cpu_count
import logging
import threading
import json
import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc, order_api_pb2, order_api_pb2_grpc
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2_grpc
import sys
import time
from model.logger import setup_logger
from multiprocessing.pool import ThreadPool
import time
import argparse
import random
from datetime import datetime
import csv

# TRADE_HOST = 'a5520941d6c304606b40a7c7dd0dbe9b-275250026.ap-northeast-1.elb.amazonaws.com:8000'
# AUTH_HOST = 'traderauth.uat.rsec.oddlotx.com:443'

AUTH_HOST = 'traderauth.sit.rsec.oddlotx.com:443'
TRADE_HOST = 'traderapi.sit.rsec.oddlotx.com:443'

setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')

creds = grpc.ssl_channel_credentials()

USER_INFO = [
    ('HRT_SIT_EDP_USER_1', 'hrtsitedpuser1'),
]

ACCOUNT_INFO = [
    'firms/HRT-Clear-Member/accounts/HRT_SIT_EDP_ACCOUNT_1',
]

# USER_INFO = [
#     ('HRT_UAT_EDP_USER_AMM', 'hrtuatedpuseramm'),
#     ('R-Sec_UAT_EDP_USER_2', 'rsecuatedpuser2')
# ]
#
# ACCOUNT_INFO = [
#     'firms/HRT-Clear-Member/accounts/HRT_UAT_EDP_ACCOUNT_1',
#     'firms/Clear-Member/accounts/RUAT_EDP_ACCOUNT_2'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_3'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_4'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_5'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_6'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_7'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_8'
#     'firms/Clear-Member/accounts/RPROD_ACCOUNT_9'
# ]

symbols = []


def genClOrdID(thread_id, num):
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    # clOrderId = '9002022' + str(t) + str(execID).zfill(8)
    clOrderId = 'SINGLE' + str(thread_id).zfill(3) + \
                str(t) + str(num).zfill(8)
    # print("clOrderId : " + clOrderId)
    return clOrderId


def login(username, password):
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(AUTH_HOST, credentials=creds)

    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(
        username=username, password=password))
    return response


# def InsertOrderEntry(threadId, client, num_of_message, type, side, order_qty, symbol, price, account, access_token, time_in_force):
def InsertOrderEntry(threadId, client, num_of_message, type, side, order_qty, account, access_token, time_in_force):
    meta = [('authorization', access_token)]
    # 请求消息体
    num = 0
    start_time = time.time()
    while num < num_of_message:
        current_time = time.time()

        if current_time - start_time >= 840:
            refresh = login(username, password)
            refresh_token = refresh.access_token
            meta = [('authorization', refresh_token)]
            logfix.info(f"刷新了access_token: {meta}")
            # 更新开始时间
            start_time = current_time

        sleep_time = float(args.sleep) * 0.001  # 将5解释为0.005秒
        time.sleep(sleep_time)
        num += 1
        clord_id = str(genClOrdID(
            threadId, num))
        logfix.debug("Thread-" + str(threadId) +
                     " Send Request Last ," + "SendNum = " + str(num))
        response = client.InsertOrder(
            order_entry_api_pb2.InsertOrderRequest(type=type, side=side, order_qty=order_qty,
                                                   symbol=symbols[num % len(symbols)],
                                                   price=num % len(symbols) + 1,
                                                   clord_id=clord_id,
                                                   account=account,
                                                   time_in_force=time_in_force,
                                                   client_account_id="P.1.3"),
            metadata=meta)
        logfix.debug("Thread-" + str(threadId) +
                     " EP3 response  SendNum = " + str(num) + " " + str(response))
        # logfix.info(response)


def createOrderEntryConnection(access_token, account):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    # channel = grpc.insecure_channel(target=TRADE_HOST)
    channel = grpc.secure_channel(target=TRADE_HOST, credentials=creds,
                                  options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                           ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )

    connection = order_entry_api_pb2_grpc.OrderEntryAPIStub(channel=channel)
    return connection


def createOrderConnection(access_token, account):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(target=TRADE_HOST, credentials=creds,
                                  options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                           ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )

    connection = order_api_pb2_grpc.OrderAPIStub(channel=channel)
    return connection


def startLoad(connection, access_token, account, num_of_thread, num_of_message):
    # items = [(i, connection, num_of_message, 2, 2, 100, symbol[i%10], 10,
    items = [(i, connection, num_of_message, 2, 2, 100,
              account, access_token, 1) for i in range(num_of_thread)]
    ### TIME_IN_FORCE_IMMEDIATE_OR_CANCEL = 3
    with ThreadPool(num_of_thread) as pool:
        for result in pool.starmap(InsertOrderEntry, items):
            pass


def startBatch(order_entry_connection, order_connection, access_token, account, username, num_of_thread, num_of_message,
               batch):
    clord_id = "BATCH" + datetime.now().strftime("%Y%m%d%H%M%S")
    logfix.info("clord_id  ---  {} ".format(clord_id))
    meta = [('authorization', access_token)]
    orders = order_entry_api_pb2.InsertOrderListRequest()
    for i in range(batch):
        order = order_entry_api_pb2.InsertOrderRequest(
            type="ORDER_TYPE_LIMIT",
            side="SIDE_BUY",
            order_qty=100,
            symbol="1301.EDP",
            price=39900,
            clord_id=clord_id + '_' + str(i),
            account=account,
            user=username,
            time_in_force="TIME_IN_FORCE_DAY")
        ### TIME_IN_FORCE_IMMEDIATE_OR_CANCEL = 3
        # print(order)
        orders.requests.append(order)

    items = [(i, order_entry_connection, num_of_message, orders,
              clord_id, meta) for i in range(num_of_thread)]

    with ThreadPool(num_of_thread) as pool:
        for result in pool.starmap(loadBatch, items):
            pass
    pool.join()


def loadBatch(thread_id, order_entry_connection, num_of_message, orders, clord_id, meta):
    logfix.info("start thread {} ---".format(thread_id))
    num = 0
    while num < num_of_message:
        num += 1
        response = order_entry_connection.InsertOrderList(
            orders, metadata=meta)
        logfix.debug(" batch order response ==" + str(response))


if __name__ == '__main__':

    # get the number of logical cpu cores
    n_cores = cpu_count()
    # report the number of logical cpu cores
    logfix.info(f'Number of Logical CPU cores: {n_cores}')

    parser = argparse.ArgumentParser(description='EP3 load test tool')

    # parser.add_argument("trade-server", help="trade api server")
    # parser.add_argument("trade-api", help="positional argument 1")
    # parser.add_argument("auth_api", help="auth api server")

    parser.add_argument('-m', '--message', type=int, default=2,
                        help='number of message to send per thread')

    parser.add_argument('-t', '--thread', type=int, default=1,
                        help='number of message to send per thread')

    parser.add_argument('-u', '--user_id', type=int, default=1,
                        help='user id to use for test')

    parser.add_argument('-a', '--account_id', type=int, default=1,
                        help='account id to use for test')

    parser.add_argument('-l', '--log-level', default="INFO", choices=['INFO', 'DEBUG'],
                        help='set log level')

    parser.add_argument('-k', '--kind', default="SINGLE", choices=['SINGLE', 'BATCH'],
                        help='single or batch insert order')

    parser.add_argument('--symbol', default="7267.ROLB",
                        help='account id to use for test)')

    parser.add_argument('-b', '--batch', type=int, default=2,
                        help='number of order in batch request')

    parser.add_argument('-s', '--sleep', default=5,
                        help='number of order in batch request')

    args = parser.parse_args()

    logfix.setLevel(args.log_level)

    logfix.info(
        "load test start at --- {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    logfix.info("running command --- {}".format(" ".join(sys.argv)))
    start_time = time.time()

    account = ACCOUNT_INFO[args.account_id - 1]
    (username, password) = USER_INFO[args.user_id - 1]
    logfix.info("user:" + username + "  account: " + account)

    with open('symbol.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            symbol = row[0]
            symbols.append(symbol)

    # 获取登陆的response
    login_time = time.time()
    logfix.info("start login --- %s seconds ---" % login_time)
    login_info = login(username, password)
    connection_time = time.time()
    logfix.info("start connection  --- %s seconds ---" % connection_time)

    order_entry_connection = createOrderEntryConnection(
        login_info.access_token, args.account_id)

    load_time = time.time()

    if args.kind == "SINGLE":
        logfix.info("start load --- %s seconds ---" % connection_time)
        startLoad(order_entry_connection, login_info.access_token,
                  account, args.thread, args.message)

        logfix.info(
            "finished --- {} messages per thread, total  {} threads, total {} messages in {} seconds ---".format(
                args.message, args.thread, (args.message * args.thread), (time.time() - start_time)))

    if args.kind == "BATCH":
        logfix.info("start batch --- {} seconds ---".format(connection_time))
        order_connection = createOrderConnection(
            login_info.access_token, args.account_id)
        startBatch(order_entry_connection, order_connection,
                   login_info.access_token, account, username, args.thread, args.message, args.batch)

        total_orders = args.batch * args.message * args.thread
        total_orders_per_thread = args.batch * args.message
        time_spent = time.time() - start_time
        total_throughput = total_orders / time_spent
        thread_throughput = total_throughput / args.thread
        logfix.info(
            "finished --- {} orders per message, {} messages per thread, total  {} threads, overall {} orders in {} seconds, total throughput  {} orders per seconds , throughput per thread {} orders per seconds ---".format(
                args.batch, args.message, args.thread, (total_orders), (time_spent), (total_throughput),
                (thread_throughput)))
