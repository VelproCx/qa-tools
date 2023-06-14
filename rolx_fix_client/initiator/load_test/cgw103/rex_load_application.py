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
    Success = 0
    Fail = 0
    Total = 0

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
        logfix.info("Result : Total = %d,Success = %d,Fail = %d" % (self.Total, self.Success, self.Fail))
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
            self.Total = self.Total + 1
            self.Fail = self.Fail + 1
            logfix.info("Result : Fail ," + "ordStatus =" + ordStatus)
        else:
            logfix.info("(recvMsg) R << %s" % msg)
            self.Total = self.Total + 1
            self.Success = self.Success + 1
            logfix.info("Result : Success ," + "ordStatus =" + ordStatus)

        self.onMessage(message, sessionID)
        logfix.info("-------------------------------------------------------------------------------------------------")
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching


    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        return '9002023' + str(t) + str(self.execID).zfill(8)

    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty


    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account("RUAT_ACCOUNT_3"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(self.getOrderQty()))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.HandlInst('1'))
        msg.setField(fix.Side("1"))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        # 自定义Tag
        msg.setField(8164, "REX")

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg
        time.sleep(1)

    def runTestCase(self, row):
        self.insert_order_request(row)

    def load_test_case(self):
        """Run"""
        with open('../case/top500.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            num = 0
            while num < 45:
                num += 1
                for row in case_data_list["testCase"]:
                    self.runTestCase(row)
                    time.sleep(0.004)
