#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import sys

import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
import random

__SOH__ = chr(1)


class Application(fix.Application):
    exec_id = 0
    order_new = 0
    order_ioc_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_fill_indication = 0
    order_tostnet_confirmation = 0
    order_tostnet_rejection = 0
    order_num = 0
    order_book_is_close = 0
    not_book_is_close = []

    def __init__(self):
        super().__init__()
        self.sessionID = None
        self.account = None
        self.Sender = None
        self.Target = None
        self.Host = None
        self.Port = None

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
        logfix.info(f"Result: order_new = {self.order_new}, order_accepted = {self.order_accepted}, "
                    f"order_rejected = {self.order_rejected}, order_book_is_close ={self.order_book_is_close}）")
        logfix.info(
            f"Result: order_edp_indication = {self.order_fill_indication}, "
            f"order_tostnet_confirmation = {self.order_tostnet_confirmation}, order_tostnet_rejection = {self.order_tostnet_rejection}）")

        logfix.info(f"Result: order_ioc_expired = {self.order_ioc_expired}")
        logfix.info(f"Result: not_book_is_close = {self.not_book_is_close}")
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msgtype = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(sendMsg) S >> {msg}")
        if msgtype == "D":
            self.order_new += 1
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")
        execTransType = message.getField(20)
        if execTransType == "2":
            self.order_tostnet_confirmation += 1
            logfix.info(f"(recvMsg)ToSTNeT Confirmation << {msg}")
        else:
            if ordStatus == "0":
                self.order_accepted += 1
                logfix.info(f"(recvMsg) Order Accepted << {msg}")
            elif ordStatus == "8":
                text = message.getField(58)
                self.order_rejected += 1
                logfix.info(f"(recvMsg) Order Rejected << {msg}")
                # 目前该ErrorCode返回的错误码为200开头，后期可能需要修改成000开头
                if 'ERROR_20010064,Book is Closed' in text:
                    self.order_book_is_close += 1
                else:
                    self.not_book_is_close.append(msg)
            elif ordStatus == "4":
                text = message.getField(58)
                if 'ERROR_00010051,Order rejected due to IoC expired.' == text:
                    self.order_ioc_expired += 1
                    logfix.info("(recvMsg) Order IOC Expired << {}".format(msg))
                else:
                    self.order_tostnet_rejection += 1
                    logfix.info("(recvMsg)ToSTNeT Rejection << {}".format(msg))
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
        self.exec_id += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.exec_id).zfill(6)

    def insert_order_request(self, row, account, order_num):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))

        if (order_num % 2) == 0:
            msg.setField(fix.Side("2"))
        else:
            msg.setField(fix.Side("1"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self, account):
        """Run"""
        with open('EDP_FOR_PROD.json', 'r') as f_json:
            order_num = 0
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while order_num < 2:
                order_num += 1
                for row in case_data_list["testCase"]:
                    self.insert_order_request(row, account, order_num)
                    time.sleep(0.004)

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser()
        config.read('edp_fullstock_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_fullstock_client.cfg', 'w') as configfile:
            config.write(configfile)


def main():
    global account
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='RPROD_EDP_ACCOUNT_99', help='choose account to use for test')
        parser.add_argument('--Sender', default='RPROD_EDP_99', help='choose Sender to use for test')
        parser.add_argument('--Target', default='FSX_PROD_EDP', help='choose Target to use for test')
        parser.add_argument('--Host', default='clientgateway99', help='choose Host to use for test')
        parser.add_argument('--Port', default='5001', help='choose Port to use for test')

        # parser.add_argument('--account', default='RSIT_EDP_ACCOUNT_2', help='choose account to use for test')
        # parser.add_argument('--Sender', default='RSIT_EDP_2', help='choose Sender to use for test')
        # parser.add_argument('--Target', default='FSX_SIT_EDP', help='choose Target to use for test')
        # parser.add_argument('--Host', default='52.194.183.77', help='choose Host to use for test')
        # parser.add_argument('--Port', default='30052', help='choose Port to use for test')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.Sender
        target = args.Target
        host = args.Host
        port = args.Port

        cfg = Application()
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        global logfix
        # report
        setup_logger('logfix', f'{account}_report.log')
        logfix = logging.getLogger('logfix')

        settings = fix.SessionSettings("edp_fullstock_client.cfg")
        application = Application()
        application.account = account
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.load_test_case(account)
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
