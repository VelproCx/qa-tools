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
setup_logger('logfix', 'edp_fullstock_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    orderID = 0
    execID = 0
    ORDERS_DICT = []
    LASTEST_ORDER = {}
    Success = 0
    Fail = 0
    Total = Success + Fail
    Result = []
    ReceveRes = []
    OrderNum = 0

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
        self.logsCheck()
        # logfix.info("Result : Total = {},Success = {},Fail = {}".format(self.Total, self.Success, self.Fail))
        print("Session (%s) logout !" % sessionID.toString())
        # send_mail(['report/edp_report.xlsx', 'logs/edp_report.log'])
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
                self.NewAck += 1
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
                            ordType, rule80A,
                            side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                            cashMargin,
                            crossingPriceType, fsxTransactTime, marginTransactionType, MinQty, OrderClassification,
                            SelfTradePreventionId) != "":
                        logfix.info("(recvMsg) Order Accepted << %s" % msg + "ordStatus = " + str(ordStatus))
                        logfix.info("Result : Order Accepted ," + "ordStatus =" + ordStatus)
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
                    else:
                        logfix.info("(recvMsg) Order Rejected << %s" % msg + 'Order Rejected FixMsg Error!')
                # 7.6 Execution Report – Order Canceled
                elif ordStatus == "4":
                    origClOrdID = message.getField(41)
                    execBroker = message.getField(76)
                    if (avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                        side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID, execBroker,
                        MinQty, OrderClassification, SelfTradePreventionId) != "":
                        logfix.info("(recvMsg) Order Canceled << %s" % msg + "ordStatus = " + str(ordStatus))
                    else:
                        logfix.info("(recvMsg) Order Canceled << %s" % msg + 'Order Canceled FixMsg Error!')
                # 7.7 Execution Report – Trade
                elif ordStatus == "1" or ordStatus == "2":
                    lastPx = float(message.getField(31))
                    lastShares = message.getField(32)
                    execBroker = message.getField(76)
                    primaryLastPx = float(message.getField(8031))
                    primaryBidPx = float(message.getField(8032))
                    primaryAskPx = float(message.getField(8033))
                    routingDecisionTime = message.getField(8051)
                    propExecPrice = message.getField(8165)
                    price = message.getField(44)
                    # Added tag to the EDP project
                    lastLiquidityind = message.getField(851)
                    if (
                            avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType, rule80A,
                            side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                            cashMargin,
                            crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx, primaryBidPx,
                            primaryAskPx,
                            routingDecisionTime, propExecPrice, MinQty, OrderClassification,
                            SelfTradePreventionId, price, lastLiquidityind) != "":
                        logfix.info(
                            "(recvMsg) Order Filled << %s" % msg)
                        if ordStatus == '2':
                            logfix.info("Result : Order Filled ," + "ordStatus =" + ordStatus)
                        else:
                            logfix.info("Result : Order Partially Filled ," + "ordStatus =" + ordStatus)
                    else:
                        logfix.info("(recvMsg) Order Filled << %s" % msg + "Order Trade FixMsg Error!")

                    # -------->toSTNeTExecutionID为非必填字段，联调时候再确认是否需要修改判断条件
                    if execTransType == '2':
                        execRefID = message.getField(19)
                        lastLiquidityInd = message.getField(851)
                        toSTNeTOrderID = message.getField(8101)
                        toSTNeTExecutionID = message.getField(8102)
                        toSTNeTTransactionTime = message.getField(8106)

                        #  Execution Report – Trade Correction (EDP ToSTNeT Accepted)
                        if toSTNeTExecutionID == 'Accepted':
                            if (
                                    avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID,
                                    orderQty, ordType, rule80A,
                                    side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                    cashMargin,
                                    crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx,
                                    primaryBidPx, primaryAskPx,
                                    routingDecisionTime, propExecPrice, MinQty, OrderClassification,
                                    SelfTradePreventionId, execRefID, lastLiquidityInd, toSTNeTOrderID,
                                    toSTNeTTransactionTime
                            ) != "":
                                logfix.info("(recvMsg) EDP ToSTNeT Accepted << %s" % msg + "ToSTNeTresult = " + str(
                                    toSTNeTExecutionID))
                            else:
                                logfix.info(
                                    "(recvMsg) EDP ToSTNeT Accepted << %s" % msg + 'EDP ToSTNeT Accepted FixMsg Error!')
                        # Execution Report – Trade Correction (EDP ToSTNeT Confirmation)
                        else:
                            if (
                                    avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID,
                                    orderQty, ordType, rule80A,
                                    side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                    cashMargin,
                                    crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx,
                                    primaryBidPx, primaryAskPx,
                                    routingDecisionTime, propExecPrice, MinQty, OrderClassification,
                                    SelfTradePreventionId, execRefID, lastLiquidityInd, toSTNeTOrderID,
                                    toSTNeTTransactionTime) != "":
                                logfix.info(
                                    "(recvMsg) EDP ToSTNeT Confirmation << %s" % msg + "ToSTNeTExecutionID = " + str(
                                        toSTNeTExecutionID))
                            else:
                                logfix.info(
                                    "(recvMsg) EDP ToSTNeT Confirmation << %s" % msg + 'EDP ToSTNeT Confirmation FixMsg Error!')
                    # Execution Report – Trade Cancel (EDP ToSTNeT Rejection)
                    elif execTransType == '1':
                        lastLiquidityInd = message.getField(851)
                        toSTNeTTransactionTime = message.getField(8106)
                        if (
                                avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty,
                                ordType,
                                rule80A, side, symbol, timeInForce, transactTime, execBroker, clientID, execType,
                                leavesQty,
                                cashMargin, crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx,
                                primaryBidPx,
                                primaryAskPx, routingDecisionTime, propExecPrice, MinQty, OrderClassification,
                                SelfTradePreventionId, lastLiquidityInd, toSTNeTTransactionTime) != "":
                            logfix.info("(recvMsg) EDP ToSTNeT Rejection << %s" % msg)
                        else:
                            logfix.info(
                                "(recvMsg) EDP ToSTNeT Rejection << %s" % msg + 'EDP ToSTNeT Rejection FixMsg Error!')
                #  7.8 Execution Report – End of Day Expired
                elif ordStatus == "C":
                    text = message.getField(58)
                    execBroker = message.getField(76)
                    origClOrdID = message.getField(41)
                    clOrdID = message.getField(11)
                    if (avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                        side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType, execBroker, origClOrdID, text) != "":
                        logfix.info("(recvMsg) Order Expired << %s" % msg + "ExpireRes = " + str(text))
                        logfix.info("Result : Order Expired ," + "ordStatus =" + ordStatus)
                    else:
                        logfix.info("(recvMsg) Order Expired << %s" % msg + "Order Expired FixMsg Error!")
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
        msg.setField(fix.Account("RSIT_ACCOUNT_1"))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(self.getOrderQty()))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.HandlInst('1'))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        if self.OrderNum % 2 == 0:
            msg.setField(fix.Side("1"))
        else:
            msg.setField(fix.Side("2"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg
        time.sleep(1)

    def runTestCase(self, row):
        self.insert_order_request(row)

    # 加载用例文件
    def load_test_case(self):
        """Run"""
        with open('../case/full_stock_List.json', 'r') as f_json:
            case_data_list = json.load(f_json)
            time.sleep(1)
            # 循环所有用例，并把每条用例放入runTestCase方法中
            while self.OrderNum < 2:
                self.OrderNum += 1
                for row in case_data_list["testCase"]:
                    self.runTestCase(row)
                    time.sleep(0.04)