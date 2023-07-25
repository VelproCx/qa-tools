#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
from ctypes import *
# import ctypes
import os, time

# test_env = {'version': "test_2"}
kafka_port = '192.168.0.72:9092'

if "KAFKA_FSX" in os.environ:
    kafka_port = os.environ["KAFKA_FSX"]

print("KAFKA order parse server start, user kafka port : " + kafka_port)


class Header_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char)
    ]


class Time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('tv_sec', c_longlong),
        ('tv_usec', c_longlong)
    ]


class BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('LastTime', Time_t),
        ('LastPrice', c_double),
        ('LastQty', c_double),
        ('BidTime', Time_t),
        ('BidPrice', c_double),
        ('BidQty', c_double),
        ('AskTime', Time_t),
        ('AskPrice', c_double),
        ('AskQty', c_double),
        ('OpenPrice', c_double)
    ]


class NewOrder_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('ClOrdID', c_char * 32),
        ('OrderQty', c_double),
        ('OrdType', c_char),
        ('Price', c_double),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('CashMargin', c_char),
        ('CrossingPriceType', c_char * 20),
        ('Account', c_char * 32),
        ('MarginTransactionType', c_char),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('OrdStatus', c_char),
        ('FsxTransactTime', c_char * 28)
    ]


class NewOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('NewOrder', NewOrder_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class OrderAccepted_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecTransType', c_char),
        ('LastPx', c_double),
        ('LastShares', c_double),
        ('OrderID', c_char * 32),
        ('OrderQty', c_double),
        ('OrdStatus', c_char),
        ('OrdType', c_char),
        ('Price', c_double),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('ExecBroker', c_char * 20),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('CrossingPriceType', c_char * 20),
        ('Account', c_char * 32),
        ('MarginTransactionType', c_char),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class OrderAccepted_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderAccepted', OrderAccepted_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class OrderRejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecTransType', c_char),
        ('LastPx', c_double),
        ('LastShares', c_double),
        ('OrderID', c_char * 32),
        ('OrderQty', c_double),
        ('OrdStatus', c_char),
        ('OrdType', c_char),
        ('Price', c_double),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('Text', c_char * 150),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('OrdRejReason', c_int),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('CrossingPriceType', c_char * 20),
        ('Account', c_char * 32),
        ('MarginTransactionType', c_char),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class OrderRejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderRejected', OrderRejected_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class CancelOrder_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('ClOrdID', c_char * 32),
        ('OrigClOrdID', c_char * 32),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TransactTime', c_char * 28),
        ('OrderID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('OrdStatus', c_char),
        ('FsxTransactTime', c_char * 28),

        ('Account', c_char * 32),
        ('Price', c_double),
        ('TimeInForce', c_char),
        ('OrderQty', c_double),
        ('LeavesQty', c_double)
    ]


class CancelOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('CancelOrder', CancelOrder_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class Trade_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecTransType', c_char),
        ('LastPx', c_double),
        ('LastShares', c_double),
        ('OrderID', c_char * 32),
        ('OrderQty', c_double),
        ('OrdStatus', c_char),
        ('OrdType', c_char),
        ('Price', c_double),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('ExecBroker', c_char * 20),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('LastLiquidityInd', c_int),
        ('TrdMatchID', c_char * 20),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('CrossingPriceType', c_char * 20),
        ('PropExecPrice', c_double),
        ('PropExecID', c_char * 32),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('Account', c_char * 32),
        ('ParentFsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28),
        ('RoutingDecisionTime', c_char * 28),
        ('MarginTransactionType', c_char)
    ]


class Trade_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Trade', Trade_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class OrderCancelAccepted_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecTransType', c_char),
        ('OrderQty', c_double),
        ('OrdStatus', c_char),
        ('OrdType', c_char),
        ('OrigClOrdID', c_char * 32),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('ExecBroker', c_char * 20),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('CrossingPriceType', c_char * 20),
        ('MarginTransactionType', c_char),
        ('Price', c_double),
        ('Account', c_char * 32),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28),
        ('OrderID', c_char * 32)
    ]


class OrderCancelAccepted_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderCancelAccepted', OrderCancelAccepted_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class OrderCancelRejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('ClOrdID', c_char * 32),
        ('OrderID', c_char * 32),
        ('OrigClOrdID', c_char * 32),
        ('Text', c_char * 150),
        ('TransactTime', c_char * 28),
        ('OrdStatus', c_char),
        ('CxlRejReason', c_char),
        ('CxlRejResponseTo', c_char),
        ('OrdType', c_char),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28),

        ('Price', c_double),
        ('Account', c_char * 32),
        ('TimeInForce', c_char),
        ('OrderQty', c_double),
        ('LeavesQty', c_double)
    ]


class OrderCancelRejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderCancelRejected', OrderCancelRejected_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class AmendOrder_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('ClOrdID', c_char * 32),
        ('OrigClOrdID', c_char * 32),
        ('HandlInst', c_char),
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrdType', c_char),
        ('Price', c_double),
        ('OrderQty', c_double),
        ('TransactTime', c_char * 28),
        ('OrderID', c_char * 20),
        ('ExecBroker', c_char * 20),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class AmendOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('AmendOrder', AmendOrder_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class UnsolicitedCancelReplaceResponse_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecTransType', c_char),
        ('OrderQty', c_double),
        ('OrdStatus', c_char),
        ('OrdType', c_char),
        ('OrigClOrdID', c_char * 32),
        ('Rule80A', c_char),
        ('Side', c_char),
        ('Symbol', c_char * 12),
        ('TimeInForce', c_char),
        ('TransactTime', c_char * 28),
        ('ExecBroker', c_char * 20),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('Price', c_double),
        ('ParentClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28),
        ('crossingPriceType', c_char * 20),
        ('OrderID', c_char * 32),
        ('MarginTransactionType', c_char),
        ('Text', c_char * 150),
        ('Account', c_char * 32)
    ]


class UnsolicitedCancelReplaceResponse_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('UnsolicitedCancelReplaceResponse', UnsolicitedCancelReplaceResponse_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class BusinessMessageRejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('RefSeqNum', c_int),
        ('Text', c_char * 150),
        ('RefMsgType', c_char * 9),
        ('BusinessRejectRefID', c_char * 32),
        ('BusinessRejectReason', c_char),
        ('EncodedTextLen', c_int),
        ('EncodedText', c_char * 150)
    ]


class BusinessMessageRejected_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('BusinessMessageRejected', BusinessMessageRejected_t),
        ('RecTime', Time_t)
    ]


class TradeSessionStatus_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('TradingSessionID', c_char * 20),
        ('TradSesMode', c_char),
        ('TradSesStatus', c_char)
    ]


class TradeSessionStatus_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('TradeSessionStatus', TradeSessionStatus_t),
        ('RecTime', Time_t)
    ]


class Rejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),

        ('RefSeqNum', c_int),
        ('Text', c_char * 150),
        ('RefTagID', c_int),
        ('RefMsgType', c_char * 9),
        ('SessionRejectReason', c_int)
    ]


class Rejected_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Rejected', Rejected_t),
        ('RecTime', Time_t)
    ]


def OrderDump(ord, indent=None):
    if indent:
        prifix = indent
    else:
        prifix = ""
    print(prifix + "{")
    for attr in ord._fields_:
        attr_name = attr[0]
        attr_val = getattr(ord, attr[0])
        if hasattr(attr_val, "_fields_"):
            print((prifix + "  {} :").format(attr_name))
            OrderDump(attr_val, prifix + "  ")
        else:
            if "tv_sec" == attr_name and 0 <= attr_val:
                print((prifix + "  {} : {} ( {} )").format(attr_name, attr_val, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(attr_val))))
            else:
                print((prifix + "  {} : {}").format(attr_name, attr_val))
    print(prifix + "}")

    '''
    这个方法名为OrderDump，它接受一个名为ord的参数和一个可选的indent参数。该方法的作用是以递归方式将ord对象的属性打印出来，可以用于调试和查看对象的结构。

    下面是对该方法的逐行解析：

    if indent: 和 else: 语句用于确定prifix变量的值。如果indent参数存在，则将prifix设置为indent的值，否则设置为空字符串。
    print(prifix + "{") 打印左花括号{，并在前面添加prifix作为缩进。
    for attr in ord._fields_: 对ord._fields_进行迭代，其中ord是一个对象，_fields_是一个属性，表示对象的字段列表。
    attr_name = attr[0] 获取当前字段的名称。
    attr_val = getattr(ord, attr[0]) 获取当前字段的值，getattr()函数通过反射机制获取对象的属性值。
    if hasattr(attr_val, "_fields_"): 检查当前字段的值是否具有_fields_属性。如果具有，说明它是一个结构体类型的字段，需要递归调用OrderDump方法打印其属性。
    print((prifix + " {} :").format(attr_name)) 打印当前字段的名称，并添加适当的缩进。
    OrderDump(attr_val, prifix + " ") 递归调用OrderDump方法，将当前字段的值作为新的ord对象传递，并添加额外的缩进。
    else: 如果当前字段不是结构体类型的字段，则打印字段的名称和值。
    if "tv_sec" == attr_name and 0 <= attr_val: 检查当前字段的名称是否为"tv_sec"，并且值大于等于0。
    print((prifix + " {} : {} ( {} )").format(attr_name, attr_val, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(attr_val)))) 如果满足条件，则以特定的时间格式打印字段的名称、值和格式化后的时间。
    else: 如果不满足上述条件，则以普通格式打印字段的名称和值。
    print(prifix + "}") 打印右花括号}，并添加适当的缩进。
    这个方法的目的是以递归方式打印对象的属性，并根据特定条件进行格式化输出。通过调用OrderDump方法，你可以将一个对象的结构可视化，以便更好地理解和调试该对象的属性。请注意，代码中使用的time模块需要事先导入才能正常运行。
    '''


