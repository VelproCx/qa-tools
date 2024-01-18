#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import csv
import sys

import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import random

__SOH__ = chr(1)

symbols = []


class Application(fix.Application):

    def __init__(self, logger, account, message_num, sleep):
        super().__init__()
        self.logger = logger
        self.account = account
        self.message_num = message_num
        self.sleep = sleep

        self.sessionID = None
        self.exec_id = 0
        self.order_new = 0
        self.order_expired = 0
        self.order_accepted = 0
        self.order_rejected = 0
        self.order_partial_fill = 0
        self.order_fill_indication = 0
        self.order_num = 0

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print("onCreate : Session (%s)" % sessionID.toString())
        time.sleep(1)
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        # self.logsCheck()
        self.logger.info(
            f"result: order_new = {self.order_new}（ order_accepted = {self.order_accepted}, order_rejected = {self.order_rejected}）")
        self.logger.info(
            f"result: order_partial_fill = {self.order_partial_fill} , order_fill_indication = {self.order_fill_indication}")
        self.logger.info(f"Result: order_expired = {self.order_expired}")
        print("Session ({}) logout !".format(sessionID.toString()))
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(Core) S >> %s" % msg)
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(sendMsg) S >> %s" % msg)
        if msgType == "D":
            self.order_new += 1
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")
        if ordStatus == "0":
            self.order_accepted += 1
            self.logger.info(f"(recvMsg) Order Accepted << {msg}")
        elif ordStatus == "8":
            self.order_rejected += 1
            self.logger.info(f"(recvMsg) Order Rejected << {msg}")
        elif ordStatus == "C":
            self.order_expired += 1
            self.logger.info(f"(recvMsg) Order Expired << {msg}")
        elif ordStatus == "1":
            self.order_partial_fill += 1
            self.logger.info(f"(recvMsg) Order Partially Filled Indication<< {msg}")
        elif ordStatus == "2":
            self.order_fill_indication += 1
            self.logger.info(f"(recvMsg) Order Filled Indication<< {msg}")
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def gen_client_order_id(self):
        # "随机数生成ClOrdID"
        self.exec_id += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.exec_id).zfill(6)

    def gen_order_qty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    def insert_order_request(self, symbol):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(self.gen_order_qty()))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(symbol))

        if (self.order_num % 2) == 1:
            msg.setField(fix.Side("1"))
        else:
            msg.setField(fix.Side("2"))

        # 自定义Tag
        msg.setField(8164, "REX")

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self):
        """Run"""
        num = 0
        while num < int(self.message_num):
            num += 1
            sleep_time = float(self.sleep) * 0.001
            time.sleep(sleep_time)
            symbol = symbols[num % len(symbols)]
            self.insert_order_request(symbol)

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read('/app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rex_performance_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('/app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rex_performance_client.cfg',
                  'w') as configfile:
            config.write(configfile)


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('-account', default='RSIT_ACCOUNT_7', help='choose account to use for test')
        parser.add_argument('-sender', default='RSIT_REX_7', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_SIT_REX', help='choose Target to use for test')
        parser.add_argument('-host', default='54.250.107.1', help='choose Host to use for test')
        parser.add_argument('-port', default='5007', help='choose Port to use for test')
        parser.add_argument('-m', help='choose num')
        parser.add_argument('-s', help='choose num')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port
        message_num = args.m
        sleep = args.s

        # report
        setup_logger('logfix', f'{account}_report.log')
        logger = logging.getLogger('logfix')

        cfg = Application(logger, account, message_num, sleep)
        cfg.sender = sender
        cfg.target = target
        cfg.host = host
        cfg.port = port
        cfg.read_config(sender, target, host, port)

        with open('/app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/symbol.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                symbol = row[0]
                symbols.append(symbol)

        settings = fix.SessionSettings(
            "/app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rex_performance_client.cfg")
        application = Application(logger, account, message_num, sleep)
        application.account = account
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()
        application.load_test_case()
        # 执行完所有测试用例后等待时间
        sleep_duration = timedelta(minutes=50)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
