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
setup_logger('logfix', 'logs/report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    execID = 0
    Total = 0
    num = 1
    order_new = 0
    order_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_TosTNeT_rejected = 0
    order_filled = 0
    order_comfirmation = 0

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
        logfix.info(
            "Result : Total = {},Accepted = {},Filled = {},Rejected = {},Expired = {}, TosTNeT_rejected = {}, comfirmation = {}".format(
                self.Total, self.order_accepted,
                self.order_filled,
                self.order_rejected,
                self.order_expired, self.order_TosTNeT_rejected, self.order_comfirmation))
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
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")

        if ordStatus == "8":
            logfix.info("(recvMsg) R << %s" % msg)
            self.order_rejected = self.order_rejected + 1
            self.Total = self.Total + 1
            logfix.info("Result : Rejected ," + "ordStatus =" + ordStatus)
        elif ordStatus == "0":
            logfix.info("(recvMsg) R << %s" % msg)
            self.Total = self.Total + 1
            self.order_accepted = self.order_accepted + 1
            logfix.info("Result : Accepted ," + "ordStatus =" + ordStatus)
        elif ordStatus == "4":
            text = message.getField(58)
            if 'ERROR_20010051,Order rejected due to IoC expired.' == text:
                logfix.info("(recvMsg) R << %s" % msg)
                self.order_expired = self.order_expired + 1
                logfix.info("Result : Expired ," + "ErrorCode =" + text)
            else:
                logfix.info("(recvMsg) R << %s" % msg)
                self.order_TosTNeT_rejected = self.order_TosTNeT_rejected + 1
                logfix.info("Result : ToSTNeT Rejection ," + "ErrorCode =" + text)
        elif ordStatus == "2" or ordStatus == "1":
            execTransType = message.getField(20)
            if execTransType == '0':
                logfix.info("(recvMsg) R << %s" % msg)
                self.order_filled = self.order_filled + 1
                logfix.info("Result : Filled ," + "ordStatus =" + ordStatus)
            else:
                logfix.info("(recvMsg) R << %s" % msg)
                self.order_comfirmation = self.order_comfirmation + 1
                logfix.info("Result : comfirmation ," + "ordStatus =" + ordStatus)
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
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.execID).zfill(6)

    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account('RSIT_EDP_ACCOUNT_5'))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Symbol(row["Symbol"]))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))
        if row["OrdType"] == "2":
            msg.setField(fix.Price(row["Price"]))

        if (self.num % 2) == 0:
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
        with open('../../../testcases/edp_Load_Test_Matrix.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while self.num < 6:
                self.num += 1
                for row in case_data_list["testCase"]:
                    self.runTestCase(row)
                    time.sleep(0.004)
