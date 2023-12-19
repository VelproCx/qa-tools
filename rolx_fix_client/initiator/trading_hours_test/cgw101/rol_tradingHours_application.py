#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
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
setup_logger('logfix', 'report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    order_id = 0
    exec_id = 0
    orders_dict = []
    lastest_order = {}
    success = 0
    fail = 0
    total = 0

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
        print(f"successful Logon to session '{sessionID.toString()}'.")
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        if self.total != self.success + self.fail:
            Miss_Num = self.total - (self.success + self.fail)
            logfix.info(f"Order Miss, Result : total = {self.total},success = {self.success},fail = {self.fail},MissOrderNum = {Miss_Num}")
        else:
            logfix.info(
                f"Order Not Miss, Result : total = {self.total},success = {self.success},fail = {self.fail}")
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(sendMsg) S >> {msg}")
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取clOrdId、ordStatus
        self.orders_dict = message.getField(11)
        ordStatus = message.getField(39)
        msg = message.toString().replace(__SOH__, "|")
        if ordStatus == "2":
            logfix.info(f"(recvMsg)R < < {msg}")
            self.success = self.success + 1
            logfix.info("Result : success," + "OrdStasus = " + ordStatus)
        elif ordStatus == "8":
            logfix.info(f"(recvMsg) R << {msg}")
            self.fail = self.fail + 1
            logfix.info("Result : fail ," + "ordStatus =" + ordStatus)

        self.onMessage(message, sessionID)
        logfix.info("-------------------------------------------------------------------------------------------------")
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.exec_id += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.exec_id).zfill(6)

    def insert_order_request(self, row):
        logfix.info("Test Contexts：" + row["Comment"])
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account("RUAT_ACCOUNT_1"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Symbol(row["Symbol"]))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        if row["TimeInForce"] != "":
            msg.setField(fix.TimeInForce(row["TimeInForce"]))

        if row["Rule80A"] != "":
            msg.setField(fix.Rule80A(row["Rule80A"]))

        if row["CashMargin"] != "":
            msg.setField(fix.CashMargin(row["CashMargin"]))

        # 自定义Tag
        if row["CrossingPriceType"] != "":
            msg.setField(8164, row["CrossingPriceType"])

        if row["MarginTransactionType"] != "":
            msg.setField(8214, row["MarginTransactionType"])

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)
        fix.Session.sendToTarget(msg, self.sessionID)
        self.total = self.total + 1
        return msg

    def runTestCase(self, row):

        action = row["ActionType"]
        if action == 'NewAck':
            self.insert_order_request(row)
        elif action == 'CancelAck':
            self.order_cancel_request(row)

    def load_test_case(self):
        """Run"""
        with open('../../../testcases/Rol_Trading_Hours_Test_Matrix.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(0.04)
            start_Time = datetime.now()

            while start_Time.hour < 15:
                for row in case_data_list["testCase"]:
                    time.sleep(1)
                    endTime = datetime.now()
                    if endTime.hour == 11 and endTime.minute == 30:
                        return
                    else:
                        self.runTestCase(row)
        # while start_Time.hour < 15:
        #     runningTime = datetime.now()
        #     if runningTime.hour < 15:
        #         for row in case_data_list["testCase"]:
        #             time.sleep(1)
        #             self.runTestCase(row)
        #     else:
        #         time.sleep(2)
        #         break


def main():
    try:
        settings = fix.SessionSettings("rol_tradingHours_client.cfg")
        application = Application()
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.load_test_case()
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
