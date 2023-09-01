import time
import logging
from datetime import datetime
import random

global initiator
import pytest
import quickfix as fix

__SOH__ = chr(1)

from model.logger import setup_logger

# log
setup_logger('logfix', 'edp_report.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    # received_messages = []

    def __init__(self):
        super().__init__()
        self.received_messages = []
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
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        print("(Core) S >> {}".format(msg))
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        print("-------------------------------------------------------------------------------------------------")
        msg = message.toString().replace(__SOH__, "|")
        print("(Core) NewAck << {}".format(msg))
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        print("(Core) R << {}".format(msg))
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        # print("(Core) Recv << {}".format(msg))
        received_msg = str(message)
        # logfix.info(received_msg)

        self.received_messages.append(received_msg)
        # self.received_messages = received_msg
        # return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass


@pytest.fixture
def my_application():
    return Application()


def getClOrdID():
    # "随机数生成ClOrdID"
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
    return str(t) + str1


def test_send_fix_request(my_application):
    # 配置client
    settings = fix.SessionSettings("test_edp_debug_client.cfg")
    # application = Application()
    # storeFactory = fix.MemoryStoreFactory()
    # logFactory = fix.ScreenLogFactory(settings)
    # initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.ScreenLogFactory(settings)
    initiator = fix.SocketInitiator(my_application, storeFactory, settings, logFactory)

    initiator.start()

    session_id = "FIX.4.2:RSIT_EDP_1->FSX_SIT_EDP"
    session_id_parts = session_id.split(":")
    begin_string = session_id_parts[0]
    comp_id_parts = session_id_parts[1].split("->")
    sender_comp_id = comp_id_parts[0]
    target_comp_id = comp_id_parts[1]
    # 创建 FIX::SessionID 对象
    sessionID = fix.SessionID(begin_string, sender_comp_id, target_comp_id)

    time.sleep(3)
    # 配置send msg
    msg = fix.Message()
    header = msg.getHeader()
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    header.setField(fix.MsgType("D"))
    msg.setField(fix.Account("RSIT_EDP_ACCOUNT_1"))
    msg.setField(fix.ClOrdID(getClOrdID()))
    msg.setField(fix.OrderQty(100))
    msg.setField(fix.OrdType("1"))
    msg.setField(fix.Side("1"))
    msg.setField(fix.Symbol("7203"))

    # 获取TransactTime
    trstime = fix.TransactTime()
    trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
    msg.setField(trstime)

    fix.Session.sendToTarget(msg, sessionID)
    # 等待1s，等待fromApp获取到的消息体插入到received_messages列表中
    time.sleep(1)

    # 获取收到的消息列表
    received_messages = my_application.received_messages
    # my_application.fromApp(received_messages, sessionID)

    # 断言验证消息是否存在、是否符合预期
    assert received_messages
    # 循环取数组里的消息体
    for message in received_messages:
        # 创建 quickfix.Message 对象，并使用 fromString 方法解析消息
        received_msg = fix.Message()
        logfix.info(message)
        # 获取到到消息体转格式
        received_msg.setString(message)
        # 获取 OrderQty 标签的值并进行断言
        order_qty = fix.OrderQty()
        received_msg.getField(order_qty)
        assert order_qty.getValue() == 100  # 验证 OrderQty 标签的值是否符合预期
    initiator.stop()


if __name__ == "__main__":
    pytest.main()