consumer = KafkaConsumer(bootstrap_servers=kafka_port)
consumer.subscribe(['Order', 'SystemEvent'])

for msg in consumer:
    msg_len = len(msg.value)
    if 'Order' == msg.topic:
        hd = Header_t.from_buffer_copy(msg.value)
        print("recv msg Msgtype : {}, Evttype : {}, len : {}".format(hd.Msgtype, hd.Evttype, msg_len))
        if b'D' == hd.Msgtype and b'0' == hd.Evttype:
            if (sizeof(NewOrder_t)) + sizeof(Time_t) == msg_len:
                neword = NewOrder_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            elif sizeof(NewOrder_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                neword = NewOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            else:
                print("new order msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'B' == hd.Evttype:
            if (sizeof(OrderAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderAccepted_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("OrderAccepted msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'C' == hd.Evttype:
            if (sizeof(OrderRejected_t)) + sizeof(Time_t) == msg_len:
                ord = OrderRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderRejected_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("OrderRejected msg length err, len : %d" % msg_len)
                exit(0)
        elif b'F' == hd.Msgtype and b'1' == hd.Evttype:
            if (sizeof(CancelOrder_t)) + sizeof(Time_t) == msg_len:
                ord = CancelOrder_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(CancelOrder_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = CancelOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("CancelOrder msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'H' == hd.Evttype:
            if (sizeof(Trade_t)) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Trade_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("Trade msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'D' == hd.Evttype:
            if (sizeof(OrderCancelAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderCancelAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderCancelAccepted_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderCancelAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("OrderCancelAccepted msg length err, len : %d" % msg_len)
                exit(0)
        elif b'9' == hd.Msgtype and b'E' == hd.Evttype:
            if (sizeof(OrderCancelRejected_t)) + sizeof(Time_t) == msg_len:
                ord = OrderCancelRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderCancelRejected_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderCancelRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("OrderCancelRejected msg length err, len : %d" % msg_len)
                exit(0)
        elif b'G' == hd.Msgtype and b'2' == hd.Evttype:
            if (sizeof(AmendOrder_t)) + sizeof(Time_t) == msg_len:
                ord = AmendOrder_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(AmendOrder_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = AmendOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("AmendOrder msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'F' == hd.Evttype:
            if (sizeof(UnsolicitedCancelReplaceResponse_t)) + sizeof(Time_t) == msg_len:
                ord = UnsolicitedCancelReplaceResponse_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(UnsolicitedCancelReplaceResponse_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = UnsolicitedCancelReplaceResponse_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("UnsolicitedCancelReplaceResponse msg length err, len : %d" % msg_len)
                exit(0)
        elif b'j' == hd.Msgtype and b'J' == hd.Evttype:
            if (sizeof(BusinessMessageRejected_t)) == msg_len:
                ord = BusinessMessageRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(BusinessMessageRejected_t) + sizeof(Time_t) == msg_len:
                ord = BusinessMessageRejected_with_time_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("BusinessMessageRejected msg length err, len : %d" % msg_len)
                exit(0)
        elif b'D' == hd.Msgtype and b'Q' == hd.Evttype:
            if (sizeof(NewOrder_t)) + sizeof(Time_t) == msg_len:
                neword = NewOrder_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            elif sizeof(NewOrder_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                neword = NewOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            else:
                print("queueing-order msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'a' == hd.Evttype:
            if (sizeof(Trade_t)) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Trade_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("prop-buy msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'b' == hd.Evttype:
            if (sizeof(Trade_t)) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Trade_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("prop-sell msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'c' == hd.Evttype:
            if (sizeof(Trade_t)) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Trade_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("hrt-buy msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'd' == hd.Evttype:
            if (sizeof(Trade_t)) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Trade_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("hrt-sell msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'S' == hd.Evttype:
            if (sizeof(OrderAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderAccepted_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("snapshot msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'e' == hd.Evttype:
            if (sizeof(OrderAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderAccepted_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("Queuing.OrderAccepted msg length err, len : %d" % msg_len)
                exit(0)
        elif b'8' == hd.Msgtype and b'f' == hd.Evttype:
            if (sizeof(OrderRejected_t)) + sizeof(Time_t) == msg_len:
                ord = OrderRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(OrderRejected_t) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                ord = OrderRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("Queuing.OrderRejected msg length err, len : %d" % msg_len)
                exit(0)
        elif b'3' == hd.Msgtype and b'I' == hd.Evttype:
            if (sizeof(Rejected_t)) == msg_len:
                ord = Rejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif sizeof(Rejected_t) + sizeof(Time_t) == msg_len:
                ord = Rejected_with_time_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print("Rejected msg length err, len : %d" % msg_len)
                exit(0)
        else:
            print("Unsupported message type")
            # exit(0)
    elif 'SystemEvent' == msg.topic:
        print(msg.value)
    else:
        print("Unsupported topic type")