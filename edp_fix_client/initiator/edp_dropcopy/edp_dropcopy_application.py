#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import difflib
import os
import random
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
import json
from openpyxl import load_workbook
from gRpc_py import sit_client

__SOH__ = chr(1)

from importlib.machinery import SourceFileLoader

# 获取当前所在目录绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
# 将当前目录的路径和上级目录的绝对路径拼接
Parent_path = os.path.abspath(os.path.join(current_path, "../../method"))
grpc_path = os.path.abspath(os.path.join(current_path, "../../../gRpc_py"))
# 获取上级目录中一个文件的路径
generation_path = os.path.join(Parent_path, "file_generation.py")
# 获取data_comparsion
data_comparison_path = os.path.join(Parent_path, "data_comparison.py")
# 获取gRpc发单脚本路径
sit_client_path = os.path.join(grpc_path, "sit_client.py")


# log
setup_logger('logfix', 'logs/edp_report.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):

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
        # "客户端断开连接时候调用此方法"
        print("Session (%s) logout !" % sessionID.toString())
        self.writeResExcel('report/edp_report.xlsx', self.Result, 2, 'S')
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
                self.order_new += 1
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
        logfix.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        # "接收业务消息时调用此方法"
        logfix.info("-------------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        if msgType == "j":
            refSeqNum = message.getField(45)
            text = message.getField(58)
            refMsgType = message.getField(372)
            businessRejectRefID = message.getField(379)
            if (refSeqNum, text, refMsgType, businessRejectRefID) != '':
                logfix.info("(recvMsg) Business Message << {}".format(msg))
            else:
                logfix.info("(recvMsg) Business Message Error")
        elif msgType == "8":
            avgPx = message.getField(6)
            clOrdID = message.getField(11)
            CumQty = message.getField(14)
            execID = message.getField(17)
            execTransType = message.getField(20)
            orderID = message.getField(37)
            orderQty = message.getField(38)
            ordStatus = message.getField(39)
            ordType = message.getField(40)
            price = message.getField(44)
            rule80A = message.getField(47)
            side = message.getField(54)
            symbol = message.getField(55)
            timeInForce = message.getField(59)
            transactTime = message.getField(60)
            execBroker = message.getField(76)
            clientID = message.getField(109)
            MinQty = message.getField(110)
            execType = message.getField(150)
            leavesQty = message.getField(151)
            cashMargin = message.getField(544)
            primaryLastPx = float(message.getField(8031))
            primaryBidPx = float(message.getField(8032))
            primaryAskPx = float(message.getField(8033))
            routingDecisionTime = message.getField(8051)
            OrderClassification = message.getField(8060)
            crossingPriceType = message.getField(8164)
            fsxTransactTime = message.getField(8169)
            SelfTradePreventionId = message.getField(8174)
            marginTransactionType = message.getField(8214)
            if execTransType == "2":
                execRefID = message.getField(19)
                lastPx = float(message.getField(31))
                lastShares = message.getField(32)
                SecondaryOrderID = message.getField(198)
                ContraBroker = message.getField(375)
                SecondaryExecID = message.getField(527)
                lastLiquidityind = message.getField(851)
                toSTNeTOrderID = message.getField(8101)
                toSTNeTExecutionID = message.getField(8102)
                if (avgPx, clOrdID, CumQty, execID, orderID, orderQty, ordStatus, ordType, price, rule80A, side, symbol,
                    timeInForce, transactTime, execBroker, clientID, MinQty, execType, leavesQty, cashMargin,
                    primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime, OrderClassification,
                    crossingPriceType, fsxTransactTime, SelfTradePreventionId, marginTransactionType, execRefID,
                    lastPx, lastShares, SecondaryOrderID, ContraBroker, SecondaryExecID, lastLiquidityind,
                    toSTNeTOrderID, toSTNeTExecutionID) != "":
                    logfix.info("(recvMsg) EDP ToSTNeT Confirmation << {}".format(msg))
                else:
                    logfix.info(
                        "(recvMsg) EDP ToSTNeT Confirmation << {},EDP ToSTNeT Confirmation FixMsg Error!".format(msg))
            else:
                text = message.getField(58)
                if (avgPx, clOrdID, CumQty, execID, orderID, orderQty, ordStatus, ordType, price, rule80A, side, symbol,
                    timeInForce, transactTime, execBroker, clientID, MinQty, execType, leavesQty, cashMargin,
                    primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime, OrderClassification,
                    crossingPriceType, fsxTransactTime, SelfTradePreventionId, marginTransactionType, text) != "":
                    logfix.info("(recvMsg) EDP ToSTNeT Rejection << {}".format(msg))
                else:
                    logfix.info(
                        "(recvMsg) EDP ToSTNeT Rejection << {},EDP ToSTNeT Rejection FixMsg Error!".format(msg))

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
        # module_name = "InsertOrderEntryFirst"
        # module_path = sit_client_path
        # insert_order_module = SourceFileLoader(module_name, module_path).load_module()
        # insert = insert_order_module.InsertOrderEntryFirst

        return

    def order_cancel_request(self, row):
        pass

    def load_test_case(self):
        module_name = "generation"
        module_path = generation_path
        # 导入具有完整文件路径的模块
        module1 = SourceFileLoader(module_name, module_path).load_module()
        generation = module1.generation
        """Run"""
        with open("../../testcases/symbolList.json", "r") as f_json:
            case_list = json.load(f_json)
            time.sleep(2)
            for row in case_list["testCase"]:
                symbol = row["symbol"]
                price = float(row["Price"]) * 10
                orderQty = int(row["lot_size"])
                sit_client.InsertOrderEntryFirst()
        pass
