#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import difflib
import random
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
import json

__SOH__ = chr(1)

# report
setup_logger('logfix', 'logs/edp_fullstock_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    execID = 0
    symbol_list = []
    Success = 0
    Fail = 0
    Total = Success + Fail
    Result = []
    order_new = 0
    order_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_TosTNeT_rejected = 0
    order_filled = 0
    order_partially_filled = 0
    order_comfirmation = 0

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
        logfix.info(
            "Result: order_new = {}, order_accepted = {}, order_filled = {}, order_partially_filled = {}, order_expired = {}, order_rejected = {}, order_TosTNeT_rejected = {}, order_comfirmation = {}".format(
                self.order_new, self.order_accepted, self.order_filled, self.order_partially_filled, self.order_expired,
                self.order_rejected, self.order_TosTNeT_rejected, self.order_comfirmation))
        print("Session ({}) logout !".format(sessionID.toString()))
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
            if (clOrdID, orderQty, ordType,
                side, symbol, transactTime,
                ) != "":
                logfix.info("(sendMsg) New Ack >> %s" % msg)
                self.order_new += 1
            else:
                logfix.info("(sendMsg) New Ack >> %s" % msg + 'New Order Single FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msgType = message.getHeader().getField(35)

        # trading session
        if msgType == 'h':
            tradingSessionID = message.getField(336)
            tradSesMode = message.getField(339)
            tradSesStatus = message.getField(340)
            msg = message.toString().replace(__SOH__, "|")
            if (tradingSessionID, tradSesMode, tradSesStatus) != '':
                logfix.info("(recvMsg) Trading Session << {}".format(msg))
            else:
                logfix.info("(recvMsg) Trading Session Error")
        # Business Message Reject
        elif msgType == 'j':
            refSeqNum = message.getField(45)
            text = message.getField(58)
            refMsgType = message.getField(372)
            businessRejectRefID = message.getField(379)
            msg = message.toString().replace(__SOH__, "|")
            if (refSeqNum, text, refMsgType, businessRejectRefID) != '':
                logfix.info("(recvMsg) Business Message << {}".format(msg))
            else:
                logfix.info("(recvMsg) Business Message Error")
        else:
            clOrdID = message.getField(11)
            orderID = message.getField(37)
            ordStatus = message.getField(39)
            transactTime = message.getField(60)
            fsxTransactTime = message.getField(8169)

            if msgType != '9':
                avgPx = message.getField(6)
                CumQty = message.getField(14)
                execID = message.getField(17)
                execTransType = message.getField(20)
                orderQty = message.getField(38)
                ordType = message.getField(40)
                rule80A = message.getField(47)
                side = message.getField(54)
                symbol = message.getField(55)
                timeInForce = message.getField(59)
                clientID = message.getField(109)
                execType = message.getField(150)
                leavesQty = message.getField(151)
                cashMargin = message.getField(544)
                crossingPriceType = message.getField(8164)
                marginTransactionType = message.getField(8214)

                # Added tag to the EDP project
                MinQty = message.getField(110)
                OrderClassification = message.getField(8060)
                SelfTradePreventionId = message.getField(8174)

                if execType != ordStatus:
                    logfix.info(
                        "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))

                msg = message.toString().replace(__SOH__, "|")
                # 7.2 Execution Report – Order Accepted
                if ordStatus == "0":
                    execBroker = message.getField(76)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    if (
                            avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker, clientID, execType,
                            leavesQty, cashMargin,
                            crossingPriceType, fsxTransactTime, marginTransactionType, MinQty, OrderClassification,
                            SelfTradePreventionId) != "":
                        logfix.info("(recvMsg) Order Accepted << %s" % msg + "ordStatus = " + str(ordStatus))
                        logfix.info("Result : Order Accepted ," + "ordStatus =" + ordStatus)
                        self.order_accepted += 1
                    else:
                        logfix.info("(recvMsg) Order Accepted << %s" % msg + 'Order Accepted FixMsg Error!')
                # 7.3 Execution Report – Order Rejected
                elif ordStatus == "8":
                    text = message.getField(58)
                    ordRejReason = message.getField(103)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    if (
                            avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType, rule80A,
                            side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                            crossingPriceType,
                            fsxTransactTime, marginTransactionType, text, ordRejReason, MinQty, OrderClassification,
                            SelfTradePreventionId) != "":
                        logfix.info("(recvMsg) Order Rej << %s" % msg + "RejRes = " + str(text))
                        self.order_rejected += 1
                    else:
                        logfix.info("(recvMsg) Order Rejected << %s" % msg + 'Order Rejected FixMsg Error!')
                #  7.8 Execution Report – Order Canceled / IOC Expired / ToSTNeT Rejection
                elif ordStatus == "4":
                    text = message.getField(58)
                    origClOrdID = message.getField(41)
                    execBroker = message.getField(76)
                    # Execution Report – IOC Expired
                    if 'ERROR_20010051,Order rejected due to IoC expired.' == text:
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                                side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                cashMargin, crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID,
                                text) != "":
                            self.order_expired += 1
                            logfix.info("(recvMsg) Order Expired << {}".format(msg))
                            logfix.info("Result : Order Expired ," + "ordStatus =" + ordStatus)
                        else:
                            logfix.info("(recvMsg) Order Expired << {}".format(msg) + "Order Expired FixMsg Error!")
                    # Execution Report – Order Canceled
                    elif 'ERROR_20010052,Order canceled due to client cancel request.' == text:
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                                side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                                crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID, execBroker,
                                MinQty, OrderClassification, SelfTradePreventionId, text) != "":
                            logfix.info("(recvMsg) Order Canceled << {}".format(msg))
                            logfix.info("Result : Order Canceled ," + "ordStatus =" + ordStatus)
                        else:
                            logfix.info("(recvMsg) Order Canceled << {}".format(msg) + 'Order Canceled FixMsg Error!')
                    # Execution Report – ToSTNeT Rejection
                    else:
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                                side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                cashMargin, crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID,
                                text) != "":
                            self.order_TosTNeT_rejected += 1
                            logfix.info("(recvMsg)ToSTNeT Rejection << {}".format(msg))
                            logfix.info("Result:ToSTNeT Rejection ," + "ordStatus =" + ordStatus)
                        else:
                            logfix.info(
                                "(recvMsg)ToSTNeT Rejection << {}".format(msg) + 'EDP ToSTNeT Rejection FixMsg Error!')
                # 7.7 Execution Report – Trade
                elif ordStatus == "1" or ordStatus == "2":
                    lastPx = float(message.getField(31))
                    lastShares = message.getField(32)
                    execBroker = message.getField(76)
                    primaryLastPx = float(message.getField(8031))
                    primaryBidPx = float(message.getField(8032))
                    primaryAskPx = float(message.getField(8033))
                    routingDecisionTime = message.getField(8051)
                    # price = message.getField(44)
                    # Added tag to the EDP project
                    lastLiquidityind = message.getField(851)
                    if execTransType == "0":
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty,
                                ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker, clientID,
                                execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime,
                                MinQty, OrderClassification, SelfTradePreventionId, lastLiquidityind) != "":
                            logfix.info(
                                "(recvMsg) Order Filled << {}".format(msg))
                            if ordStatus == '2':
                                logfix.info("Result : EP3 Order Filled ," + "ordStatus =" + ordStatus)
                                self.order_filled += 1
                            else:
                                logfix.info("Result : EP3 Order Partially Filled ," + "ordStatus =" + ordStatus)
                                self.order_partially_filled += 1

                        else:
                            logfix.info("(recvMsg) EP3 Order Filled << {}".format(msg) + "Order Trade FixMsg Error!")

                    elif execTransType == '2':
                        execRefID = message.getField(19)
                        lastLiquidityInd = message.getField(851)
                        toSTNeTOrderID = message.getField(8101)
                        toSTNeTExecutionID = message.getField(8102)
                        toSTNeTTransactionTime = message.getField(8106)
                        SecondaryOrderID = message.getField(198)
                        ContraBroker = message.getField(375)
                        SecondaryExecID = message.getField(527)
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID,
                                orderQty, ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker,
                                clientID, execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime,
                                MinQty, OrderClassification, SelfTradePreventionId, execRefID, lastLiquidityInd,
                                toSTNeTOrderID, toSTNeTTransactionTime, SecondaryOrderID, ContraBroker, SecondaryExecID,
                                toSTNeTExecutionID) != "":
                            logfix.info(
                                "(recvMsg)ToSTNeT Confirmation << {}".format(msg))
                            self.order_comfirmation += 1
                        else:
                            logfix.info(
                                "(recvMsg)ToSTNeT Confirmation << {}".format(
                                    msg) + 'EDP ToSTNeT Confirmation FixMsg Error!')

            else:
                origClOrdID = message.getField(41)
                text = message.getField(58)
                cxlRejReason = message.getField(102)
                cxlRejResponseTo = message.getField(434)
                clOrdID = message.getField(11)
                msg = message.toString().replace(__SOH__, "|")
                if (clOrdID, orderID, transactTime, fsxTransactTime, origClOrdID, text,
                    cxlRejReason, cxlRejResponseTo) != "":
                    logfix.info("(recvMsg) Order Canceled << %s" % msg + "ordStatus = " + str(ordStatus))
                else:
                    logfix.info("(recvMsg) Order Canceled << %s" % msg + 'Order Canceled FixMsg Error!')

            self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        response = ['ps: 若列表存在failed数据，请查看report.log文件']
        self.writeResExcel('report/edp_report.xlsx', response, 2, 'T')
        with open('logs/edp_report.log', 'r') as f:
            content = f.read()
        if 'FixMsg Error' in content:
            logfix.info('FixMsg is NG')
        else:
            logfix.info('FixMsg is OK')
        if 'Order execType error' in content:
            logfix.info("execType is NG")
        else:
            logfix.info("execType is OK")

    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.execID).zfill(6)

    # Order Qty 随机生成
    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    def insert_order_request(self, row):
        global orderNum
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account("RUAT_EDP_ACCOUNT_4"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(int(row["OrderQty"])))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        if row["Symbol"] <= '5000':
            msg.setField(fix.Side("1"))
        elif row["Symbol"] >= '5001' and row["Symbol"] <= '7000':
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

    # 加载用例文件
    def load_test_case(self):
        """Run"""
        with open('../../../testcases/full_stock_List.json', 'r') as j_son:
            symbol_list = json.load(j_son)
            time.sleep(3)
            for row in symbol_list["testCase"]:
                if row['Symbol'] < '7000':
                    self.runTestCase(row)
                    time.sleep(0.004)
                else:
                    pass
