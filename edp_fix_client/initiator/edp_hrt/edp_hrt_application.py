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
from datetime import datetime
from model.logger import setup_logger
import json

__SOH__ = chr(1)

# report
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"edp_report_{current_date}.log"
setup_logger('logfix', 'logs/' + log_filename)
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    orderID = 0
    execID = 0

    def __init__(self):
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print("onCreate : Session ({})".format(sessionID.toString()))
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print("Successful Logon to session '{}'.".format(sessionID.toString()))
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> {}".format(msg))
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        logfix.info("-------------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        # 7.1 New Order Single
        if msgType == "D":
            orderQty = message.getField(38)
            ordType = message.getField(40)
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)

            if (clOrdID, orderQty, ordType, side, symbol, transactTime,) != "":
                logfix.info("(sendMsg) New Ack >> {}".format(msg))
            else:
                logfix.info("(sendMsg) New Ack >> {}".format(msg) + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        elif msgType == "F":
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)
            if (clOrdID, side, symbol, transactTime) != "":
                logfix.info("(sendMsg) Cancel Ack >> {}".format(msg))
            else:
                logfix.info("(sendMsg) Cancel Ack >> {}".format(msg) + 'Order Cancel Request FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << {}".format(msg))
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) recvMsg << {}".format(msg))
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

    def insert_order_request(self, data):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(data.get('Account')))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(int(data.get("OrderQty"))))
        msg.setField(fix.OrdType(data.get("OrdType")))
        msg.setField(fix.Side(data.get("Side")))
        msg.setField(fix.Symbol(data.get("Symbol")))

        # 判断订单类型
        if data.get("Price") == "2":
            msg.setField(fix.Price(data.get("Price")))

        if data.get("TimeInForce") != "":
            msg.setField(fix.TimeInForce(data.get("TimeInForce")))

        if data.get("OrderCapacity") != "":
            msg.setField(fix.OrderCapacity(data.get("OrderCapacity")))

        if data.get("CashMargin") != "":
            msg.setField(fix.CashMargin(data.get("CashMargin")))

        if data.get("SecurityID") != "":
            msg.setField(fix.SecurityID(data.get("SecurityID")))

        if data.get("ExDestination") != "":
            msg.setField(fix.ExDestination(data.get("ExDestination")))

        # 自定义Tag
        if data.get("CrossingPriceType") != "":
            msg.setField(8164, data.get("CrossingPriceType"))

        if data.get("MarginTransactionType") != "":
            msg.setField(8214, data.get("MarginTransactionType"))

        # EDP

        if data.get("MinQty") != "":
            msg.setField(fix.MinQty(int(data.get("MinQty"))))

        if data.get("OrderClassification") != "":
            msg.setField(8060, data.get("OrderClassification"))

        if data.get("SelfTradePreventionId") != "":
            msg.setField(8174, data.get("SelfTradePreventionId"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)
        print(111)

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
        msg.setField(fix.OrigClOrdID(clOrdId))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.Side(row["Side"]))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)
        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写

        print(sender, target, host, port)

        config.read('edp_hrt_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_hrt_client.cfg', 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


def main():
    global data
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--data', help='please enter send data')
        args = parser.parse_args()  # 解析参数

        if args.data:
            data = json.loads(args.data)
        else:
            data = {}
        print(data)
        account = data.get("Account")
        sender = data.get("Sender")
        target = data.get("Target")
        host = data.get("Ip")
        port = data.get("Port")

        print(args.data)

        cfg = Application()
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        settings = fix.SessionSettings("edp_hrt_client.cfg")
        application = Application()
        application.account = account
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

        initiator.start()
        time.sleep(1)
        if data.get("ActionType") == "NewAck":
            application.insert_order_request(data)
        elif data.get("ActionType") == "CancelAck":
            application.order_cancel_request(data)
        time.sleep(10)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
