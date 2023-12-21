#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
import random
import math
import sys

sys.path.append("medhod/")
# from get_Symbol import get_Symbol_file

__SOH__ = chr(1)

symbols = []


class Application(fix.Application):
    def __init__(self, account, logger):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger

        # 定义变量
        self.execID = 0
        self.ROL_PROP_BPS_BUY = 0.0022
        self.ROL_PROP_BPS_SELL = 0.0022
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
        self.logger.info(
            f"Result : NewAck ={self.order_new}, Accepted = {self.order_accepted}, Rejected= {self.order_rejected}, "
            f"Expired= {self.order_expired}, Filled = {self.order_filled}, "
            f"PartiallyFilled = {self.order_partially_filled}, Book_is_closed={self.Book_is_closed}")
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        self.logger.info("-------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        # 7.1 New Order Single
        if msgType == "D":
            self.order_new += 1
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取tag及value
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")

        # 7.2 Execution Report – Order Accepted
        if ordStatus == "0":
            self.logger.info(f"(recvMsg) Order Accepted << {msg}, ordStatus = {str(ordStatus)}")
            self.order_accepted += 1

        # 7.3 Execution Report – Order Rejected
        elif ordStatus == "8":
            text = message.getField(58)
            self.logger.info(f"(recvMsg) Order Rej << {msg}, RejRes = {str(text)}")
            self.order_rejected += 1
            if text == "Book is CLOSED":
                self.order_book_is_close += 1
            else:
                self.not_book_is_close.append(msg)

        # 7.7 Execution Report – Trade
        elif ordStatus == "1" or ordStatus == "2":
            side = message.getField(54)
            lastPx = message.getField(169)
            clOrdID = message.getField(11)
            primaryBidPx = float(message.getField(8032))
            primaryAskPx = float(message.getField(8033))
            adjustLastPxBuy = math.ceil(primaryAskPx * (1 + self.ROL_PROP_BPS_BUY))
            adjustLastPxSell = math.floor(primaryBidPx * (1 - self.ROL_PROP_BPS_SELL))

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
                adjustLastPx = math.ceil(primaryAskPx * (1 + self.ROL_PROP_BPS_BUY))
                if adjustLastPx == lastPx:
                    return True
                else:
                    self.logger.info(
                        f'Market Price is not matching, clOrdID：{clOrdID}, adjustLastPx：{str(adjustLastPx)},'
                        f'lastPx: {str(lastPx)}')
            elif side == "2":
                adjustLastPx = math.floor(primaryBidPx * (1 - self.ROL_PROP_BPS_SELL))
                if adjustLastPx == lastPx:
                    return True
                else:
                    self.logger.info(
                        f'Market Price is not matching, clOrdID：{clOrdID}, adjustLastPx：{str(adjustLastPx)},'
                        f'lastPx: {str(lastPx)}')

        #  7.8 Execution Report – End of Day Expired
        elif ordStatus == "C":
            text = message.getField(58)
            self.logger.info(f"(recvMsg) Order Expired << {msg}, ExpireRes = {str(text)}")
            self.order_expired += 1
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        with open('rolx_report.log', 'r') as f:
            content = f.read()
        if 'Market Price is not matching' in content:
            self.logger.info('Market Price is NG')
        else:
            self.logger.info('Market Price is OK')

    # "随机数生成ClOrdID"
    def getClOrdID(self):
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 6)])
        return '2023' + str1 + str(t) + str(self.execID).zfill(8)

    # Order Qty 随机生成
    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    # New Ack Req
    def insert_order_request(self, row, account, order_num):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(self.getOrderQty()))
        # msg.setField(fix.OrderQty(row['OrderQty']))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["symbol"]))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))
        if order_num % 2 == 1:
            msg.setField(fix.Side("1"))
        else:
            msg.setField(fix.Side("2"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    # 加载用例文件
    def load_test_case(self, account):
        """Run"""
        with open('../../testcases/full_stock_List.json', 'r') as f_json:
            order_num = 0
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while order_num < 10:
                order_num += 1
                for row in case_data_list["testCase"]:
                    self.insert_order_request(row, account, order_num)
                    time.sleep(0.0035)

    # def gen_thread(self):
    #     threads = []
    #     for _ in range(5):
    #         t = threading.Thread(target=self.load_test_case())
    #         threads.append(t)
    #     for t in threads:
    #         t.start()

    def read_config(self, Sender, Target, Host, Post):
        config = configparser.ConfigParser()
        config.read('rolx_full_stock_client.cfg')
        config.set('SESSION', 'SenderCompID', Sender)
        config.set('SESSION', 'TargetCompID', Target)
        config.set('SESSION', 'SocketConnectHost', Host)
        config.set('SESSION', 'SocketConnectPort', Post)

        with open('rolx_full_stock_client.cfg', 'w') as configfile:
            config.write(configfile)


def main():
    global account
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='RSIT_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('--Sender', default='RSIT_ROLX_1', help='choose Sender to use for test')
        parser.add_argument('--Target', default='FSX_SIT_ROLX', help='choose Target to use for test')
        parser.add_argument('--Host', default='35.74.32.240', help='choose Host to use for test')
        parser.add_argument('--Port', default='5001', help='choose Port to use for test')

        args = parser.parse_args()
        account = args.account
        sender = args.Sender
        target = args.Target
        host = args.Host
        port = args.Port

        # report
        setup_logger('logfix', 'logs/rolx_report.log')
        logger = logging.getLogger('logfix')

        cfg = Application(account, logger)
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        settings = fix.SessionSettings("rolx_full_stock_client.cfg")
        application = Application(account, logger)
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.load_test_case(account)
        # 执行完所有测试用例后等待时间
        sleep_duration = timedelta(minutes=5)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
