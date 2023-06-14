"""FIX Application"""
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
import json
import random
import math
__SOH__ = chr(1)

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):
    """FIX Application"""
    orderID = 0
    execID = 0


    def onCreate(self, sessionID):
        """onCreate"""
        """服务器启动时候调用此方法创建"""
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        """onLogon"""
        """客户端登陆成功时候调用此方法"""
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        """onLogout"""
        """客户端断开连接时候调用此方法"""
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        """发送会话消息时候调用此方法"""
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        """发送业务消息时候调用此方法"""
        logfix.info('--------------------------------------------------------------------------------------------------------------------')
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return
    

    def onMessage(self, message, sessionID):
        """Mockup execution report for newordersingle"""
        beginString = fix.BeginString()
        msgType = fix.MsgType()
        message.getHeader().getField( beginString )
        message.getHeader().getField( msgType )

        symbol = fix.Symbol()
        side = fix.Side()
        ordType = fix.OrdType()
        orderQty = fix.OrderQty()
        price = fix.Price()
        clOrdID = fix.ClOrdID()
        # transactTime = fix.transatTime()
        message.getField( ordType )
        if ordType.getValue() != fix.OrdType_LIMIT:
            raise fix.IncorrectTagValue( ordType.getField() )

        message.getField( symbol )
        message.getField( side )
        message.getField( orderQty )
        message.getField( price )
        message.getField( clOrdID )
        # message.getField( transactTime )

        executionReport = fix.Message()
        executionReport.getHeader().setField( beginString )
        executionReport.getHeader().setField( fix.MsgType(fix.MsgType_ExecutionReport) )

        executionReport.setField( fix.OrderID(self.getOrderID()) )
        executionReport.setField( fix.ExecID(self.getExecID()) )
        executionReport.setField( fix.OrdStatus(fix.OrdStatus_FILLED) )
        executionReport.setField( symbol )
        executionReport.setField( side )
        executionReport.setField( fix.CumQty(orderQty.getValue()) )
        executionReport.setField( fix.AvgPx(price.getValue()) )
        executionReport.setField( fix.LastShares(orderQty.getValue()) )
        executionReport.setField( fix.LastPx(price.getValue()) )
        executionReport.setField( clOrdID )
        executionReport.setField( orderQty )

        if beginString.getValue() == fix.BeginString_FIX40 or beginString.getValue() == fix.BeginString_FIX41 or beginString.getValue() == fix.BeginString_FIX42:
            executionReport.setField( fix.ExecTransType(fix.ExecTransType_NEW) )

        if beginString.getValue() >= fix.BeginString_FIX41:
            executionReport.setField( fix.ExecType(fix.ExecType_FILL) )
            executionReport.setField( fix.LeavesQty(0) )

        try:
            fix.Session.sendToTarget( executionReport, sessionID )
        except fix.SessionNotFound as e:
            return

    def getClOrdID(self):
        self.execID += 1
        # 获取当前时间并且进行格式转换
        t = int(time.time())
        return '9002023' + str(t) + str(self.execID).zfill(8)

    # def getOrderQty(self):
    #     # 随机生成Qty1-5
    #     orderQty = random.randint(1, 5)
    #     return orderQty

    def getExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def insert_order_request(self,row):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType('D'))
        msg.setField(fix.Account(row['Account']))
        msg.setField(fix.ClOrdID(self.getClOrdID))
        msg.setField(fix.HandlInst('1'))
        msg.setField(fix.OrderQty(row['OrderQty']))
        msg.setField(fix.OrdType(row['OrdType']))
        msg.setField(fix.Symbol(row["Symbol"]))
        msg.setField(fix.SecurityType(row['SecurityType']))
        msg.setField(fix.ExDestination(row['ExDestination']))

        if row["TimeInForce"] != "":
            msg.setField(fix.TimeInForce(row["TimeInForce"]))

        if row["Rule80A"] != "":
            msg.setField(fix.Rule80A(row["Rule80A"]))

        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)

        if row['OrdType'] == '2':
            msg.setField(fix.Price('Price'))
        elif row['OrdType'] == '1':
            print('')

    def Test_run_case(self):
        """Run"""
        with open('acceptor_session_tst.json','r') as f_json:
            caseDatalist = json.load(f_json)
            time.sleep(1)

