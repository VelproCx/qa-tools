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

__SOH__ = chr(1)

# report
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"edp_report_{current_date}.log"
setup_logger('logfix', 'logs/' + log_filename)
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    orderID = 0
    execID = 0

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
        logfix.info("(Core) R << {}".format(msg))
        return

    def fromApp(self, message, sessionID):
        logfix.info("-------------------------------------------------------------------------------------------------")
        # "接收业务消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Core) recvMsg << {}".format(msg))
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def getClOrdID(self):
        # "随机数生成ClOrdID"
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        return str(t) + str1 + str(self.execID).zfill(6)


    def genPrice(self):
        return

    def insert_order_request(self, row, account):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        # msg.setField(fix.Account("RUAT_EDP_ACCOUNT_1"))
        msg.setField(fix.Account(account))
        msg.setField(fix.ClOrdID(self.getClOrdID()))
        msg.setField(fix.OrderQty(100))
        msg.setField(fix.OrdType("1"))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.Price())

        msg.setField(fix.Side("1"))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        fix.Session.sendToTarget(msg, self.sessionID)
        return msg

    def load_test_case(self, account):
        """Run"""
        with open('uat_test_with_hrt.json', 'r') as f_json:
            orderNum = 0
            case_data_list = json.load(f_json)
            time.sleep(2)
            # 循环所有用例，并把每条用例放入runTestCase方法中，
            while orderNum < 41:
                orderNum += 1
                for row in case_data_list["testCase"]:
                    self.insert_order_request(row, account)
                    time.sleep(0.05)


    def read_config(self, Sender, Target, Host, Port):
        # 读取并修改配置文件
        config = configparser.ConfigParser()
        config.read('edp_performance_client.cfg')
        config.set('SESSION', 'SenderCompID', Sender)
        config.set('SESSION', 'TargetCompID', Target)
        config.set('SESSION', 'SocketConnectHost', Host)
        config.set('SESSION', 'SocketConnectPort', Port)

        with open('edp_performance_client.cfg', 'w') as configfile:
            config.write(configfile)



def main():
    global account
    try:
        # 使用argparse的add_argument方法进行传参
        parser = argparse.ArgumentParser()  # 创建对象
        parser.add_argument('--account', default='RUAT_EDP_ACCOUNT_7', help='choose account to use for test')
        parser.add_argument('--Sender', default='RUAT_EDP_7', help='choose Sender to use for test')
        parser.add_argument('--Target', default='FSX_UAT_EDP', help='choose Target to use for test')
        parser.add_argument('--Host', default='clientgateway107', help='choose Host to use for test')
        parser.add_argument('--Port', default='5007', help='choose Port to use for test')

        args = parser.parse_args()  # 解析参数
        account = args.account
        Sender = args.Sender
        Target = args.Target
        Host = args.Host
        Port = args.Port

        cfg = Application()
        cfg.Sender = Sender
        cfg.Target = Target
        cfg.Host = Host
        cfg.Port = Port
        cfg.read_config(Sender, Target, Host, Port)

        global logfix
        # report
        setup_logger('logfix', '{}_report.log'.format(account))
        logfix = logging.getLogger('logfix')

        settings = fix.SessionSettings("edp_performance_client.cfg")
        application = Application()
        application.account = account
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.load_test_case(account)
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
