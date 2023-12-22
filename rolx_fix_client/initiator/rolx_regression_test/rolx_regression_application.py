#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import difflib
import sys

import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
# from ..method1.file_generation import generation
import math
import random

__SOH__ = chr(1)

from openpyxl import load_workbook
# import sys
# sys.path.append("../method")

from importlib.machinery import SourceFileLoader
import os

# 获取当前所在目录绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
# 将当前目录的路径和上级目录的绝对路径拼接
Parent_path = os.path.abspath(os.path.join(current_path, "../../method"))
# 获取上级目录中一个文件的路径
generation_path = os.path.join(Parent_path, "file_generation.py")
# 获取data_comparison
data_comparison_path = os.path.join(Parent_path, "data_comparison.py")

# report
setup_logger('logfix', 'logs/rolx_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    exec_id = 0
    orders_dict = []
    success = 0
    fail = 0
    total = success + fail
    rol_prop_bps_buy = 0.0022
    rol_prop_bps_sell = 0.0022
    result = []
    receve_results = []
    order_new = 0
    order_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_filled = 0
    order_partially_filled = 0

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
        self.logsCheck()
        json_data = json.dumps(self.receve_results)

        module_name = "compare_field_values"
        module_path = data_comparison_path
        # 导入具有完整文件路径的模块
        module1 = SourceFileLoader(module_name, module_path).load_module()
        # 将JSON数据写入文件
        with open('logs/recv_data.json', 'w') as file:
            file.write(json_data)
        self.result = module1.compare_field_values('../../testcases/ROL_Functional_Test_Matrix.json',
                                                   'logs/recv_data.json',
                                                   'ordstatus')
        print(f"Session ({sessionID.toString()}) logout !")

        ordstatus_list = []
        errorCode_list = []
        # 循环receve_results并将value添加到列表里
        for i in self.receve_results:
            ordstatus_list.append(str(i['ordstatus']))
            if 'errorCode' in i:
                errorCode_list.append(str(i['errorCode']))

            # receve_results 没有'errorCode'字段时,添加空字符串到列表里
            else:
                errorCode_list.append(" ")

        # report文件里写入字段
        self.writeResExcel('report/rolx_report.xlsx', ordstatus_list, 2, 'J')
        self.writeResExcel('report/rolx_report.xlsx', errorCode_list, 2, 'K')
        self.writeResExcel('report/rolx_report.xlsx', self.result, 2, 'L')

        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        logfix.info("-------------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(__SOH__, "|")
        clOrdID = message.getField(11)
        side = message.getField(54)
        symbol = message.getField(55)
        transactTime = message.getField(60)

        # 7.1 New Order Single
        if msgType == "D":
            orderQty = message.getField(38)
            ordType = message.getField(40)
            if (clOrdID, orderQty, ordType,
                side, symbol, transactTime,
                ) != "":
                logfix.info(f"(sendMsg) New Ack >> {msg}")
                self.order_new += 1
            else:
                logfix.info(f"(sendMsg) New Ack >> {msg}" + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        elif msgType == "F":
            if (clOrdID, side, symbol, transactTime) != "":
                logfix.info(f"(sendMsg) Cancel Ack >> {msg}")
            else:
                logfix.info(f"(sendMsg) Cancel Ack >> {msg}" + 'Order Cancel Request FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msgType = message.getHeader().getField(35)

        # Trading Session Status
        if msgType == 'h':
            tradingSessionID = message.getField(336)
            tradSesMode = message.getField(339)
            tradSesStatus = message.getField(340)
            msg = message.toString().replace(__SOH__, "|")
            if (tradingSessionID, tradSesMode, tradSesStatus) != '':
                logfix.info(f"(recvMsg) Trading Session << {msg}")
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
                logfix.info(f"(recvMsg) Business Message << {msg}")
            else:
                logfix.info("(recvMsg) Business Message Error")
        else:
            clOrdID = message.getField(11)
            orderID = message.getField(37)
            ordStatus = message.getField(39)
            transactTime = message.getField(60)
            fsxTransactTime = message.getField(8169)

            if ordStatus == '4':
                symbol = message.getField(55)
                if symbol == '1311':
                    new_clOrdID = int(clOrdID) + 1
                    clOrdID = str(new_clOrdID)
            # 模糊匹配方法，判断收到fix消息体中的clordId是否在列表中，true则更新status，false则新增一条数据
            # 设置匹配的阈值
            threshold = 1
            # 使用difflib模块的get_close_matches函数进行模糊匹配
            matches = difflib.get_close_matches(clOrdID, [item['clordId'] for item in self.receve_results], n=1,
                                                cutoff=threshold)
            # 如果有匹配结果
            if matches:
                matched_clordId = matches[0]
                # 拿到clordId去数组里循环比对
                for item in self.receve_results:
                    # 判断当前收到的消息体clordid是否在数组里
                    if item['clordId'] == matched_clordId:
                        # 更新该组数据的ordstatus
                        item['ordstatus'].append(ordStatus)
            else:
                if ordStatus != '8':
                    # 添加新的数据到数组中
                    self.receve_results.append({'clordId': clOrdID, 'ordstatus': [ordStatus]})

                else:
                    text = message.getField(58)
                    self.receve_results.append({'clordId': clOrdID, 'ordstatus': [ordStatus], 'errorCode': text})

            # 因CancelRej消息体与其他消息体共用字段少，为减少代码量，将msgType == '9'的消息体做单独处理
            if msgType != '9':
                # 消息体共用tag
                avgPx = message.getField(6)
                CumQty = message.getField(14)
                exec_id = message.getField(17)
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
                if symbol == '5076' or symbol == '1311' or symbol == '6954':
                    self.orders_dict = message.getField(11)
                msg = message.toString().replace(__SOH__, "|")
                # 7.2 Execution Report – Order Accepted
                if ordStatus == "0":
                    execBroker = message.getField(76)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    clOrdID = message.getField(11)
                    # 判断tag是否存在
                    if (
                            avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType,
                            rule80A,
                            side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                            cashMargin,
                            crossingPriceType, fsxTransactTime, marginTransactionType) != "":
                        logfix.info(f"(recvMsg) Order Accepted << {msg}" + "ordStatus = " + str(ordStatus))
                        logfix.info("result : Order Accepted ," + "ordStatus =" + ordStatus)
                        self.order_accepted += 1
                    else:
                        logfix.info(f"(recvMsg) Order Accepted << {msg}" + 'Order Accepted FixMsg Error!')
                    if execType != ordStatus:
                        logfix.info(
                            f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                # 7.3 Execution Report – Order Rejected
                elif ordStatus == "8":
                    text = message.getField(58)
                    ordRejReason = message.getField(103)
                    lastShares = message.getField(32)
                    lastPx = message.getField(31)
                    clOrdID = message.getField(11)
                    # 判断tag是否存在
                    if (
                            avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType,
                            rule80A,
                            side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                            crossingPriceType,
                            fsxTransactTime, marginTransactionType, text, ordRejReason) != "":
                        logfix.info(f"(recvMsg) Order Rej << {msg}" + "RejRes = " + str(text))
                        self.order_rejected += 1
                    else:
                        logfix.info(f"(recvMsg) Order Rejected << {msg}" + 'Order Rejected FixMsg Error!')
                    if execType != ordStatus:
                        logfix.info(
                            f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                # 7.6 Execution Report – Order Canceled
                elif ordStatus == "4":
                    origClOrdID = message.getField(41)
                    execBroker = message.getField(76)
                    clOrdID = message.getField(11)
                    # 判断tag是否存在
                    if (avgPx, clOrdID, CumQty, exec_id, execTransType, orderID, orderQty, ordType, rule80A,
                        side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType,
                        fsxTransactTime, marginTransactionType, origClOrdID, execBroker) != "":
                        logfix.info(f"(recvMsg) Order Canceled << {msg}" + "ordStatus = " + str(ordStatus))
                    else:
                        logfix.info(f"(recvMsg) Order Canceled << {msg}" + 'Order Canceled FixMsg Error!')
                    if execType != ordStatus:
                        logfix.info(
                            f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                # 7.7 Execution Report – Trade
                elif ordStatus == "1" or ordStatus == "2":
                    lastPx = float(message.getField(31))
                    lastShares = message.getField(32)
                    execBroker = message.getField(76)
                    primaryBidPx = float(message.getField(8032))
                    primaryAskPx = float(message.getField(8033))
                    routingDecisionTime = message.getField(8051)
                    propExecPrice = message.getField(8165)
                    Propexec_id = message.getField(8166)
                    clOrdID = message.getField(11)
                    # 公式计算期望值 FillPrice
                    adjustLastPxBuy = math.ceil(primaryAskPx * (1 + self.rol_prop_bps_buy))
                    adjustLastPxSell = math.floor(primaryBidPx * (1 - self.rol_prop_bps_sell))

                    # 判断tag是否存在
                    if (
                            avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, orderID, orderQty,
                            ordType,
                            rule80A,
                            side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                            cashMargin,
                            crossingPriceType, fsxTransactTime, marginTransactionType, primaryBidPx, primaryAskPx,
                            routingDecisionTime, propExecPrice, Propexec_id) != "":
                        logfix.info(
                            "(recvMsg) Order Filled << {}".format(msg) + 'Side: ' + str(
                                side) + ',' + "Fill Price: " + str(
                                lastPx) + ',' + "AdjustLastPx Of Buy: " + str(
                                adjustLastPxBuy) + ',' + "AdjustLastPx Of Sell: " + str(
                                adjustLastPxSell) + ',' + "Order Type:" + str(ordType))
                        logfix.info("result : Order Filled ," + "ordStatus =" + ordStatus)
                        if ordStatus == "1":
                            self.order_partially_filled += 1
                        else:
                            self.order_filled += 1
                    else:
                        logfix.info(f"(recvMsg) Order Filled << {msg}" + "Order Trade FixMsg Error!")
                    if execType != ordStatus:
                        logfix.info(
                            f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                        # Fill Price Check
                    if ordType == '1':
                        if side == "1":
                            adjustLastPx = math.ceil(primaryBidPx * (1 + self.rol_prop_bps_buy))
                            # 期望值与获取的fillPrice进行比对
                            if adjustLastPx == lastPx:
                                return True
                            else:
                                logfix.info(
                                    'Market Price is not matching,' + 'clOrdID：' + clOrdID + ',' + 'symbol：' + symbol + ',' + 'adjustLastPx：' + str(
                                        adjustLastPx) + ',' + 'lastPx:' + str(lastPx))
                        elif side == "2":
                            adjustLastPx = math.floor(primaryAskPx * (1 - self.rol_prop_bps_sell))
                            # 期望值与获取的fillPrice进行比对
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
                    # 判断tag是否存在
                    if (avgPx, clOrdID, CumQty, exec_id, execTransType, orderID, orderQty, ordType, rule80A,
                        side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                        crossingPriceType, fsxTransactTime, marginTransactionType, execBroker, origClOrdID, text) != "":
                        logfix.info(f"(recvMsg) Order Expired << {msg}" + "ExpireRes = " + str(text))
                        logfix.info("result : Order Expired ," + "ordStatus =" + ordStatus)
                        self.order_expired += 1
                    else:
                        logfix.info(f"(recvMsg) Order Expired << {msg}" + "Order Expired FixMsg Error!")
                    if execType != ordStatus:
                        logfix.info(
                            f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
            else:
                origClOrdID = message.getField(41)
                text = message.getField(58)
                cxlRejReason = message.getField(102)
                cxlRejResponseTo = message.getField(434)
                clOrdID = message.getField(11)
                msg = message.toString().replace(__SOH__, "|")
                # 判断tag是否存在
                if (clOrdID, orderID, transactTime, fsxTransactTime, origClOrdID, text,
                    cxlRejReason, cxlRejResponseTo) != "":
                    logfix.info(f"(recvMsg) Order Canceled << {msg}" + "ordStatus = " + str(ordStatus))
                else:
                    logfix.info(f"(recvMsg) Order Canceled << {msg}" + 'Order Canceled FixMsg Error!')
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def logsCheck(self):
        response = ['ps: 若列表存在failed数据，请查看report.log文件']
        self.writeResExcel('report/rolx_report.xlsx', response, 2, 'M')
        with open('logs/rolx_report.log', 'r') as f:
            content = f.read()
        if 'Market Price is not matching' in content:
            logfix.info('Market Price is NG')
            response = ['Market Price is NG']
            self.writeResExcel('report/rolx_report.xlsx', response, 5, 'M')
        else:
            logfix.info('Market Price is OK')
            response = ['Market Price is OK']
            self.writeResExcel('report/rolx_report.xlsx', response, 3, 'M')

        if 'FixMsg Error' in content:
            logfix.info('FixMsg is NG')
            response = ['FixMsg is NG']
            self.writeResExcel('report/rolx_report.xlsx', response, 6, 'M')
        else:
            logfix.info('FixMsg is OK')
            response = ['FixMsg is OK']
            self.writeResExcel('report/rolx_report.xlsx', response, 4, 'M')
        if 'Order execType error' in content:
            logfix.info("execType is NG")
            response = ['execType is NG']
            self.writeResExcel('report/rolx_report.xlsx', response, 7, "M")
        else:
            logfix.info("execType is OK")
            response = ['execType is OK']
            self.writeResExcel('report/rolx_report.xlsx', response, 8, "M")

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
        self.exec_id += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.exec_id).zfill(6)

    def insert_order_request(self, row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Symbol(row["Symbol"]))
        # msg.setField(fix.HandlInst('1'))
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

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def order_cancel_request(self, row):
        # 使用变量接收上一个订单clOrdId
        clOrdId = self.orders_dict
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

    def load_test_case(self):
        module_name = "generation"
        module_path = generation_path
        # 导入具有完整文件路径的模块
        module1 = SourceFileLoader(module_name, module_path).load_module()

        generation = module1.generation

        """Run"""
        with open('../../testcases/ROL_Functional_Test_Matrix.json', 'r') as f_json:
            generation('../../testcases/ROL_Functional_Test_Matrix.json', 'report/rolx_report.xlsx')
            case_data_list = json.load(f_json)
            time.sleep(2)

            # 循环所有用例，并把每条用例放入runTestCase方法中，
            for row in case_data_list["testCase"]:
                if row['Id'] == "1":
                    self.insert_order_request(row)
                    time.sleep(60)

                elif row["ActionType"] == 'NewAck':
                    self.insert_order_request(row)
                    time.sleep(1)

                elif row["ActionType"] == 'CancelAck':
                    # 增加判断条件，判断是否为需要cancel的symbol
                    if row["Symbol"] == "5076":
                        time.sleep(3)
                    else:
                        time.sleep(1)
                    self.order_cancel_request(row)

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写
        config.read('edp_regression_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_regression_client.cfg', 'w') as configfile:
            config.write(configfile)

def main():
    global account
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('-account', default='RSIT_ROLX_2', help='choose account to use for test')
        parser.add_argument('-sender', default='RSIT_ROLX_2', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_SIT_ROLX', help='choose Target to use for test')
        parser.add_argument('-host', default='35.74.32.240', help='choose Host to use for test')
        parser.add_argument('-port', default='5002', help='choose Port to use for test')

        args = parser.parse_args()  # 解析参数
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port

        cfg = Application()
        cfg.sender = sender
        cfg.target = target
        cfg.host = host
        cfg.port = port
        cfg.read_config(sender, target, host, port)
        settings = fix.SessionSettings("rolx_regression_client.cfg")
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
