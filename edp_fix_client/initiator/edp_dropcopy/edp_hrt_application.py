#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import argparse
import sys
from datetime import timedelta, datetime
import quickfix as fix
import logging
from model.logger import setup_logger
import time
__SOH__ = chr(1)
global initiator
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
            clOrdID = message.getField(11)
            execID = message.getField(17)
            execTransType = message.getField(20)
            orderID = message.getField(37)
            side = message.getField(54)
            symbol = message.getField(55)

            if execTransType == "2":
                execRefID = message.getField(19)
                lastPx = float(message.getField(31))
                lastShares = message.getField(32)
                fsxTransactTime = message.getField(8169)

                if (clOrdID, orderID, execID, side, symbol,
                    fsxTransactTime, execRefID,
                    lastPx, lastShares, execTransType) != '':
                    logfix.info("(recvMsg) EDP ToSTNeT Confirmation << {}".format(msg))
                else:
                    logfix.info(
                        "(recvMsg) EDP ToSTNeT Confirmation << {},EDP ToSTNeT Confirmation FixMsg Error!".format(msg))
            else:
                ordStatus = message.getField(39)
                text = message.getField(58)
                origClOrdID = message.getField(41)
                transactTime = message.getField(60)
                execType = message.getField(150)
                if (
                        clOrdID, execID, orderID, ordStatus, transactTime, side, symbol, transactTime, execType,
                        text, origClOrdID) != "":
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


def main():
    try:
        settings = fix.SessionSettings("edp_dropcopy_client.cfg")
        application = Application()
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)
        initiator.start()
        # 执行完所有测试用例后等待时间
        sleep_duration = timedelta(minutes=60)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()