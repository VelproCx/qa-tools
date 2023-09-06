import time
import logging
import yaml
import pytest
import quickfix as fix
from pytest_demo.Application import Application
from pytest_demo.model.logger import setup_logger
from datetime import datetime

__SOH__ = chr(1)

# log
setup_logger('logfix', 'edp_report.log')
logfix = logging.getLogger('logfix')


with open('test_case.yaml', 'r') as f:
    testData = yaml.safe_load(f)


@pytest.fixture(scope='module')
def my_application():
    return Application()


@pytest.fixture(scope='class')
def get_sessionId(my_application):
    global initiator
    settings = fix.SessionSettings("test_edp_debug_client.cfg")
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.ScreenLogFactory(settings)
    initiator = fix.SocketInitiator(my_application, storeFactory, settings, logFactory)
    initiator.start()
    # 创建 FIX::SessionID 对象
    sessionID = fix.SessionID('FIX.4.2', 'RSIT_EDP_1', 'FSX_SIT_EDP')
    print('生成sessionID')
    yield sessionID
    initiator.stop()
    print('断开连接')


@pytest.mark.usefixtures('get_sessionId')
class TestBusinessFlow:

    def setup(self):
        # 在每个测试方法之前执行的设置工作
        self.OrdStatus = []
        self.OrderQty = 0
        self.CumQty = 0
        self.LeavesQty = 0
        self.Text = []
        self.PrimaryLastPx = 0
        self.PrimaryBidPx = 0
        self.PrimaryAskPx = 0

    @pytest.mark.NewAsk
    def test_case1(self, my_application, sessionID, getClOrdID):
        msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgType("D"))
        msg.setField(fix.Account(testData['Testcase'][0]['Account']))
        msg.setField(fix.ClOrdID(getClOrdID))
        msg.setField(fix.OrderQty(testData['Testcase'][0]['OrderQty']))
        msg.setField(fix.OrdType(testData['Testcase'][0]['OrdType']))
        msg.setField(fix.Side(testData['Testcase'][0]['Side']))
        msg.setField(fix.Symbol(testData['Testcase'][0]['Symbol']))
        # 获取TransactTime
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
        msg.setField(trstime)
        my_sessionID = sessionID[0]
        time.sleep(1)
        fix.Session.sendToTarget(msg, my_sessionID)
        # 等待1s，等待fromApp获取到的消息体插入到received_messages列表中
        time.sleep(1)
        # 获取收到的消息列表
        received_messages = my_application.received_messages
        # print(received_messages)
        # 断言验证消息是否存在、是否符合预期
        assert received_messages
        # 循环取数组里的消息体
        for message in received_messages:
            # 创建 quickfix.Message 对象，并使用 fromString 方法解析消息
            received_msg = fix.Message()
            # 获取到到消息体转格式
            received_msg.setString(message)
            # 将Tag（39）插入数据中
            self.OrdStatus.append(received_msg.getField(39))
            self.OrderQty = received_msg.getField(38)
            self.CumQty = received_msg.getField(14)
            self.LeavesQty = received_msg.getField(151)
            self.PrimaryLastPx = received_msg.getField(8031)
            self.PrimaryBidPx = received_msg.getField(8032)
            self.PrimaryAskPx = received_msg.getField(8032)


        assert self.OrdStatus == testData['Testcase'][0]['OrdStatus']
        assert self.LeavesQty == self.OrderQty - self.CumQty
        assert self.PrimaryLastPx != ''
        assert self.PrimaryBidPx != ''
        assert self.PrimaryAskPx != ''


    # @pytest.mark.CancelAsk
    # def test_case2(self, sessionID, my_application):
    #     clOrdId = my_application.ORDERS_DICT
    #     print(clOrdId)
    #     msg = fix.Message()
    #     header = msg.getHeader()
    #     header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
    #     header.setField(fix.MsgType("F"))
    #     msg.setField(fix.Account("RSIT_EDP_ACCOUNT_1"))
    #     msg.setField(fix.ClOrdID(getClOrdID()))
    #     msg.setField(fix.OrigClOrdID(clOrdId))
    #     msg.setField(fix.Side("1"))
    #     msg.setField(fix.Symbol("7203"))
    #     # 获取TransactTime
    #     trstime = fix.TransactTime()
    #     trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
    #     msg.setField(trstime)
    #     my_sessionID = sessionID[0]
    #     time.sleep(1)
    #     fix.Session.sendToTarget(msg, my_sessionID)
    #     # 等待1s，等待fromApp获取到的消息体插入到received_messages列表中
    #     time.sleep(1)
    #
    #     # 获取收到的消息列表
    #     received_messages = my_application.received_messages
    #     # print(received_messages)
    #     # 断言验证消息是否存在、是否符合预期
    #     assert received_messages
    #     # 循环取数组里的消息体
    #     for message in received_messages:
    #         # 创建 quickfix.Message 对象，并使用 fromString 方法解析消息
    #         received_msg = fix.Message()
    #         # 获取到到消息体转格式
    #         received_msg.setString(message)
    #         # 获取 OrderQty 标签的值并进行断言
    #         order_qty = fix.OrderQty()
    #         received_msg.getField(order_qty)
    #         assert order_qty.getValue() == 100  # 验证 OrderQty 标签的值是否符合预期
    # def test_case2(self, my_application, sessionID, getClOrdID):
    #     msg = fix.Message()
    #     header = msg.getHeader()
    #     header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    #     header.setField(fix.MsgType("D"))
    #     msg.setField(fix.Account("RSIT_EDP_ACCOUNT_1"))
    #     msg.setField(fix.ClOrdID(getClOrdID))
    #     msg.setField(fix.OrderQty(1))
    #     msg.setField(fix.OrdType("1"))
    #     msg.setField(fix.Side("1"))
    #     msg.setField(fix.Symbol("1309"))
    #     # 获取TransactTime
    #     trstime = fix.TransactTime()
    #     trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))
    #     msg.setField(trstime)
    #     my_sessionID = sessionID[0]
    #     time.sleep(1)
    #     fix.Session.sendToTarget(msg, my_sessionID)
    #     # 等待1s，等待fromApp获取到的消息体插入到received_messages列表中
    #     time.sleep(1)
    #     # 获取收到的消息列表
    #     received_messages = my_application.received_messages
    #     # print(received_messages)
    #     # 断言验证消息是否存在、是否符合预期
    #     assert received_messages
    #     # 循环取数组里的消息体
    #     for message in received_messages:
    #         # 创建 quickfix.Message 对象，并使用 fromString 方法解析消息
    #         received_msg = fix.Message()
    #         # 获取到到消息体转格式
    #         received_msg.setString(message)
    #         # 获取 Tag(39) 标签的值并进行断言
    #         received_msg.getField(39)
    #         self.status.append(received_msg.getField(39))
    #     assert self.status == ['0', '2', '2']







if __name__ == "__main__":
    pytest.main()

