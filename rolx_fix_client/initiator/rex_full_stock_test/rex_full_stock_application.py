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
import random
import math
import csv

symbols = []


class Application(fix.Application):

    def __init__(self, account, logger):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger

        # 定义变量
        self.exec_id = 0
        self.REX_PROP_BPS_BUY = 0.0022
        self.REX_PROP_BPS_SELL = 0.0022
        self.order_new = 0
        self.order_expired = 0
        self.order_accepted = 0
        self.order_rejected = 0
        self.order_filled = 0
        self.order_partially_filled = 0
        self.order_num = 0
        self.order_book_is_close = 0
        self.not_book_is_close = []

        # 定义常量
        self.__SOH__ = chr(1)
        self.exec_id = 0

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
        self.logs_check()
        self.logger.info(
            f"Result : NewAck ={self.order_new}, Accepted = {self.order_accepted}, Rejected= {self.order_rejected}, "
            f"Expired= {self.order_expired}, Filled = {self.order_filled}, "
            f"PartiallyFilled = {self.order_partially_filled}, Book_is_closed={self.order_book_is_close}")
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        self.logger.info("-------------------------------------------------------------------------------------------")
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        self.logger.info("-------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(self.__SOH__, "|")
        # 7.1 New Order Single
        if msgType == "D":
            self.order_new += 1
            self.logger.info(f"(Core) S >> {msg}")
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        self.logger.info("-------------------------------------------------------------------------------------------")
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        ordStatus = message.getField(39)
        msg = message.toString().replace(self.__SOH__, "|")

        # 7.2 Execution Report – Order Accepted
        if ordStatus == "0":
            self.logger.info(f"(recvMsg) Order Accepted << {msg}, ordStatus = {str(ordStatus)}")
            self.order_accepted += 1

        # 7.7 Execution Report – Trade
        elif ordStatus == "1" or ordStatus == "2":
            side = message.getField(54)
            lastPx = float(message.getField(31))
            clOrdID = message.getField(11)
            primaryLastPx = float(message.getField(8031))
            adjustLastPxBuy = math.ceil(primaryLastPx * (1 + self.REX_PROP_BPS_BUY))
            adjustLastPxSell = math.floor(primaryLastPx * (1 - self.REX_PROP_BPS_SELL))
            # Trade Tags is null check
            if ordStatus == "1":
                self.order_partially_filled += 1
                self.logger.info(f"(recvMsg) Order Partially Filled << {msg}, Side: {str(side)}, Fill Price: "
                                 f"{str(lastPx)}, AdjustLastPx Of Buy: {str(adjustLastPxBuy)}, AdjustLastPx Of Sell:"
                                 f"{str(adjustLastPxSell)}")
            else:
                self.order_filled += 1
                self.logger.info(f"(recvMsg) Order Filled << {msg}, Side: {str(side)}, Fill Price: "
                                 f"{str(lastPx)}, AdjustLastPx Of Buy: {str(adjustLastPxBuy)}, AdjustLastPx Of Sell:"
                                 f"{str(adjustLastPxSell)}")
            # Fill Price Check
            if side == "1":
                adjustLastPx = math.ceil(primaryLastPx * (1 + self.REX_PROP_BPS_BUY))
                if adjustLastPx != lastPx:
                    self.logger.info(
                        f'Market Price is not matching, clOrdID：{clOrdID}, adjustLastPx：{str(adjustLastPx)},'
                        f'lastPx: {str(lastPx)}')

            elif side == "2":
                adjustLastPx = math.floor(primaryLastPx * (1 - self.REX_PROP_BPS_SELL))
                if adjustLastPx != lastPx:
                    self.logger.info(
                        f'Market Price is not matching, clOrdID：{clOrdID}, adjustLastPx：{str(adjustLastPx)},'
                        f'lastPx: {str(lastPx)}')

        #  7.8 Execution Report – End of Day Expired
        elif ordStatus == "C":
            self.logger.info(f"(recvMsg) Order Expired << {msg}")
            self.order_expired += 1

        # 7.3 Execution Report – Order Rejected
        elif ordStatus == "8":
            text = message.getField(58)
            self.logger.info(f"(recvMsg) Order Rej << {msg}")
            self.order_rejected += 1
            if text == "Book is CLOSED":
                self.order_book_is_close += 1
            else:
                self.not_book_is_close.append(msg)

        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching
    def logs_check(self):
        with open('logs/rex_report.log', 'r') as f:
            content = f.read()
        if 'Market Price is not matching' in content:
            self.logger.info('Market Price is NG')
        else:
            self.logger.info('Market Price is OK')

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

        # 自定义Tag
        msg.setField(8164, "REX")

        if (self.order_num % 2) == 1:
            msg.setField(fix.Side("1"))
        else:
            msg.setField(fix.Side("2"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self):
        """Run"""
        # 循环所有用例，并把每条用例放入runTestCase方法中，
        while self.order_num < 2:
            self.order_num += 1
            for symbol in symbols:
                self.insert_order_request(symbol)
                time.sleep(0.04)

    def read_config(self, sender, target, host, post):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read(
            '/app/data/qa-tools/rolx_fix_client/initiator/rex_full_stock_test/rex_full_stock_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', post)

        with open(
                '/app/data/qa-tools/rolx_fix_client/initiator/rex_full_stock_test/rex_full_stock_client.cfg', 'w'
        ) as configfile:
            config.write(configfile)


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('-account', default='RSIT_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('-sender', default='RSIT_1', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_SIT_CGW_1', help='choose Target to use for test')
        parser.add_argument('-host', default='10.4.65.1', help='choose Host to use for test')
        parser.add_argument('-port', default='5001', help='choose Port to use for test')

        args = parser.parse_args()
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port

        # report
        setup_logger('logfix', '/app/data/qa-tools/rolx_fix_client/initiator/rex_full_stock_test/logs/rex_report.log')
        logger = logging.getLogger('logfix')

        cfg = Application(account, logger)
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        with open("/app/data/qa-tools/rolx_fix_client/initiator/rex_full_stock_test/symbol.csv", "r",
                  newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                symbol = row[0]
                symbols.append(symbol)

        settings = fix.SessionSettings(
            "/app/data/qa-tools/rolx_fix_client/initiator/rex_full_stock_test/rex_full_stock_client.cfg")
        application = Application(account, logger)
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
