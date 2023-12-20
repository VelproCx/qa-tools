#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import csv
import random
import sys
import threading
import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger

symbols = []
security_ids = []


class Application(fix.Application):

    def __init__(self, account, logger, message_num, sleep):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger
        self.message_num = message_num
        self.sleep = sleep

        # 定义变量
        self.order_id = 0
        self.exec_id = 0

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
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(sendMsg) New Ack >> {msg}")
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) recvMsg << {msg}")
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

    def insert_order_request(self, symbol, price, securityID):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        # msg.setField(fix.Account("RUAT_EDP_ACCOUNT_1"))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(100))
        msg.setField(fix.OrdType("2"))
        msg.setField(fix.Symbol(symbol))
        msg.setField(fix.Price(price))

        msg.setField(fix.Side("2"))
        msg.setField(fix.OrderCapacity('P'))
        msg.setField(fix.ExDestination("EiB MarketEiB"))
        msg.setField(fix.TimeInForce("0"))
        msg.setField(fix.CashMargin("1"))
        msg.setField(fix.SecurityID(securityID))
        msg.setField(8164, "EDP")
        msg.setField(8214, "0")
        msg.setField(fix.MinQty(0))
        msg.setField(8060, "3")
        msg.setField(8174, "0")
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
            price = num % len(symbols) + 1
            securityID = security_ids[num % len(security_ids)]
            self.insert_order_request(symbol, price, securityID)

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read('edp_hrt_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_hrt_client.cfg', 'w') as configfile:
            config.write(configfile)


def convert_stock_code(stock_code):
    digits = "0123456789"
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    slice_char = stock_code[:4]
    for char in slice_char:
        if char.isdigit():
            # 处理数字位
            digit = str(digits.index(char)).zfill(2)
            result += digit
        elif char.isalpha():
            # 处理字母位
            letter = str(letters.index(char.upper()) + 10)
            result += letter

    return result


class Threads(threading.Thread):
    def __init__(self, application):
        super().__init__()
        self.application = application

    def run(self):
        self.application.load_test_case()


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        # 20服务器
        # parser.add_argument('-account', default='HRT_SIT_EDP_ACCOUNT_2', help='choose account to use for test')
        # parser.add_argument('-sender', default='TRADER_C', help='choose Sender to use for test')
        # parser.add_argument('-target', default='terminal_1', help='choose Target to use for test')
        # parser.add_argument('-host', default='192.168.0.20', help='choose Host to use for test')
        # parser.add_argument('-port', default='11113', help='choose Port to use for test')

        parser.add_argument('--account', default='HRT_SIT_EDP_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('--sender', default='HRT_SIT_EDP_D_1', help='choose Sender to use for test')
        parser.add_argument('--target', default='s_t2', help='choose Target to use for test')
        parser.add_argument('--host', default='10.4.128.117', help='choose Host to use for test')
        parser.add_argument('--port', default='11131', help='choose Port to use for test')
        parser.add_argument('-m', help='Please enter the order quantity')
        parser.add_argument('-s', help='Please enter the delay')
        parser.add_argument('-t', help='Please enter the number of threads')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port
        message_num = args.m
        sleep = args.s
        ord_threads = args.t

        cfg = Application()
        cfg.sender = sender
        cfg.target = target
        cfg.host = host
        cfg.port = port
        cfg.read_config(sender, target, host, port)

        # report
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"edp_report_{current_date}.log"
        setup_logger('logfix', 'logs/' + log_filename)
        logger = logging.getLogger('logfix')

        with open('symbol.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                symbol = row[0]
                securityID = "5" + convert_stock_code(symbol)
                security_ids.append(securityID)
                symbols.append(symbol)

        settings = fix.SessionSettings("edp_hrt_client.cfg")
        application = Application(account, logger, message_num, sleep)
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()
        # 创建线程并发运行 load_test_case 方法
        threads = []
        for _ in range(int(ord_threads)):
            thread = Threads(application)
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

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
