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

symbols = []


class Application(fix.Application):

    def __init__(self, account, logger, message_num, sleep):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger
        self.message_num = message_num
        self.sleep = sleep

        # 定义变量
        self.exec_id = 0
        self.order_new = 0
        self.order_ioc_expired = 0
        self.order_accepted = 0
        self.order_rejected = 0
        self.order_fill_indication = 0
        self.order_tostnet_confirmation = 0
        self.order_tostnet_rejection = 0
        self.order_num = 0

        # 定义常量
        self.__SOH__ = chr(1)

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print(f"onCreate : Session ({sessionID.toString()})")
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print(f"Successful Logon to session '{sessionID.toString()}'.")
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        # self.logger.info(
        #     "Result: order_new = {}（ order_accepted = {}, order_ioc_expired = {}, order_rejected = {},"
        #     " order_edp_indication = {}, order_tostnet_confirmation = {}, order_tostnet_rejection = {}".format(
        #         self.order_new,
        #         self.order_accepted,
        #         self.order_ioc_expired,
        #         self.order_rejected,
        #         self.order_edp_indication,
        #         self.order_tostnet_confirmation,
        #         self.order_tostnet_rejection
        #     ))

        self.logger.info(f"Result: order_new = {self.order_new} , order_accepted = {self.order_accepted}, "
                         f"order_rejected = {self.order_rejected}）")
        self.logger.info(
            f"Result: order_edp_indication = {self.order_fill_indication}, "
            f"order_tostnet_confirmation = {self.order_tostnet_confirmation}, order_tostnet_rejection = {self.order_tostnet_rejection}）")
        self.logger.info(f"Result: order_ioc_expired = {self.order_ioc_expired}")
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(sendMsg) S >> {msg}")
        if msgType == "D":
            self.order_new += 1
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        ordStatus = message.getField(39)
        msg = message.toString().replace(self.__SOH__, "|")
        execTransType = message.getField(20)
        if execTransType == "2":
            self.order_tostnet_confirmation += 1
            self.logger.info(f"(recvMsg)ToSTNeT Confirmation << {msg}")
        else:
            if ordStatus == "0":
                self.order_accepted += 1
                self.logger.info(f"(recvMsg) Order Accepted << {msg}")
            elif ordStatus == "8":
                self.order_rejected += 1
                self.logger.info(f"(recvMsg) Order Rejected << {msg}")
            elif ordStatus == "4":
                text = message.getField(58)
                if 'ERROR_00010051,Order rejected due to IoC expired.' == text:
                    self.order_ioc_expired += 1
                    self.logger.info(f"(recvMsg) Order IOC Expired << {msg}")
                else:
                    self.order_tostnet_rejection += 1
                    self.logger.info(f"(recvMsg)ToSTNeT Rejection << {msg}")
            elif ordStatus == "1" or ordStatus == "2":
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

    # def gen_order_quantity(self):
    #     # 随机生成Qty1-5
    #     orderQty = random.randint(1, 5)
    #     return orderQty

    def insert_order_request(self, symbol):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        # msg.setField(fix.Account("RUAT_EDP_ACCOUNT_1"))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(100))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(symbol))

        msg.setField(fix.Side("1"))

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
        config.read('edp_performance_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_performance_client.cfg', 'w') as configfile:
            config.write(configfile)


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='RSIT_EDP_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('--sender', default='RSIT_EDP_1', help='choose Sender to use for test')
        parser.add_argument('--target', default='FSX_SIT_EDP', help='choose Target to use for test')
        parser.add_argument('--host', default='10.4.129.151', help='choose Host to use for test')
        parser.add_argument('--port', default='30051', help='choose Port to use for test')
        parser.add_argument('--m', help='choose num')
        parser.add_argument('--s', help='choose num')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port
        message_num = args.m
        sleep = args.s

        # report
        setup_logger('logfix', '{}_report.log'.format(account))
        logger = logging.getLogger('logfix')

        cfg = Application(account, logger, message_num, sleep)
        cfg.sender = sender
        cfg.target = target
        cfg.host = host
        cfg.port = port
        cfg.read_config(sender, target, host, port)

        with open('symbol.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                symbol = row[0]
                symbols.append(symbol)

        settings = fix.SessionSettings("edp_performance_client.cfg")
        application = Application(account, logger, message_num, sleep)
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()
        application.load_test_case()
        sleep_duration = timedelta(minutes=1)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
