#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
import json
import random
__SOH__ = chr(1)

# report
setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    orderID = 0
    execID = 0
    ORDERS_DICT = []
    LASTEST_ORDER = {}
    Accepted = 0
    Rejected = 0
    Total = 0
    Filled = 0
    num = 1

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
        logfix.info("Result : Total = {},Accepted = {},Filled = {},Rejected = {}" .format(self.Total, self.Accepted, self.Filled, self.Rejected))
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> %s" % msg)
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(sendMsg) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        self.ORDERS_DICT = message.getField(11)
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")

        if ordStatus == "8":
            logfix.info("(recvMsg) R << %s" % msg)
            self.Rejected = self.Rejected + 1
            self.Accepted = self.Accepted + 1
            logfix.info("Result : Rejected ," + "ordStatus =" + ordStatus)
        elif ordStatus == "0":
            logfix.info("(recvMsg) R << %s" % msg)
            self.Total = self.Total + 1
            self.Accepted = self.Accepted + 1
            logfix.info("Result : Accepted ," + "ordStatus =" + ordStatus)
        elif ordStatus == "2":
            logfix.info("(recvMsg) R << %s" % msg)
            self.Filled = self.Filled + 1
            self.Accepted = self.Accepted + 1
            logfix.info("Result : Filled ," + "ordStatus =" + ordStatus)

        self.onMessage(message, sessionID)
        logfix.info("-------------------------------------------------------------------------------------------------")
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        return '2023900' + str(t) + str(self.execID).zfill(8)

    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account("RUAT_ACCOUNT_6"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(1))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.HandlInst('1'))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        if self.num % 2 == 0:
            msg.setField(fix.Side("2"))
        else:
            msg.setField(fix.Side("1"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def runTestCase(self, row):
        self.insert_order_request(row)

    def load_test_case(self):
        """Run"""
        with open('../case/topix400_case.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while self.num < 127:
                self.num += 1
                for row in case_data_list["testCase"]:
                    self.runTestCase(row)
                    time.sleep(0.004)
