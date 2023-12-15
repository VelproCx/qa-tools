#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import threading

import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json
import random
import math
import sys

sys.path.append("../medhod/")
# from get_Symbol import get_Symbol_file

__SOH__ = chr(1)

symbols = []

# report
setup_logger('logfix', '../logs/rolx_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    Accepted = 0
    execID = 0
    Symbol_list = []
    OrderNum = 0
    ROL_PROP_BPS_BUY = 0.0022
    ROL_PROP_BPS_SELL = 0.0022
    Rejected = 0
    Book_is_closed = 0
    Filled = 0
    PartiallyFilled = 0
    NewAck = 0
    Expired = 0
    order_new = 0
    order_expired = 0
    order_accepted = 0
    order_rejected = 0
    order_filled = 0
    order_partially_filled = 0
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
        logfix.info(
            "Result : NewAck ={} Accepted = {} , Rejected= {}, Expired= {}, Filled = {}, PartiallyFilled = {}, "
            "Book_is_closed={}".format
            (self.NewAck, self.Accepted, self.Rejected, self.Expired, self.Filled, self.PartiallyFilled,
             self.Book_is_closed))

        # logfix.info("Result : Total = %d,Success = %d,Fail = %d" % (self.Total, self.Success, self.Fail))
        # self.logsCheck()
        # if self.Rejected == self.Book_is_closed:
        #     logfix.info("testcases OK")
        # else:
        #     logfix.info("testcases NG")

        print("Session (%s) logout !" % sessionID.toString())
        # send_mail('./report.log')
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
                self.order_new += 1
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
        # "接收业务消息时调用此方法"
        # 使用quickFix框架getField方法提取tag及value
        logfix.info("-------------------------------------------------------------------------------------------------")
        avgPx = message.getField(6)
        CumQty = message.getField(14)
        execID = message.getField(17)
        execTransType = message.getField(20)
        orderID = message.getField(37)
        orderQty = message.getField(38)
        ordStatus = message.getField(39)
        ordType = message.getField(40)
        rule80A = message.getField(47)
        side = message.getField(54)
        symbol = message.getField(55)
        timeInForce = message.getField(59)
        transactTime = message.getField(60)
        clientID = message.getField(109)
        execType = message.getField(150)
        leavesQty = message.getField(151)
        cashMargin = message.getField(544)
        crossingPriceType = message.getField(8164)
        fsxTransactTime = message.getField(8169)
        marginTransactionType = message.getField(8214)
        msg = message.toString().replace(__SOH__, "|")

        # 7.2 Execution Report – Order Accepted
        if ordStatus == "0":
            execBroker = message.getField(76)
            lastShares = message.getField(32)
            lastPx = message.getField(31)
            clOrdID = message.getField(11)
            if (avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType, rule80A,
                side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                crossingPriceType, fsxTransactTime, marginTransactionType) != "":
                logfix.info("(recvMsg) Order Accepted << %s" % msg + "ordStatus = " + str(ordStatus))
                self.order_accepted += 1
                self.Accepted += 1
            else:
                logfix.info("(recvMsg) Order Accepted << %s" % msg + 'Order Accepted FixMsg Error!')
        # 7.3 Execution Report – Order Rejected
        elif ordStatus == "8":
            text = message.getField(58)
            ordRejReason = message.getField(103)
            lastShares = message.getField(32)
            lastPx = message.getField(31)
            clOrdID = message.getField(11)

            if (avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType, rule80A,
                side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin, crossingPriceType,
                fsxTransactTime, marginTransactionType, text, ordRejReason) != "":
                logfix.info("(recvMsg) Order Rej << %s" % msg + "RejRes = " + str(text))
                self.order_rejected += 1
                self.Rejected += 1
                if text == "Book is CLOSED":
                    self.Book_is_closed += 1

            else:
                logfix.info("(recvMsg) Order Rej << %s" % msg + 'Order Rejected FixMsg Error!')
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
            PropExecID = message.getField(8166)
            clOrdID = message.getField(11)
            adjustLastPxBuy = math.ceil(primaryAskPx * (1 + self.ROL_PROP_BPS_BUY))
            adjustLastPxSell = math.floor(primaryBidPx * (1 - self.ROL_PROP_BPS_SELL))
            # Trade Tags is null check
            if (avgPx, clOrdID, CumQty, execID, execTransType, lastPx, lastShares, orderID, orderQty, ordType, rule80A,
                side, symbol, timeInForce, transactTime, execBroker, clientID, execType, leavesQty, cashMargin,
                crossingPriceType, fsxTransactTime, marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx,
                routingDecisionTime, propExecPrice, PropExecID) != "":
                logfix.info("(recvMsg) Order Filled << %s" % msg + 'Side: ' + str(side) + ',' + "Fill Price: " + str(
                    lastPx) + ',' + "AdjustLastPx Of Buy: " + str(
                    adjustLastPxBuy) + ',' + "AdjustLastPx Of Sell: " + str(adjustLastPxSell))
                if ordStatus == "1":
                    self.order_partially_filled += 1
                else:
                    self.order_filled += 1
            else:
                logfix.info("(recvMsg) Order Filled << %s" % msg + "Trade FixMsg Error!")
            # Fill Price Check
            if side == "1":
                adjustLastPx = math.ceil(primaryAskPx * (1 + self.ROL_PROP_BPS_BUY))
                if adjustLastPx == lastPx:
                    self.PartiallyFilled += 1
                    return True
                else:
                    logfix.info(
                        'Market Price is not matching,' + 'clOrdID：' + clOrdID + ',' + 'symbol：' + symbol + ','
                        + 'adjustLastPx：' + str(adjustLastPx) + ',' + 'lastPx:' + str(lastPx))
            elif side == "2":
                adjustLastPx = math.floor(primaryBidPx * (1 - self.ROL_PROP_BPS_SELL))
                if adjustLastPx == lastPx:
                    self.Filled += 1
                    return True
                else:
                    logfix.info(
                        'Market Price is not matching,' + 'clOrdID：' + clOrdID + ',' + 'symbol：' + symbol + ','
                        + 'adjustLastPx：' + str(adjustLastPx) + ',' + 'lastPx:' + str(lastPx))
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
                self.order_expired += 1
                self.Expired += 1
            else:
                logfix.info("(recvMsg) Order Expired << %s" % msg + "Order Expired FixMsg Error!")

        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    # 判断log文件中是否存在 Market Price is not matching
    def logsCheck(self):
        with open('rolx_report.log', 'r') as f:
            content = f.read()
        if 'Market Price is not matching' in content:
            logfix.info('Market Price is NG')
        else:
            logfix.info('Market Price is OK')

    # "随机数生成ClOrdID"
    def getClOrdID(self):
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 6)])
        return '2023' + str1 + str(t) + str(self.execID).zfill(8)

    # Order Qty 随机生成
    def getOrderQty(self):
        # 随机生成Qty1-5
        orderQty = random.randint(1, 5)
        return orderQty

    # New Ack Req
    def insert_order_request(self, symbol):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        # msg.setField(fix.Account("RSIT_ACCOUNT_1"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(self.getOrderQty()))
        # msg.setField(fix.OrderQty(row['OrderQty']))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(symbol))
        ClientID = msg.getField(11)
        msg.setField(fix.ClientID(ClientID))
        if self.OrderNum % 2 == 1:
            msg.setField(fix.Side("1"))
        else:
            msg.setField(fix.Side("2"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    # 加载用例文件
    def load_test_case(self):
        """Run"""
        start_time = datetime.now()
        tor = int(time_of_running)

        while True:
            # 获取当前时间
            current_time = datetime.now()
            # 定义时间区间
            time_difference = current_time - start_time
            # 循环股票列表
            for symbol in symbols:
                # 判断时间区间是否小于等于传进来的运行时间参数
                if time_difference <= timedelta(minutes=tor):
                    # 重新计算
                    current_time = datetime.now()
                    time_difference = current_time - start_time
                    if time_difference <= timedelta(minutes=tor):
                        self.insert_order_request(symbol)
                        time.sleep(1)
                else:
                    break

            if time_difference > timedelta(minutes=tor):
                return

    # def gen_thread(self):
    #     threads = []
    #     for _ in range(5):
    #         t = threading.Thread(target=self.load_test_case())
    #         threads.append(t)
    #     for t in threads:
    #         t.start()

    def read_config(self, sender, target, host, port):
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read("rolx_full_stock_client.cfg")
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('rolx_full_stock_client.cfg', 'w') as configfile:
            config.write(configfile)


def main():
    global account
    global time_of_running

    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('-account', default='RUAT_ROLX_2', help='choose account to use for test')
        parser.add_argument('-sender', default='RUAT_ROLX_2', help='choose Sender to use for test')
        parser.add_argument('-target', default='FSX_UAT_ROLX', help='choose Target to use for test')
        parser.add_argument('-host', default='clientgateway102', help='choose Host to use for test')
        parser.add_argument('-port', default='5001', help='choose Port to use for test')
        parser.add_argument('-tor', default=30, help='time_of_running')

        args = parser.parse_args()
        account = args.account
        sender = args.sender
        target = args.target
        host = args.host
        port = args.port
        time_of_running = args.tor

        cfg = Application()
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        with open("../../../testcases/full_stock_List.json", "r") as f_json:
            case_data_list = json.load(f_json)
            for row in case_data_list:
                symbol = row[0]
                symbols.append(symbol)

        settings = fix.SessionSettings("rolx_full_stock_client.cfg")
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
