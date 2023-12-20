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

    def __init__(self, account, logger, time_of_running):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger
        self.time_of_running = time_of_running

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
        self.order_book_is_close = 0
        self.not_book_is_close = []

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
        self.logger.info(f"Result: order_new = {self.order_new}, order_accepted = {self.order_accepted}, "
                         f"order_rejected = {self.order_rejected}, order_book_is_close ={self.order_book_is_close}）")
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
        msgtype = message.getHeader().getField(35)
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(sendMsg) S >> {msg}")
        if msgtype == "D":
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
                text = message.getField(58)
                self.order_rejected += 1
                self.logger.info(f"(recvMsg) Order Rejected << {msg}")
                # 目前该ErrorCode返回的错误码为200开头，后期可能需要修改成000开头
                if 'ERROR_20010064,Book is Closed' in text:
                    self.order_book_is_close += 1
                else:
                    self.not_book_is_close.append(msg)
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

    def insert_order_request(self, symbol):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(100))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(symbol))

        msg.setField(fix.Side("2"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self):
        """Run"""
        start_time = datetime.now()
        tor = int(self.time_of_running)

        while True:
            # 获取当前时间
            current_time = datetime.now()
            # 定义时间区间
            time_difference = current_time - start_time
            # 循环股票列表
            for symbol in symbols:
                # 判断时间区间是否小于等于传进来的运行时间参数
                if time_difference <= timedelta(minutes=tor):
                    # 重新计算
                    current_time = datetime.now()
                    time_difference = current_time - start_time
                    if time_difference <= timedelta(minutes=tor):
                        self.insert_order_request(symbol)
                        time.sleep(0.005)
                else:
                    break

            if time_difference > timedelta(minutes=tor):
                return

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read('/app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('/app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.cfg', 'w') as configfile:
            config.write(configfile)


def main():
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

        # report
        setup_logger('logfix', '{}_report.log'.format(account))
        logger = logging.getLogger('logfix')

        with open('/app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/symbol.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                symbol = row[0]
                symbols.append(symbol)

        settings = fix.SessionSettings("/app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.cfg")
        application = Application(account, logger, time_of_running)
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()
        application.load_test_case()

        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
