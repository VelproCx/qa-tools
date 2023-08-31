#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import threading

import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
import random

__SOH__ = chr(1)

# report
setup_logger('logfix', 'report_107.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    execID = 0
    order_new = 0
    order_ioc_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_fill_indication = 0
    order_tostnet_confirmation = 0
    order_tostnet_rejection = 0
    order_num = 0

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
        self.logsCheck()
        # logfix.info(
        #     "Result: order_new = {}（ order_accepted = {}, order_ioc_expired = {}, order_rejected = {},"
        #     " order_edp_indication = {}, order_tostnet_confirmation = {}, order_tostnet_rejection = {}".format(
        #         self.order_new,
        #         self.order_accepted,
        #         self.order_ioc_expired,
        #         self.order_rejected,
        #         self.order_edp_indication,
        #         self.order_tostnet_confirmation,
        #         self.order_tostnet_rejection
        #     ))

        logfix.info("Result: order_new = {}（ order_accepted = {}, order_rejected = {}）".format(self.order_new,
                                                                                               self.order_accepted,
                                                                                               self.order_rejected, ))
        logfix.info(
            "Result: order_edp_indication = {}（ order_tostnet_confirmation = {}, order_tostnet_rejection = {}）".format(
                self.order_fill_indication,
                self.order_tostnet_confirmation,
                self.order_tostnet_rejection
            ))
        logfix.info("Result: order_ioc_expired = {}".format(
            self.order_ioc_expired
        ))
        print("Session ({}) logout !".format(sessionID.toString()))
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> %s" % msg)
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        msgtype = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(sendMsg) S >> %s" % msg)
        if msgtype == "D":
            self.order_new += 1
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
        execTransType = message.getField(20)
        if execTransType == "2":
            self.order_tostnet_confirmation += 1
            logfix.info("(recvMsg)ToSTNeT Confirmation << {}".format(msg))
        else:
            if ordStatus == "0":
                self.order_accepted += 1
                logfix.info("(recvMsg) Order Accepted << {}".format(msg))
            elif ordStatus == "8":
                self.order_rejected += 1
                logfix.info("(recvMsg) Order Rejected << {}".format(msg))
            elif ordStatus == "4":
                text = message.getField(58)
                if 'ERROR_00010051,Order rejected due to IoC expired.' == text:
                    self.order_ioc_expired += 1
                    logfix.info("(recvMsg) Order IOC Expired << {}".format(msg))
                else:
                    self.order_tostnet_rejection += 1
                    logfix.info("(recvMsg)ToSTNeT Rejection << {}".format(msg))
            elif ordStatus == "1" or ordStatus == "2":
                self.order_fill_indication += 1
                logfix.info("(recvMsg) Order Filled Indication<< {}".format(msg))
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

    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account("RSIT_EDP_ACCOUNT_7"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(100))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))

        if (self.order_num % 2) == 0:
            msg.setField(fix.Side("2"))
        else:
            msg.setField(fix.Side("1"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self):
        """Run"""
        with open('uat_test_with_hrt.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while self.order_num < 2000:
                self.order_num += 1
                for row in case_data_list["testCase"]:
                    self.insert_order_request(row)
                    time.sleep(0.0035)

    def gen_thread(self):
        threads = []
        for _ in range(5):
            t = threading.Thread(target=self.load_test_case())
            threads.append(t)
        for t in threads:
            t.start()


def main():
    try:
        settings = fix.SessionSettings("edp_performance107_client.cfg")
        application = Application()
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.gen_thread()
        sleep_duration = timedelta(minutes=10)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()