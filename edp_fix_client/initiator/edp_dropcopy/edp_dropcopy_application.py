#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import difflib
import os
import random
import quickfix as fix
import time
import logging
from model.logger import setup_logger

__SOH__ = chr(1)


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
        # return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) S >> {}".format(msg))
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        logfix.info("-------------------------------------------------------------------------------------------------")
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
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
            ordStatus = message.getField(39)
            side = message.getField(54)
            symbol = message.getField(55)
            execType = message.getField(150)
            leavesQty = message.getField(151)
            contraBroker = message.getField(375)
            cashMargin = message.getField(544)
            primaryLastPx = float(message.getField(8031))
            primaryBidPx = float(message.getField(8032))
            primaryAskPx = float(message.getField(8033))
            OrderClassification = message.getField(8060)
            crossingPriceType = message.getField(8164)
            phase = message.getField(8171)
            SelfTradePreventionId = message.getField(8174)
            marginTransactionType = message.getField(8214)

            if execTransType == "2":
                execRefID = message.getField(19)
                lastPx = float(message.getField(31))
                lastShares = message.getField(32)
                timeInForce = message.getField(59)
                minQty = message.getField(110)
                fsxTransactTime = message.getField(8169)
                rule80A = message.getField(47)

                if (avgPx, clOrdID, CumQty, execID, orderID, ordStatus, rule80A, side, symbol,
                    timeInForce, execType, leavesQty, cashMargin,
                    primaryLastPx, primaryBidPx, primaryAskPx, OrderClassification,
                    crossingPriceType, fsxTransactTime, SelfTradePreventionId, marginTransactionType, execRefID,
                    lastPx, lastShares, execTransType, minQty, contraBroker, phase) != '':
                    logfix.info("(recvMsg) EDP ToSTNeT Confirmation << {}".format(msg))
                else:
                    logfix.info(
                        "(recvMsg) EDP ToSTNeT Confirmation << {},EDP ToSTNeT Confirmation FixMsg Error!".format(msg))
            else:
                text = message.getField(58)
                origClOrdID = message.getField(41)
                transactTime = message.getField(60)
                unknow8165=message.getField(8165)
                unknow8166=message.getField(8166)
                if (avgPx, clOrdID, CumQty, execID, orderID, ordStatus, transactTime, side, symbol, transactTime, execType, leavesQty, cashMargin,
                    primaryLastPx, primaryBidPx, primaryAskPx, OrderClassification,
                    crossingPriceType, SelfTradePreventionId, marginTransactionType, text,origClOrdID,unknow8165,unknow8166) != "":
                    logfix.info("(recvMsg) EDP ToSTNeT Rejection << {}".format(msg))
                else:
                    logfix.info(
                        "(recvMsg) EDP ToSTNeT Rejection << {},EDP ToSTNeT Rejection FixMsg Error!".format(msg))

            self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) R << %s" % msg)
        pass

