#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import difflib
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
import json
from mail.run_email import send_mail
from method.file_generation import generation
import threading
import math
__SOH__ = chr(1)
from openpyxl import Workbook,load_workbook

# report
setup_logger('logfix', 'logs/rex_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):       # 定义一个类并继承‘fix.Application’类，主要用于处理收到的消息和事件
    orderID = 0
    execID = 0
    ORDERS_DICT = []
    PTF_CANCEL_LIST = []
    LASTEST_ORDER = {}
    Success = 0
    Fail = 0
    Total = 0
    REX_PROP_BPS_BUY = 0.0022
    REX_PROP_BPS_SELL = 0.0022
    Except = []
    Result = []
    ReceveRes = []

    def __init__(self):
        # 初始化sessionID = None
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        # 服务器启动时候调用此方法创建
        # 服务器启动时，读取配置文件中的【SESSION】部份，将读取到的sessionID传给self.sessionID,并打印出来
        self.sessionID = sessionID
        print("onCreate : Session ({})".format(sessionID.toString()))
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        self.logsCheck()
        json_data = json.dumps(self.ReceveRes)
        # 将JSON数据写入文件中
        with open('logs/recv_data.json', 'w') as file:
            file.write(json_data)
        self.Result = self.compare_field_values('case/REX_Functional_Test_Matrix.json', 'logs/recv_data.json',
                                                'ordstatus')
        logfix.info("Result : Total = %d,Success = %d,Fail = %d" % (self.Total, self.Success, self.Fail))
        print("Session (%s) logout !" % sessionID.toString())
        self.writeResExcel('report/rex_report.xlsx', self.Result, 2, 'P')
        # send_mail(['report/rex_report.xlsx', 'logs/rex_report.log'])
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> %s" % msg)
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
            else:
                logfix.info("(sendMsg) New Ack >> %s" % msg + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        elif msgType == "F":
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)
            if(clOrdID, side, symbol, transactTime) != "":
                logfix.info("(sendMsg) Cancel Ack >> %s" % msg)
            else:
                logfix.info("(sendMsg) Cancel Ack >> %s" % msg + 'Order Cancel Request FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")

        # "接收业务消息时调用此方法"
        msgType = message.getHeader().getField(35)
        clOrdID = message.getField(11)
        orderID = message.getField(37)
        ordStatus = message.getField(39)
        transactTime = message.getField(60)
        fsxTransactTime = message.getField(8169)

        if ordStatus == '4':
            symbol = message.getField(55)
            print(symbol)
            if symbol == '1311':
                new_clOrdID = int(clOrdID) + 1
                print(new_clOrdID)
                clOrdID = str(new_clOrdID)

        # 模糊匹配方法，判断收到fix消息体中的clordId是否在列表中，true则更新status，false则新增一条数据
        # 设置匹配的阈值
        threshold = 1
        # 使用difflib模块的get_close_matches函数进行模糊匹配
        matches = difflib.get_close_matches(clOrdID, [item['clordId'] for item in self.ReceveRes], n=1, cutoff=threshold)
        # 如果有匹配结果
        if matches:
            matched_clordId = matches[0]
            for item in self.ReceveRes:
                if item['clordId'] == matched_clordId:
                    # 更新该组数据的ordstatus
                    item['ordstatus'] = str(ordStatus)
        else:
            # 添加新的数据到数组中
            self.ReceveRes.append({'clordId': clOrdID, 'ordstatus': str(ordStatus)})

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
            if symbol == '5076':
                self.PTF_CANCEL_LIST.append(message.getField(11))
            elif symbol == '1311' or symbol == '6954':
                self.ORDERS_DICT = message.getField(11)
            msg = message.toString().replace(__SOH__, "|")
            # 7.2 Execution Report – Order Accepted
            if ordStatus == "0":
                execBroker = message.getField(76)
                lastShares = message.getField(32)
                lastPx = message.getField(31)
                clOrdID = message.getField(11)
                if (
                        avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType,
                        rule80A,
                        side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType) != "":
                    logfix.info("(recvMsg) Order Accepted << %s" % msg + "ordStatus = " + str(ordStatus))
                    logfix.info("Result : Order Accepted ," + "ordStatus =" + ordStatus)
                else:
                    logfix.info("(recvMsg) Order Accepted << %s" % msg + 'Order Accepted FixMsg Error!')
                if execType != ordStatus:
                    logfix.info("(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
            # 7.3 Execution Report – Order Rejected
            elif ordStatus == "8":
                text = message.getField(58)
                ordRejReason = message.getField(103)
                lastShares = message.getField(32)
                lastPx = message.getField(31)
                clOrdID = message.getField(11)
                if (
                        avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType,
                        rule80A,
                        side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType,
                        fsxTransactTime, marginTransactionType, text, ordRejReason) != "":
                    logfix.info("(recvMsg) Order Rej << %s" % msg + "RejRes = " + str(text))
                else:
                    logfix.info("(recvMsg) Order Rejected << %s" % msg + 'Order Rejected FixMsg Error!')
                if execType != ordStatus:
                    logfix.info("(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
            # 7.6 Execution Report – Order Canceled
            elif ordStatus == "4":
                origClOrdID = message.getField(41)
                execBroker = message.getField(76)
                clOrdID = message.getField(11)
                if (avgPx, clOrdID, CumQty, execID, execTransType, orderID, orderQty, ordType, rule80A,
                    side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                    crossingPriceType,
                    fsxTransactTime, marginTransactionType, origClOrdID, execBroker) != "":
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
                routingDecisionTime = message.getField(8051)
                propExecPrice = message.getField(8165)
                PropExecID = message.getField(8166)
                clOrdID = message.getField(11)
                adjustLastPxBuy = math.ceil(primaryLastPx * (1 + self.REX_PROP_BPS_BUY))
                adjustLastPxSell = math.floor(primaryLastPx * (1 - self.REX_PROP_BPS_SELL))
                if (
                        avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType,
                        rule80A,
                        side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx, routingDecisionTime,
                        propExecPrice, PropExecID) != "":
                    logfix.info(
                        "(recvMsg) Order Filled << %s" % msg + 'Side: ' + str(side) + ',' + "Fill Price: " + str(
                            lastPx) + ',' + "AdjustLastPx Of Buy: " + str(
                            adjustLastPxBuy) + ',' + "AdjustLastPx Of Sell: " + str(
                            adjustLastPxSell) + ',' + "Order Type:" + str(ordType))
                    logfix.info("Result : Order Filled ," + "ordStatus =" + ordStatus)
                else:
                    logfix.info("(recvMsg) Order Filled << %s" % msg + "Order Trade FixMsg Error!")
                if execType != ordStatus:
                    logfix.info("(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
                    # Fill Price Check
                if ordType == '1':
                    if side == "1":
                        adjustLastPx = math.ceil(primaryLastPx * (1 + self.REX_PROP_BPS_BUY))
                        if adjustLastPx == lastPx:
                            return True
                        else:
                            logfix.info(
                                'Market Price is not matching,' + 'clOrdID：' + clOrdID + ',' + 'symbol：' + symbol + ',' + 'adjustLastPx：' + str(
                                    adjustLastPx) + ',' + 'lastPx:' + str(lastPx))
                    elif side == "2":
                        adjustLastPx = math.floor(primaryLastPx * (1 - self.REX_PROP_BPS_SELL))
                        if adjustLastPx == lastPx:
                            return True
                        else:
                            logfix.info(
                                'Market Price is not matching,' + 'clOrdID：' + clOrdID + ',' + 'symbol：' + symbol + ',' + 'adjustLastPx：' + str(
                                    adjustLastPx) + ',' + 'lastPx:' + str(lastPx))
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
                    logfix.info("(recvMsg) Order execType error,orderStatus = {},execType = {}".format(ordStatus, execType))
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
        # 数据比对的方法

    # 数据比对的方法
    def compare_field_values(self,json_file1, json_file2, field_name):
        resList = []
        with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        records1 = data1['testCase']
        records2 = data2
        # 判断记录数量是否相同
        if len(records1) != len(records2):
            logfix.info("两个文件记录数量不一致，比对结果不准确，请仔细核对数据，再次进行比对！")
        # 逐组比较字段值并输出结果s
        for i, (record1, record2) in enumerate(zip(records1, records2), 1):
            if record1[field_name] == record2[field_name]:
                self.Success += 1
                self.Total +=1
                resList.append('success')
            else:
                self.Fail += 1
                self.Total += 1
                logfix.info(f"第 {i} 条数据的指定字段值不相同" + "," + "clordId:" + str(record2['clordId']))
                resList.append('failed')
                logfix.info("Except:" + str(record1[field_name]) + " ，" + "ordStatus: " + str(record2[field_name]))
        return resList

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        response = ['ps:若列表存在failed数据，请查看report.log文件']
        self.writeResExcel('report/rex_report.xlsx', response, 2, 'Q')
        with open('logs/rex_report.log', 'r') as f:
            content = f.read()
        if 'Market Price is not matching' in content:
            logfix.info('Market Price is NG')
            response = ['Market Price is NG']
            self.writeResExcel('report/rex_report.xlsx', response, 5, 'Q')
        else:
            logfix.info('Market Price is OK')
            response = ['Market Price is OK']
            self.writeResExcel('report/rex_report.xlsx', response, 3, 'Q')
        if 'FixMsg Error' in content:
            logfix.info('FixMsg is NG')
            response = ['FixMsg is NG']
            self.writeResExcel('report/rex_report.xlsx', response, 6, 'Q')
        else:
            logfix.info('FixMsg is OK')
            response = ['FixMsg is OK']
            self.writeResExcel('report/rex_report.xlsx', response, 4, 'Q')
        if 'Order execType error' in content:
            logfix.info("execType is NG")
            response = ['execType is NG']
            self.writeResExcel('report/rex_report.xlsx', response, 7, "Q")
        else:
            logfix.info("execType is OK")
            response = ['execType is OK']
            self.writeResExcel('report/rex_report.xlsx', response, 8, "Q")
    def writeResExcel(self,filename,data,row,column):
        #打开现有的Excel文件或者创建新的Workbook
        workbook = load_workbook(filename)
    #     指定要写入数据的工作表
        sheet = workbook.active
        #指定要写入的列号
        start_row = row
        start_column = column
        #写入数据到指定列
        for row,value in enumerate(data,start=start_row):
            sheet[start_column + str(row)] = value

        #保持冰关闭工作簿
        workbook.save(filename)
    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        return '9002023' + str(t) + str(self.execID).zfill(8)

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

        # 判断订单类型
        if row["OrdType"] == "2":
            msg.setField(fix.Price(row["Price"]))
        elif row["OrdType"] == "1":
            print("")

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def order_cancel_request(self, row):

        if row["Id"] == '57':
            clOrdId = self.PTF_CANCEL_LIST[0]
        elif row["Id"] == '58':
            clOrdId = self.PTF_CANCEL_LIST[1]
        else:
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
        with open('case/REX_Functional_Test_Matrix.json', 'r') as f_json:
            generation('case/REX_Functional_Test_Matrix.json', 'report/rex_report.xlsx')
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            for row in case_data_list["testCase"]:
                if row["Id"] == "57":
                    time.sleep(120)
                    self.runTestCase(row)
                else:
                    time.sleep(1)
                    self.runTestCase(row)