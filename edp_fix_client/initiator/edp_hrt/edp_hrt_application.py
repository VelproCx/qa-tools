#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import random
import sys
import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json


class Application(fix.Application):

    def __init__(self, account, logger):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger

        # 定义变量
        self.order_id = 0
        self.exec_id = 0
        self.orders_dict = []

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
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(self.__SOH__, "|")
        # 7.1 New Order Single
        if msgType == "D":
            orderQty = message.getField(38)
            ordType = message.getField(40)
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)
            self.orders_dict = message.getField(11)

            if (clOrdID, orderQty, ordType, side, symbol, transactTime,) != "":
                self.logger.info(f"(sendMsg) New Ack >> {msg}")
            else:
                self.logger.info(f"(sendMsg) New Ack >> {msg}" + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        elif msgType == "F":
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)

            if (clOrdID, side, symbol, transactTime) != "":
                self.logger.info(f"(sendMsg) Cancel Ack >> {msg}")
            else:
                self.logger.info(f"(sendMsg) Cancel Ack >> {msg}" + 'Order Cancel Request FixMsg Error!')
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

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Symbol(row["Symbol"]))

        # 判断订单类型
        if row["OrdType"] == "2":
            msg.setField(fix.Price(int(row["Price"])))

        if row["TimeInForce"] != "":
            msg.setField(fix.TimeInForce(row["TimeInForce"]))

        if row["OrderCapacity"] != "":
            msg.setField(fix.OrderCapacity(row["OrderCapacity"]))

        if row["CashMargin"] != "":
            msg.setField(fix.CashMargin(row["CashMargin"]))

        if row["SecurityID"] != "":
            msg.setField(fix.SecurityID(row["SecurityID"]))

        if row["ExDestination"] != "":
            msg.setField(fix.ExDestination(row["ExDestination"]))

        # 自定义Tag
        if row["CrossingPriceType"] != "":
            msg.setField(8164, row["CrossingPriceType"])

        if row["MarginTransactionType"] != "":
            msg.setField(8214, row["MarginTransactionType"])

        # 自定义tag：
        msg.setField(16606, "MM_FIRM_1")

        # EDP

        if row["MinQty"] != "":
            msg.setField(fix.MinQty(int(row["MinQty"])))

        if row["OrderClassification"] != "":
            msg.setField(8060, row["OrderClassification"])

        if row["SelfTradePreventionId"] != "":
            msg.setField(8174, row["SelfTradePreventionId"])

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)

        return msg

    def order_cancel_request(self, row):
        clOrdId = self.orders_dict
        time.sleep(1)
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("F"))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.OrigClOrdID(clOrdId))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.Side(row["Side"]))
        if row["SecurityID"] != "":
            msg.setField(fix.SecurityID(row["SecurityID"]))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)
        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

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
            config.write(configfile, space_around_delimiters=False)


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='HRT_UAT_EDP_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('--sender', default='HRT_UAT_EDP_D_1', help='choose Sender to use for test')
        parser.add_argument('--target', default='s_t2', help='choose Target to use for test')
        parser.add_argument('--host', default='10.2.143.128', help='choose Host to use for test')
        parser.add_argument('--port', default='11131', help='choose Port to use for test')
        args = parser.parse_args()  # 解析参数

        # if args.data:
        #     data = json.loads(args.data)
        # else:
        #     data = {}
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port

        cfg = Application()
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        # report
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"edp_report_{current_date}.log"
        setup_logger('logfix', 'logs/' + log_filename)
        logger = logging.getLogger('logfix')

        settings = fix.SessionSettings("edp_hrt_client.cfg")
        application = Application(account, logger)
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

        initiator.start()
        time.sleep(1)
        with open('../../testcases/hrt_Test_List.json', 'r') as h_json:
            case_data_list = json.load(h_json)
            for row in case_data_list["testCase"]:
                if row["ActionType"] == "NewAck":
                    application.insert_order_request(row)
                elif row["ActionType"] == "CancelAck":
                    application.order_cancel_request(row)
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
