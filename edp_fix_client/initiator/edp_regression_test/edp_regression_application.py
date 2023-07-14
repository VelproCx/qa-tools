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
from method.file_generation import generation
from openpyxl import load_workbook
__SOH__ = chr(1)

# log
setup_logger('logfix', 'logs/edp_report.log')
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
        json_data = json.dumps(self.ReceveRes)
        # 将JSON数据写入文件
        with open('logs/recv_data.json', 'w') as file:
            file.write(json_data)
        self.Result = self.compare_field_values('case/EDP_Functional_Test_Matrix.json', 'logs/recv_data.json',
                                                'ordstatus')
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
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msgType = message.getHeader().getField(35)
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

            # 模糊匹配方法，判断收到fix消息体中的clordId是否在列表中，true则更新status，false则新增一条数据
            # 设置匹配的阈值
            threshold = 1
            # 使用difflib模块的get_close_matches函数进行模糊匹配
            matches = difflib.get_close_matches(clOrdID, [item['clordId'] for item in self.ReceveRes], n=1,
                                                cutoff=threshold)
            # 如果有匹配结果
            if matches:
                matched_clordId = matches[0]
                for item in self.ReceveRes:
                    if item['clordId'] == matched_clordId:
                        # 更新该组数据的ordstatus
                        item['ordstatus'].append(str(ordStatus))
            else:
                # 添加新的数据到数组中
                self.ReceveRes.append({'clordId': clOrdID, 'ordstatus': ([ordStatus])})
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
                SecondaryOrderID = message.getField(198)
                ContraBroker = message.getField(375)
                SecondaryExecID = message.getField(527)

                if symbol == '1320' or symbol == '1321' or symbol == '1308':
                    self.ORDERS_DICT = message.getField(11)
                msg = message.toString().replace(__SOH__, "|")
                # 7.2 Execution Report – Order Accepted
                if ordStatus == "0":
                    execBroker = message.getField(76)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    clOrdID = message.getField(11)
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
                    if execType != ordStatus:
                        logfix.info(
                            "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
                # 7.3 Execution Report – Order Rejected
                elif ordStatus == "8":
                    text = message.getField(58)
                    ordRejReason = message.getField(103)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    clOrdID = message.getField(11)
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
                    if execType != ordStatus:
                        logfix.info(
                            "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
                # 7.6 Execution Report – Order Canceled
                elif ordStatus == "4":
                    origClOrdID = message.getField(41)
                    execBroker = message.getField(76)
                    clOrdID = message.getField(11)
                    if (avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                        side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID, execBroker,
                        MinQty, OrderClassification, SelfTradePreventionId) != "":
                        logfix.info("(recvMsg) Order Canceled << %s" % msg + "ordStatus = " + str(ordStatus))
                    else:
                        logfix.info("(recvMsg) Order Canceled << %s" % msg + 'Order Canceled FixMsg Error!')
                    if execType != ordStatus:
                        logfix.info(
                            "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
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
                    clOrdID = message.getField(11)
                    # price = message.getField(44)
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
                            SelfTradePreventionId) != "":
                        logfix.info(
                            "(recvMsg) Order Filled << %s" % msg)
                        if ordStatus == '2':
                            logfix.info("Result : Order Filled ," + "ordStatus =" + ordStatus)
                        else:
                            logfix.info("Result : Order Partially Filled ," + "ordStatus =" + ordStatus)
                    else:
                        logfix.info("(recvMsg) Order Filled << %s" % msg + "Order Trade FixMsg Error!")
                    if execType != ordStatus:
                        logfix.info(
                            "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
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
                        # 7.2 Execution Report – Trade Correction (EDP ToSTNeT Confirmation)
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
                    # 7.1 Execution Report – Trade Cancel (EDP ToSTNeT Rejection)
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
                    if execType != ordStatus:
                        logfix.info(
                            "(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
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

    # 结果数据比对方法
    def compare_field_values(self, json_file1, json_file2, field_name):
        resList = []
        with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        records1 = data1['testCase']
        records2 = data2
        # 判断记录数量是否相同
        if len(records1) != len(records2):
            logfix.info("两个文件记录数量不一致，比对结果不准确，请仔细核对数据，再次进行比对！")
        # 逐组比较字段值并输出结果
        for i, (record1, record2) in enumerate(zip(records1, records2), 1):
            if record1[field_name] == record2[field_name]:
                self.Success += 1
                resList.append('success')
            else:
                self.Fail += 1
                logfix.info(f"第 {i} 条数据的指定字段值不相同" + "," + "clordId:" + str(record2['clordId']))
                resList.append('failed')
                logfix.info("Except:" + str(record1[field_name]) + " ，" + "ordStatus: " + str(record2[field_name]))
        return resList

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        response = ['ps: 若列表存在failed数据，请查看report.log文件']
        self.writeResExcel('report/edp_report.xlsx', response, 2, 'T')
        with open('logs/edp_report.log', 'r') as f:
            content = f.read()

        if 'FixMsg Error' in content:
            logfix.info('FixMsg is NG')
            response = ['FixMsg is NG']
            self.writeResExcel('report/edp_report.xlsx', response, 4, 'T')
        else:
            logfix.info('FixMsg is OK')
            response = ['FixMsg is OK']
            self.writeResExcel('report/edp_report.xlsx', response, 4, 'T')
        if 'Order execType error' in content:
            logfix.info("execType is NG")
            response = ['execType is NG']
            self.writeResExcel('report/edp_report.xlsx', response, 5, "T")
        else:
            logfix.info("execType is OK")
            response = ['execType is OK']
            self.writeResExcel('report/edp_report.xlsx', response, 5, "T")

    def writeResExcel(self, filename, data, row, column):
        # 打开现有的 Excel 文件或创建新的 Workbook
        workbook = load_workbook(filename)
        # 选择要写入数据的工作表
        sheet = workbook.active
        # 指定要写入的列号
        start_row = row
        start_column = column

        # 写入数据到指定列
        for row, value in enumerate(data, start=start_row):
            sheet[start_column + str(row)] = value

        # 保存修改并关闭工作簿
        workbook.save(filename)

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
        msg.setField(fix.Account(row["Account"]))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.HandlInst('1'))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))

        # 判断订单类型
        if row["OrdType"] == "2":
            msg.setField(fix.Price(row["Price"]))

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

        # EDP

        if row["MinQty"] != "":
            msg.setField(fix.MinQty(row["MinQty"]))

        if row["OrderClassification"] != "":
            msg.setField(8060, row["OrderClassification"])

        if row["SelfTradePreventionId"] != "":
            msg.setField(8174, row["SelfTradePreventionId"])

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)

        return msg

    def order_cancel_request(self, row):
        # 使用变量接收上一个订单clOrdId
        # self.insert_order_request(row)
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

    def runTestCase(self, row):

        action = row["ActionType"]
        if action == 'NewAck':
            self.insert_order_request(row)
        elif action == 'CancelAck':
            self.order_cancel_request(row)

    def load_test_case(self):
        """Run"""
        with open('case/EDP_Functional_Test_Matrix.json', 'r') as f_json:
            generation('case/EDP_Functional_Test_Matrix.json', 'report/edp_report.xlsx')
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            for row in case_data_list["testCase"]:
                self.runTestCase(row)
                time.sleep(1)
