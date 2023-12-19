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

__SOH__ = chr(1)

# report
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"rolx_report_{current_date}.log"
setup_logger('logfix', 'logs/' + log_filename)
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    orderID = 0
    execID = 0
    ORDERS_DICT = []

    def __init__(self):
        super().__init__()
        self.sessionID = None

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
        print(f"Session (%s) logout ! {sessionID.toString()}")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        logfix.info("-------------------------------------------------------------------------------------------------")
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) New Ack >> {msg}")

        # 7.1 New Order Single
        # if msgType == "D":
        #     orderQty = message.getField(38)
        #     ordType = message.getField(40)
        #     clOrdID = message.getField(11)
        #     side = message.getField(54)
        #     symbol = message.getField(55)
        #     transactTime = message.getField(60)
        #     self.ORDERS_DICT = message.getField(11)
        #
        #     if (clOrdID, orderQty, ordType, side, symbol, transactTime,) != "":
        #     else:
        #         logfix.info("(sendMsg) New Ack >> {}".format(msg) + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        # elif msgType == "F":
        #     clOrdID = message.getField(11)
        #     side = message.getField(54)
        #     symbol = message.getField(55)
        #     transactTime = message.getField(60)
        #
        #     if (clOrdID, side, symbol, transactTime) != "":
        #         logfix.info("(sendMsg) Cancel Ack >> {}".format(msg))
        #     else:
        #         logfix.info("(sendMsg) Cancel Ack >> {}".format(msg) + 'Order Cancel Request FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) recvMsg << {msg}")
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
        # msg.setField(fix.Account(row.get('Account')))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.Account(account))
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

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)

        return msg

    def order_cancel_request(self, row):
        clOrdId = self.ORDERS_DICT
        time.sleep(1)
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("F"))
        msg.setField(fix.Account(account))
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
        config.read('rolx_hrt_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('rolx_hrt_client.cfg', 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


def main():
    global account
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='HRT_UAT_ROLX_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('--sender', default='HRT_UAT_ROLX_D_1', help='choose Sender to use for test')
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

        settings = fix.SessionSettings("rolx_hrt_client.cfg")
        application = Application()
        application.account = account
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

        initiator.start()
        time.sleep(1)
        with open('../../testcases/hrt_test_list.json', 'r') as h_json:
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
