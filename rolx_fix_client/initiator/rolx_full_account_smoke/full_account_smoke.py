#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import csv
import json
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
    execID = 0
    order_new = 0
    order_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_fill_indication = 0
    order_num = 0
    order_book_is_close = 0
    not_book_is_close = []

    def __init__(self):
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        logfix.info("Result: order_new = {}（ order_accepted = {}, order_rejected = {}, order_book_is_close ={}）".format(
            self.order_new,
            self.order_accepted,
            self.order_rejected,
            self.order_book_is_close))
        logfix.info(
            "Result: order_edp_indication = {}（ order_tostnet_confirmation = {}, order_tostnet_rejection = {}）".format(
                self.order_fill_indication,
                self.order_tostnet_confirmation,
                self.order_tostnet_rejection
            ))
        logfix.info("Result: order_expired = {}".format(
            self.order_expired
        ))

        print("Session ({}) logout !".format(sessionID.toString()))
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> %s" % msg)
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msgtype = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(sendMsg) New Ack >> %s" % msg)
        if msgtype == "D":
            self.order_new += 1
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")

        if ordStatus == "0":
            self.order_accepted += 1
            logfix.info("(recvMsg) Order Accepted << {}".format(msg))
        elif ordStatus == "8":
            self.order_rejected += 1
            logfix.info("(recvMsg) Order Rejected << {}".format(msg))
        elif ordStatus == "4":
            self.order_expired += 1
            logfix.info("(recvMsg) Order Expired End Of Day << {}".format(msg))
        elif ordStatus == "1" or ordStatus == "2":
            self.order_fill_indication += 1
            logfix.info("(recvMsg) Order Filled Indication<< {}".format(msg))
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.execID).zfill(6)

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Symbol(row["Symbol"]))
        if row["OrdType"] == "2":
            msg.setField(fix.Price(row["Price"]))  # 如果值是2，表示是限价单，要设置价格

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self):
        """Run"""

        with open('smoke_case.json', 'r') as f_json:
            case = json.load(f_json)
            time.sleep(1)
            for row in case[{"testCase"}]:
                self.insert_order_request(row)

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read('/app/data/qa-tools/rolx_fix_client/initiator/full_of_smoke/full_account_smoke.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('/app/data/qa-tools/rolx_fix_client/initiator/full_of_smoke/full_account_smoke.cfg',
                  'w') as configfile:
            config.write(configfile)


def main():
    global account
    global time_of_running
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        # parser.add_argument('--account', default='RPROD_EDP_ACCOUNT_99', help='choose account to use for test')
        # parser.add_argument('--Sender', default='RPROD_EDP_99', help='choose Sender to use for test')
        # parser.add_argument('--Target', default='FSX_PROD_EDP', help='choose Target to use for test')
        # parser.add_argument('--Host', default='clientgateway99', help='choose Host to use for test')
        # parser.add_argument('--Port', default='5001', help='choose Port to use for test')

        parser.add_argument('-account', default='RSIT_EDP_ACCOUNT_2', help='choose account to use for test')
        parser.add_argument('-sender', default='RSIT_EDP_2', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_SIT_EDP', help='choose Target to use for test')
        parser.add_argument('-host', default='clientgateway102', help='choose Host to use for test')
        parser.add_argument('-port', default='30052', help='choose Port to use for test')
        parser.add_argument('-tor', default='30052', help='Time of running')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port
        time_of_running = args.tor

        cfg = Application()
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        global logfix
        # report
        setup_logger('logfix', '{}_report.log'.format(account))
        logfix = logging.getLogger('logfix')

        settings = fix.SessionSettings(
            "/app/data/qa-tools/rolx_fix_client/initiator/full_of_smoke/full_account_smoke.cfg")
        application = Application()
        application.account = account
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.load_test_case()

        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
