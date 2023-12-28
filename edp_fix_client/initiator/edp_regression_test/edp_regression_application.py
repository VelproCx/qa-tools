#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import difflib
import os
import random
import sys
from quickfix import FieldNotFound
import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
from openpyxl import load_workbook
from model.runEmail import send_mail

from importlib.machinery import SourceFileLoader

# 获取当前所在目录绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
# 将当前目录的路径和上级目录的绝对路径拼接
parent_path = os.path.abspath(os.path.join(current_path, "../../method"))
# 获取上级目录中一个文件的路径
generation_path = os.path.join(parent_path, "file_generation.py")
# 获取data_comparison
data_comparison_path = os.path.join(parent_path, "data_comparison.py")


class Application(fix.Application):

    def __init__(self, account, logger):
        super().__init__()
        self.sessionID = None
        self.account = account
        self.logger = logger

        # 定义变量
        self.order_id = 0
        self.exec_id = 0
        self.orders_dict = []
        self.result = []
        self.recv_result = []
        self.order_new = 0
        self.order_expired = 0
        self.order_accepted = 0
        self.order_rejected = 0
        self.order_filled = 0
        self.order_partially_filled = 0

        # 定义常量
        self.__SOH__ = chr(1)

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print(f"onCreate : Session ({sessionID.toString()})")
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print(f"Successful Logon to session '{sessionID.toString()}'.")
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        self.logsCheck()
        json_data = json.dumps(self.recv_result)
        module_name = "compare_field_values"
        module_path = data_comparison_path
        # 导入具有完整文件路径的模块
        module1 = SourceFileLoader(module_name, module_path).load_module()
        # 将JSON数据写入文件
        with open('logs/recv_data.json', 'w') as file:
            file.write(json_data)
        self.result = module1.compare_field_values('../../testcases/EDP_Functional_Test_Matrix.json',
                                                   'logs/recv_data.json',
                                                   'ordStatus')
        print(f"Session {sessionID.toString()}) logout !")

        ordStatus_list = []
        errorCode_list = []

        for i in self.recv_result:
            ordStatus_list.append(str(i['ordStatus']))
            if 'errorCode' in i:
                errorCode_list.append(str(i['errorCode']))
            else:
                errorCode_list.append(" ")

        self.write_res_excel('report/edp_report.xlsx', ordStatus_list, 2, 'J')
        self.write_res_excel('report/edp_report.xlsx', errorCode_list, 2, 'K')
        self.write_res_excel('report/edp_report.xlsx', self.result, 2, 'L')
        send_mail(['report/edp_report.xlsx', 'logs/edp_report.log'])
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        self.logger.info("-------------------------------------------------------------------------------------------------")
        msgType = message.getHeader().getField(35)
        msg = message.toString().replace(self.__SOH__, "|")
        # 7.1 New Order Single
        if msgType == "D":
            orderQty = message.getField(38)
            ordType = message.getField(40)
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)

            if (clOrdID, orderQty, ordType, side, symbol, transactTime,) != "":
                self.logger.info(f"(sendMsg) New Ack >> {msg}")
                self.order_new += 1
            else:
                self.logger.info(f"(sendMsg) New Ack >> {msg}" + 'New Order Single FixMsg Error!')
        # 7.4 Order Cancel Request
        elif msgType == "F":
            clOrdID = message.getField(11)
            side = message.getField(54)
            symbol = message.getField(55)
            transactTime = message.getField(60)
            if (clOrdID, side, symbol, transactTime) != "":
                self.logger.info(f"(sendMsg) Cancel Ack >> {msg}")
            else:
                self.logger.info(f"(sendMsg) Cancel Ack >> {msg}" + 'Order Cancel Request FixMsg Error!')
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) R << {msg}")
        return

    def fromApp(self, message, sessionID):
        self.logger.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"

        try:
            msgType = message.getHeader().getField(35)
            if msgType == 'h':
                tradingSessionID = message.getField(336)
                tradSesMode = message.getField(339)
                tradSesStatus = message.getField(340)
                msg = message.toString().replace(self.__SOH__, "|")
                if (tradingSessionID, tradSesMode, tradSesStatus) != '':
                    self.logger.info(f"(recvMsg) Trading Session << {msg}")
                else:
                    self.logger.info("(recvMsg) Trading Session Error")
            # Business Message Reject
            elif msgType == 'j':
                refSeqNum = message.getField(45)
                text = message.getField(58)
                refMsgType = message.getField(372)
                businessRejectRefID = message.getField(379)
                msg = message.toString().replace(self.__SOH__, "|")
                if (refSeqNum, text, refMsgType, businessRejectRefID) != '':
                    self.logger.info(f"(recvMsg) Business Message << {msg}")
                else:
                    self.logger.info("(recvMsg) Business Message Error")
            else:
                clOrdID = message.getField(11)
                order_id = message.getField(37)
                ordStatus = message.getField(39)
                transactTime = message.getField(60)
                fsxTransactTime = message.getField(8169)

                # 模糊匹配方法，判断收到fix消息体中的clOrdId是否在列表中，true则更新status，false则新增一条数据
                # 设置匹配的阈值
                threshold = 1
                # 使用diffLib模块的get_close_matches函数进行模糊匹配
                matches = difflib.get_close_matches(clOrdID, [item['clOrdId'] for item in self.recv_result], n=1,
                                                    cutoff=threshold)
                # 如果有匹配结果
                if matches:
                    matched_clOrdId = matches[0]
                    for item in self.recv_result:
                        if item['clOrdId'] == matched_clOrdId:
                            # 更新该组数据的ordStatus
                            item['ordStatus'].append(str(ordStatus))
                            if ordStatus == "4":
                                text = message.getField(58)
                                item['errorCode'] = text
                else:
                    # 添加新的数据到数组中
                    if ordStatus != "8":
                        self.recv_result.append({'clOrdId': clOrdID, 'ordStatus': [ordStatus], 'errorCode': ""})
                    else:
                        text = message.getField(58)
                        self.recv_result.append({'clOrdId': clOrdID, 'ordStatus': [ordStatus], 'errorCode': text})

                if msgType != '9':
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
                    # Added tag to the EDP project
                    MinQty = message.getField(110)
                    OrderClassification = message.getField(8060)
                    SelfTradePreventionId = message.getField(8174)

                    self.orders_dict = message.getField(11)

                    msg = message.toString().replace(self.__SOH__, "|")
                    # 7.2 Execution Report – Order Accepted
                    if ordStatus == "0":
                        execBroker = message.getField(76)
                        lastShares = message.getField(32)
                        lastPx = message.getField(31)
                        clOrdID = message.getField(11)
                        if (
                                avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id, orderQty,
                                ordType, rule80A,
                                side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                cashMargin,
                                crossingPriceType, fsxTransactTime, marginTransactionType, MinQty, OrderClassification,
                                SelfTradePreventionId) != "":
                            self.logger.info(f"(recvMsg) Order Accepted << {msg}" + "ordStatus = " + str(ordStatus))
                            self.logger.info("Result : Order Accepted ," + "ordStatus =" + ordStatus)
                            self.order_accepted += 1
                        else:
                            self.logger.info(f"(recvMsg) Order Accepted << {msg}" + 'Order Accepted FixMsg Error!')
                        if execType != ordStatus:
                            self.logger.info(
                                f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                    # 7.3 Execution Report – Order Rejected
                    elif ordStatus == "8":
                        text = message.getField(58)
                        ordRejReason = message.getField(103)
                        lastShares = message.getField(32)
                        lastPx = message.getField(31)
                        clOrdID = message.getField(11)
                        if (
                                avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id, orderQty,
                                ordType, rule80A,
                                side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                                crossingPriceType,
                                fsxTransactTime, marginTransactionType, text, ordRejReason, MinQty, OrderClassification,
                                SelfTradePreventionId) != "":
                            self.logger.info(f"(recvMsg) Order Rej << {msg}" + "RejRes = " + str(text))
                            self.order_rejected += 1
                        else:
                            self.logger.info(f"(recvMsg) Order Rejected << {msg}" + 'Order Rejected FixMsg Error!')
                        if execType != ordStatus:
                            self.logger.info(
                                f"(recvMsg) Order execType error,orderStatus = {ordStatus},execType = {execType}")
                    elif ordStatus == "4":
                        #  7.8 Execution Report – Order Canceled / IOC Expired / ToSTNeT Rejection
                        execBroker = message.getField(76)
                        text = message.getField(58)
                        origClOrdID = message.getField(41)
                        clOrdID = message.getField(11)
                        # Execution Report – IOC Expired
                        if 'ERROR_00010051,Order rejected due to IoC expired.' == text:
                            primaryLastPx = message.getField(8031)
                            primaryBidPx = message.getField(8032)
                            primaryAskPx = message.getField(8033)
                            print(primaryLastPx, primaryBidPx, primaryAskPx)
                            # routingDecisionTime = message.getField(8051)
                            if (
                                    avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType,
                                    rule80A,
                                    side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                    cashMargin, crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID,
                                    text) != "" and primaryLastPx != "0" or primaryBidPx != "0" or primaryAskPx != "0":
                                self.logger.info(f"(recvMsg) Order Expired << {msg}")
                                self.logger.info("Result : Order Expired ," + "ordStatus =" + ordStatus)
                            else:
                                self.logger.info(f"(recvMsg) Order Expired FixMsg Error! << {msg}")
                        # Execution Report – Order Canceled
                        elif 'ERROR_00010052,Order canceled due to client cancel request.' == text:
                            if (
                                    avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType,
                                    rule80A,
                                    side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                                    crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID, execBroker,
                                    MinQty, OrderClassification, SelfTradePreventionId, text) != "":
                                self.logger.info(f"(recvMsg) Order Canceled << {msg}")
                                self.logger.info("Result : Order Canceled ," + "ordStatus =" + ordStatus)
                            else:
                                self.logger.info(
                                    f"(recvMsg) Order Canceled << {msg}" + 'Order Canceled FixMsg Error!')
                        # Execution Report – ToSTNeT Rejection
                        else:
                            if (
                                    avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType,
                                    rule80A,
                                    side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty,
                                    cashMargin, crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID,
                                    text) != "":
                                self.logger.info(f"(recvMsg)ToSTNeT Rejection << {msg}")
                                self.logger.info("Result:ToSTNeT Rejection ," + "ordStatus =" + ordStatus)
                            else:
                                self.logger.info(
                                    f"(recvMsg)ToSTNeT Rejection << {msg}" + 'EDP ToSTNeT Rejection FixMsg Error!')
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

                        if execTransType == "0":
                            if (
                                    avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id,
                                    orderQty,
                                    ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker, clientID,
                                    execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                    marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx,
                                    routingDecisionTime,
                                    MinQty, OrderClassification, SelfTradePreventionId) != "":
                                self.logger.info(
                                    f"(recvMsg) Order Filled << {msg}")
                                if ordStatus == '2':
                                    self.logger.info("Result : EP3 Order Filled ," + "ordStatus =" + ordStatus)
                                else:
                                    self.logger.info("Result : EP3 Order Partially Filled ," + "ordStatus =" + ordStatus)
                                    self.order_partially_filled += 1

                            else:
                                self.logger.info(
                                    f"(recvMsg) EP3 Order Filled << {msg}" + "Order Trade FixMsg Error!")

                        elif execTransType == '2':
                            execRefID = message.getField(19)
                            lastLiquidityInd = message.getField(851)
                            toSTNeTorder_id = message.getField(8101)
                            toSTNeTExecutionID = message.getField(8102)
                            toSTNeTTransactionTime = message.getField(8106)
                            Secondaryorder_id = message.getField(198)
                            ContraBroker = message.getField(375)
                            Secondaryexec_id = message.getField(527)
                            self.order_filled += 1
                            if (
                                    avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id,
                                    orderQty, ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker,
                                    clientID, execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                    marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx,
                                    routingDecisionTime,
                                    MinQty, OrderClassification, SelfTradePreventionId, execRefID, lastLiquidityInd,
                                    toSTNeTorder_id, toSTNeTTransactionTime, Secondaryorder_id, ContraBroker,
                                    Secondaryexec_id,
                                    toSTNeTExecutionID) != "":
                                self.logger.info(
                                    f"(recvMsg)ToSTNeT Confirmation << {msg}")
                            else:
                                self.logger.info(
                                    f"(recvMsg)ToSTNeT Confirmation << {msg}" + 'EDP ToSTNeT Confirmation FixMsg Error!')

                else:
                    origClOrdID = message.getField(41)
                    text = message.getField(58)
                    cxlRejReason = message.getField(102)
                    cxlRejResponseTo = message.getField(434)
                    clOrdID = message.getField(11)
                    msg = message.toString().replace(self.__SOH__, "|")
                    if (clOrdID, order_id, transactTime, fsxTransactTime, origClOrdID, text,
                        cxlRejReason, cxlRejResponseTo) != "":
                        self.logger.info(f"(recvMsg) Order Cancel Reject << {msg}" + "ordStatus = " + str(ordStatus))
                    else:
                        self.logger.info(
                            f"(recvMsg) Order Cancel Reject << {msg}" + 'Order Cancel Reject FixMsg Error!')
                self.onMessage(message, sessionID)
        except FieldNotFound as e:
            self.logger.error(f"未找到字段：{e}")
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        response = ['ps: 若列表存在failed数据，请查看report.log文件']
        self.write_res_excel('report/edp_report.xlsx', response, 2, 'M')
        with open('logs/edp_report.log', 'r') as f:
            content = f.read()

        if 'FixMsg Error' in content:
            self.logger.info('FixMsg is NG')
            response = ['FixMsg is NG']
            self.write_res_excel('report/edp_report.xlsx', response, 4, 'M')
        else:
            self.logger.info('FixMsg is OK')
            response = ['FixMsg is OK']
            self.write_res_excel('report/edp_report.xlsx', response, 4, 'M')
        if 'Order execType error' in content:
            self.logger.info("execType is NG")
            response = ['execType is NG']
            self.write_res_excel('report/edp_report.xlsx', response, 5, "M")
        else:
            self.logger.info("execType is OK")
            response = ['execType is OK']
            self.write_res_excel('report/edp_report.xlsx', response, 5, "M")

    def write_res_excel(self, filename, data, row, column):
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

    def gen_client_order_id(self):
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
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(row["OrderQty"]))
        msg.setField(fix.OrdType(row["OrdType"]))
        msg.setField(fix.Side(row["Side"]))
        msg.setField(fix.Account(self.account))
        msg.setField(fix.Symbol(row["Symbol"]))
        # ClientID = msg.getField(11)

        # 判断account错误：
        if "not the target test account" in row["ScenarioName"]:
            msg.setField(fix.Account(row["Account"]))

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
        clOrdId = self.orders_dict
        time.sleep(1)
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("F"))
        msg.setField(fix.OrigClOrdID(clOrdId))
        msg.setField(fix.ClOrdID(self.get_client_order_id()))
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
        # EDP_Functional_Test_Matrix.json

        with open('../../testcases/EDP_Functional_Test_Matrix.json', 'r') as f_json:
            generation('../../testcases/EDP_Functional_Test_Matrix.json', 'report/edp_report.xlsx')
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            for row in case_data_list["testCase"]:
                if row['Id'] == "1":
                    self.insert_order_request(row)
                    time.sleep(1)

                elif row["ActionType"] == 'NewAck':
                    self.insert_order_request(row)
                    time.sleep(1)

                elif row["ActionType"] == 'CancelAck':
                    # 增加判断条件，判断是否为需要cancel的symbol
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
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('-account', default='RSIT_EDP_ACCOUNT_1', help='choose account to use for test')
        parser.add_argument('-sender', default='RSIT_EDP_1', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_SIT_EDP', help='choose Target to use for test')
        parser.add_argument('-host', default='10.4.129.151', help='choose Host to use for test')
        parser.add_argument('-port', default='30051', help='choose Port to use for test')

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

        # log
        setup_logger('logfix', 'logs/edp_report.log')
        logger = logging.getLogger('logfix')

        settings = fix.SessionSettings("edp_regression_client.cfg")
        application = Application(account, logger)
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

        initiator.start()
        application.load_test_case()
        sleep_duration = timedelta(minutes=1)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
