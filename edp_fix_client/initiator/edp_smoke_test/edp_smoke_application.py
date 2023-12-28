#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import configparser
import random
import sys
import quickfix as fix
import time
import logging
from datetime import datetime, timedelta
from model.logger import setup_logger
import json


class Application(fix.Application):

    def __init__(self, data, logger):
        super().__init__()
        self.sessionID = None
        self.data = data
        self.logger = logger

        # 定义变量
        self.order_id = 0
        self.exec_id = 0

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
        print(f"Session ({sessionID.toString()}) logout !")
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(self.__SOH__, "|")
        self.logger.info(f"(Core) S >> {msg}")
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
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
        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
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
                                avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType, rule80A,
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
                                avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType, rule80A,
                                side, symbol, timeInForce, transactTime, clientID, execType, leavesQty, cashMargin,
                                crossingPriceType, fsxTransactTime, marginTransactionType, origClOrdID, execBroker,
                                MinQty, OrderClassification, SelfTradePreventionId, text) != "":
                            self.logger.info(f"(recvMsg) Order Canceled << {msg}")
                            self.logger.info("Result : Order Canceled ," + "ordStatus =" + ordStatus)
                        else:
                            self.logger.info(f"(recvMsg) Order Canceled << {msg}" + 'Order Canceled FixMsg Error!')
                    # Execution Report – ToSTNeT Rejection
                    else:
                        if (
                                avgPx, clOrdID, CumQty, exec_id, execTransType, order_id, orderQty, ordType, rule80A,
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
                    lastLiquidityind = message.getField(851)
                    if execTransType == "0":
                        if (
                                avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id, orderQty,
                                ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker, clientID,
                                execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime,
                                MinQty, OrderClassification, SelfTradePreventionId, lastLiquidityind) != "":
                            self.logger.info(
                                f"(recvMsg) Order Filled << {msg}")
                            if ordStatus == '2':
                                self.logger.info("Result : EP3 Order Filled ," + "ordStatus =" + ordStatus)
                            else:
                                self.logger.info("Result : EP3 Order Partially Filled ," + "ordStatus =" + ordStatus)

                        else:
                            self.logger.info(f"(recvMsg) EP3 Order Filled << {msg}" + "Order Trade FixMsg Error!")

                    elif execTransType == '2':
                        execRefID = message.getField(19)
                        lastLiquidityInd = message.getField(851)
                        toSTNeTorder_id = message.getField(8101)
                        toSTNeTExecutionID = message.getField(8102)
                        toSTNeTTransactionTime = message.getField(8106)
                        secondaryOrderId = message.getField(198)
                        ContraBroker = message.getField(375)
                        secondaryExecId = message.getField(527)
                        if (
                                avgPx, clOrdID, CumQty, exec_id, execTransType, lastPx, lastShares, order_id,
                                orderQty, ordType, rule80A, side, symbol, timeInForce, transactTime, execBroker,
                                clientID, execType, leavesQty, cashMargin, crossingPriceType, fsxTransactTime,
                                marginTransactionType, primaryLastPx, primaryBidPx, primaryAskPx, routingDecisionTime,
                                MinQty, OrderClassification, SelfTradePreventionId, execRefID, lastLiquidityInd,
                                toSTNeTorder_id, toSTNeTTransactionTime, secondaryOrderId, ContraBroker,
                                secondaryExecId,
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
                    self.logger.info(f"(recvMsg) Order Cancel Reject << {msg}" + 'Order Cancel Reject FixMsg Error!')

            self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def gen_client_order_id(self):
        # "随机数生成ClOrdID"
        self.exec_id += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.exec_id).zfill(6)

    def insert_order_request(self, data):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(data.get('account')))
        msg.setField(fix.ClOrdID(self.gen_client_order_id()))
        msg.setField(fix.OrderQty(int(data.get("orderQty"))))
        msg.setField(fix.OrdType(data.get("ordType")))
        msg.setField(fix.Side(data.get("side")))
        msg.setField(fix.Symbol(data.get("symbol")))

        # 判断订单类型
        if data.get("price") == "2":
            msg.setField(fix.Price(data.get("Price")))

        if data.get("timeInForce") != "":
            msg.setField(fix.TimeInForce(data.get("timeInForce")))

        if data.get("rule80A") != "":
            msg.setField(fix.Rule80A(data.get("rule80A")))

        if data.get("cashMargin") != "":
            msg.setField(fix.CashMargin(data.get("cashMargin")))

        # 自定义Tag
        if data.get("crossingPriceType") != "":
            msg.setField(8164, data.get("crossingPriceType"))

        if data.get("marginTransactionType") != "":
            msg.setField(8214, data.get("marginTransactionType"))

        # EDP

        if data.get("minQty") != "":
            msg.setField(fix.MinQty(int(data.get("minQty"))))

        if data.get("orderClassification") != "":
            msg.setField(8060, data.get("orderClassification"))

        if data.get("selfTradePreventionId") != "":
            msg.setField(8174, data.get("selfTradePreventionId"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)

        return msg

    def order_cancel_request(self, row):
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

    def read_config(self, sender, target, host, port):
        # 读取并修改配置文件
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str  # 保持键的大小写

        config.read('edp_fix_client/initiator/edp_smoke_test/edp_smoke_client.cfg')
        config.set('SESSION', 'SenderCompID', sender)
        config.set('SESSION', 'TargetCompID', target)
        config.set('SESSION', 'SocketConnectHost', host)
        config.set('SESSION', 'SocketConnectPort', port)

        with open('edp_fix_client/initiator/edp_smoke_test/edp_smoke_client.cfg', 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


def main():
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--data', help='please enter send data')

        args = parser.parse_args()  # 解析参数

        if args.data:
            data = json.loads(args.data)
        else:
            data = {}
        account = data.get("account")
        sender = data.get("sender")
        target = data.get("target")
        host = data.get("ip")
        port = data.get("port")
        # report
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"edp_report_{current_date}.log"
        setup_logger('logfix', 'edp_fix_client/initiator/edp_smoke_test/logs/' + log_filename)
        logger = logging.getLogger('logfix')

        cfg = Application(data, logger)
        cfg.Sender = sender
        cfg.Target = target
        cfg.Host = host
        cfg.Port = port
        cfg.read_config(sender, target, host, port)

        settings = fix.SessionSettings("edp_fix_client/initiator/edp_smoke_test/edp_smoke_client.cfg")
        application = Application(data, logger)
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

        initiator.start()
        time.sleep(3)
        if data.get("actionType") == "NewAck":
            application.insert_order_request(data)
        elif data.get("actionType") == "CancelAck":
            application.order_cancel_request(data)
        time.sleep(10)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
