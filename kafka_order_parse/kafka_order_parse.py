#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
import os, time
from ctypes import *

kafka_port = '172.20.214.62:9092'

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
        # last
        ('LastTime', Time_t),
        ('LastPrice', c_double),
        ('LastQty', c_double),
        # bid
        ('BidTime', Time_t),
        ('BidPrice', c_double),
        ('BidQty', c_double),
        # ask
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
        ('FsxTransactTime', c_char * 28),

        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int),

        ('OrderCapacity', c_char)
    ]


class NewOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('NewOrder', NewOrder_t),
        ('RecvTime', Time_t),
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
        ('FsxTransactTime', c_char * 28),
        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int)
    ]


class OrderAccepted_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderAccepted', OrderAccepted_t),
        ('RecvTime', Time_t),
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
        ('FsxTransactTime', c_char * 28),
        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int)
    ]


class OrderRejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderRejected', OrderRejected_t),
        ('RecvTime', Time_t),
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
        ('LeavesQty', c_double),
        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int)
    ]


class CancelOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('CancelOrder', CancelOrder_t),
        ('RecvTime', Time_t),
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
        ('OrderType', c_char),
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
        ('RecvTime', Time_t),
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
        ('OrderID', c_char * 32),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('RoutingDecisionTime', c_char * 28),
        ('Text', c_char * 150),
        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int)
    ]


class OrderCancelAccepted_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('OrderCancelAccepted', OrderCancelAccepted_t),
        ('RecvTime', Time_t),
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
        ('MarginTransactionType', c_char),
        ('MinQty', c_double),
        ('OrderClassification', c_char),
        ('SelfTradePreventionId', c_int),
        ('EdpLastLiquidityInd', c_char),
        ('SecondaryOrderID', c_char * 32),
        ('ContraBroker', c_char * 20),
        ('SecondaryExecID', c_char * 32)
    ]


class Trade_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Trade', Trade_t),
        ('RecvTime', Time_t),
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
        ('Account', c_char * 32),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('RoutingDecisionTime', c_char * 28),
        ('SecondaryOrderID', c_char * 32),
        ('ContraBroker', c_char * 20),
        ('SecondaryExecID', c_char * 32)
    ]


class UnsolicitedCancelReplaceResponse_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('UnsolicitedCancelReplaceResponse', UnsolicitedCancelReplaceResponse_t),
        ('RecvTime', Time_t),
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
        ('RecTime', Time_t),
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
        ('TradSesStatus', c_int)
    ]


class TradeSessionStatus_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('TradeSessionStatus', TradeSessionStatus_t),
        ('RecTime', Time_t)
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
        ('OrderID', c_char * 32),
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


class QueryOrder_t(LittleEndianStructure):
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
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrderID', c_char * 32),
        ('Account', c_char * 20),
        ('ExecBroker', c_char * 20)
    ]


class QueryOrder_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('QueryOrder', QueryOrder_t),
        ('RecTime', Time_t)
    ]


class TradeSessionStatusRequest_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('TradSesReqID', c_char * 20),
        ('TradingSessionID', c_char * 20),
        ('TradSesMethod', c_char),
        ('TradSesMode', c_char),
        ('SubscriptionRequestType', c_char)
    ]


class TradeSessionStatusRequest_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('TradeSessionStatusRequest', TradeSessionStatusRequest_t),
        ('RecTime', Time_t)
    ]


class TradeSessionStatusCrossRequest_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('TradSesReqID', c_char * 20),
        ('TradSesStatus', c_char),
        ('SecondaryExecID', c_char * 39)
    ]


class TradeSessionStatusCrossRequest_with_time_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('TradeSessionStatusCrossRequest', TradeSessionStatusCrossRequest_t),
        ('RecTime', Time_t)
    ]


class Participant_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Side', c_char),
        ('ClOrdID', c_char * 39),
        ('OrderQty', c_int),
        ('OrderCapacity', c_char),
        ('CashMargin', c_char),
        ('Classification', c_char)
    ]


class EdpCrossNewOrder_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('SenderSubID', c_char * 39),
        ('TargetSubID', c_char * 39),
        ('CrossID', c_char * 32),
        ('CrossType', c_int),
        ('CrossPrioritization', c_int),
        ('Buyer', Participant_t),
        ('Seller', Participant_t),
        ('Symbol', c_char * 12),
        ('SettlType', c_char),
        ('TransactTime', c_char * 28),
        ('OrdType', c_char),
        ('Price', c_double),
        ('TimeInForce', c_char),
        ('TargetStrategy', c_int),
        ('CashMarginBuy', c_char),
        ('CashMarginSell', c_char),
        ('ClassificationBuy', c_char),
        ('ClassificationSell', c_char),
        ('DarkPool', c_char),
        ('OrdStatus', c_char),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class EdpCrossNewOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpCrossNewOrder', EdpCrossNewOrder_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpCrossAcceptance_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('SenderSubID', c_char * 39),
        ('TargetSubID', c_char * 39),
        ('OrderID', c_char * 32),
        ('ClOrdID', c_char * 32),
        ('ListID', c_char * 32),
        ('CrossID', c_char * 32),
        ('ExecID', c_char * 32),
        ('ExecType', c_char),
        ('OrdStatus', c_char),
        ('SettlType', c_char),
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrderQty', c_double),
        ('Price', c_double),
        ('TargetStrategy', c_int),
        ('OrderCapacity', c_char),
        ('LeavesQty', c_double),
        ('CumQty', c_double),
        ('AvgPx', c_double),
        ('TradeTime', c_char * 28),
        ('TradingOrderCapacity', c_char),
        ('CashMargin', c_char),
        ('Classification', c_char),
        ('DarkPool', c_char),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class EdpCrossAcceptance_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpCrossAcceptance', EdpCrossAcceptance_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpCrossRejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('SenderSubID', c_char * 39),
        ('TargetSubID', c_char * 39),
        ('OrderID', c_char * 32),
        ('ClOrdID', c_char * 32),
        ('CrossID', c_char * 32),
        ('ExecID', c_char * 32),
        ('ExecType', c_char),
        ('OrdStatus', c_char),
        ('SettlType', c_char),
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrderQty', c_double),
        ('Price', c_double),
        ('TargetStrategy', c_int),
        ('OrderCapacity', c_char),
        ('LeavesQty', c_double),
        ('CumQty', c_double),
        ('AvgPx', c_double),
        ('Text', c_char * 150),
        ('ErrorTime', c_char * 15),
        ('CashMargin', c_char),
        ('Classification', c_char),
        ('DarkPool', c_char),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class EdpCrossRejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpCrossRejected', EdpCrossRejected_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpCrossExecution_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('SenderSubID', c_char * 39),
        ('TargetSubID', c_char * 39),
        ('OrderID', c_char * 32),
        ('SecondaryOrdID', c_char * 32),
        ('ClOrdID', c_char * 32),
        ('ListID', c_char * 32),
        ('CrossID', c_char * 32),
        ('ExecID', c_char * 32),
        ('ExecType', c_char),
        ('OrdStatus', c_char),
        ('SettlType', c_char),
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrderQty', c_int),
        ('TargetStrategy', c_int),
        ('OrderCapacity', c_char),
        ('LastQty', c_int),
        ('LastPx', c_double),
        ('LeavesQty', c_int),
        ('CumQty', c_int),
        ('AvgPx', c_double),
        ('TradeTime', c_char * 28),
        ('TradingOrderCapacity', c_char),
        ('CashMargin', c_char),
        ('Classification', c_char),
        ('DarkPool', c_char),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class EdpCrossExecution_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpCrossExecution', EdpCrossExecution_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpCrossExpired_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('SenderSubID', c_char * 39),
        ('TargetSubID', c_char * 39),
        ('OrderID', c_char * 32),
        ('ClOrdID', c_char * 32),
        ('ListID', c_char * 32),
        ('CrossID', c_char * 32),
        ('ExecID', c_char * 32),
        ('ExecType', c_char),
        ('OrdStatus', c_char),
        ('SettlType', c_char),
        ('Symbol', c_char * 12),
        ('Side', c_char),
        ('OrderQty', c_double),
        ('Price', c_double),
        ('OrderCapacity', c_char),
        ('LeavesQty', c_double),
        ('CumQty', c_double),
        ('AvgPx', c_double),
        ('Text', c_char * 150),
        ('ExpiryTime', c_char * 15),
        ('TradingOrderCapacity', c_char),
        ('CashMargin', c_char),
        ('Classification', c_char),
        ('DarkPool', c_char),
        ('FsxOrderID', c_char * 32),
        ('FsxTransactTime', c_char * 28)
    ]


class EdpCrossExpired_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpCrossExpired', EdpCrossExpired_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpToSTNetAccepted_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('Account', c_char * 32),
        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecRefID', c_char * 32),
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
        ('MinQty', c_double),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('EdpLastLiquidityInd', c_char),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('RoutingDecisionTime', c_char * 28),
        ('OrderClassification', c_char),
        ('ToSTNetOrderID', c_char * 32),
        ('ToSTNetExecutionID', c_char * 32),
        ('ToSTNetTransactTime', c_char * 28),
        ('CrossingPriceType', c_char * 20),
        ('FsxTransactTime', c_char * 28),
        ('SelfTradePreventionId', c_int),
        ('MarginTransactionType', c_char),
        ('SecondaryOrderID', c_char * 32),
        ('ContraBroker', c_char * 20),
        ('SecondaryExecID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('DarkPool', c_char)
    ]


class EdpToSTNetAccepted_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpToSTNetAccepted', EdpToSTNetAccepted_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpToSTNetRejected_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('Account', c_char * 32),
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
        ('MinQty', c_double),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('EdpLastLiquidityInd', c_char),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('RoutingDecisionTime', c_char * 28),
        ('OrderClassification', c_char),
        ('ToSTNetTransactTime', c_char * 28),
        ('CrossingPriceType', c_char * 20),
        ('PropExecPrice', c_double),
        ('PropExecID', c_char * 32),
        ('FsxTransactTime', c_char * 28),
        ('SelfTradePreventionId', c_int),
        ('MarginTransactionType', c_char),
        ('Text', c_char * 150),
        ('SecondaryOrderID', c_char * 32),
        ('ContraBroker', c_char * 20),
        ('SecondaryExecID', c_char * 32),
        ('OrigClOrdID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('DarkPool', c_char)
    ]


class EdpToSTNetRejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpToSTNetRejected', EdpToSTNetRejected_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
    ]


class EdpToSTNetConfirmation_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 39),
        ('TargetID', c_char * 39),
        ('Msgseqnum', c_int),
        ('Trycount', c_int),
        ('ClientID', c_char * 20),
        ('Account', c_char * 32),
        ('AvgPx', c_double),
        ('ClOrdID', c_char * 32),
        ('CumQty', c_double),
        ('ExecID', c_char * 32),
        ('ExecRefID', c_char * 32),
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
        ('MinQty', c_double),
        ('ExecType', c_char),
        ('LeavesQty', c_double),
        ('CashMargin', c_char),
        ('EdpLastLiquidityInd', c_char),
        ('PrimaryLastPx', c_double),
        ('PrimaryBidPx', c_double),
        ('PrimaryAskPx', c_double),
        ('RoutingDecisionTime', c_char * 28),
        ('OrderClassification', c_char),
        ('ToSTNetOrderID', c_char * 32),
        ('ToSTNetExecutionID', c_char * 32),
        ('ToSTNetTransactTime', c_char * 28),
        ('CrossingPriceType', c_char * 20),
        ('FsxTransactTime', c_char * 28),
        ('SelfTradePreventionId', c_int),
        ('MarginTransactionType', c_char),
        ('SecondaryOrderID', c_char * 32),
        ('ContraBroker', c_char * 20),
        ('SecondaryExecID', c_char * 32),
        ('FsxOrderID', c_char * 32),
        ('DarkPool', c_char),
        ('PropExecID', c_char)
    ]


class EdpToSTNetConfirmation_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('EdpToSTNetConfirmation', EdpToSTNetConfirmation_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
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


class Rejected_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Rejected', Rejected_t),
        ('RecTime', Time_t),
        ('BBO', BBO_t)
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
            print((prifix + f"{attr_name}:"))
            OrderDump(attr_val, prifix + " ")
        else:
            if "tv_sec" == attr_name and 0 <= attr_val:
                print((prifix + " {}: {} ( {} )").format(attr_name, attr_val, time.strftime("%Y-%m-%d %H-%M-%S"),
                                                         time.localtime(attr_val)))
            else:
                print((prifix + f" {attr_name} : {attr_val}"))
    print(prifix + "}")


consumer = KafkaConsumer(bootstrap_servers=kafka_port)
consumer.subscribe(['Order', 'SystemEvent'])

for msg in consumer:
    msg_len = len(msg.value)
    if 'Order' == msg.topic:
        hd = Header_t.from_buffer_copy(msg.value)
        print(f"recv msg Msgtype : {hd.Msgtype}, Evttpype: {hd.Evttype}, len : {msg_len}")
        if b'D' == hd.Msgtype and b'0' == hd.Evttype:
            if (sizeof(NewOrder_t)) + sizeof(Time_t) == msg_len:
                neword = NewOrder_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            elif (sizeof(NewOrder_t)) + sizeof(Time_t) + sizeof(BBO_t) == msg_len:
                neword = NewOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(neword)
            else:
                print(f"New order msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'B' == hd.Evttype:
            if (sizeof(OrderAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(OrderAccepted_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = OrderAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"OrderAccepted msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'C' == hd.Evttype:
            if (sizeof(OrderRejected_t)) + sizeof(Time_t) == msg_len:
                ord = OrderRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(OrderRejected_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = OrderRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"OrderRejected msg length err, len : {msg_len}")
                exit(0)
        elif b'F' == hd.Msgtype and b'1' == hd.Evttype:
            if (sizeof(CancelOrder_t)) + sizeof(Time_t) == msg_len:
                ord = CancelOrder_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(CancelOrder_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = CancelOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"CancelOrder msg length err, len : {msg_len}")
                exit(0)
        elif b'9' == hd.Msgtype and b'E' == hd.Evttype:
            if (sizeof(OrderCancelRejected_t)) + sizeof(Time_t) == msg_len:
                ord = OrderCancelRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(OrderCancelRejected_t)) + sizeof(BBO_t) + sizeof(Time_t):
                ord = OrderCancelRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"OrderCancelRejected msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'D' == hd.Evttype:
            if (sizeof(OrderCancelAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = OrderCancelAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(OrderCancelAccepted_t)) + sizeof(BBO_t) + sizeof(Time_t):
                ord = OrderCancelAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"OrderCancelAccepted msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'H' == hd.Evttype:
            print(sizeof(Trade_t), sizeof(BBO_t), sizeof(Time_t), msg_len)
            if sizeof(Trade_t) + sizeof(Time_t) == msg_len:
                ord = Trade_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(Trade_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = Trade_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"Trade msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'F' == hd.Evttype:
            # if (sizeof(UnsolicitedCancelReplaceResponse_t)) + sizeof(Time_t) == msg_len:
            #     ord = UnsolicitedCancelReplaceResponse_t.from_buffer_copy(msg.value)
            #     OrderDump(ord)
            # elif (sizeof(UnsolicitedCancelReplaceResponse_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
            #     print(sizeof(UnsolicitedCancelReplaceResponse_t), sizeof(BBO_t), sizeof(Time_t))
            #     ord = UnsolicitedCancelReplaceResponse_with_BBO_t.from_buffer_copy(msg.value)
            #     OrderDump(ord)
            # else:
            #     print(sizeof(UnsolicitedCancelReplaceResponse_t), sizeof(BBO_t), sizeof(Time_t), msg_len)
            #     print("UnsolicitedCancelReplaceResponse msg length err, len : {}".format(msg_len))
            #     exit(0)
            if (sizeof(UnsolicitedCancelReplaceResponse_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                print(sizeof(UnsolicitedCancelReplaceResponse_t), sizeof(BBO_t), sizeof(Time_t))
                ord = UnsolicitedCancelReplaceResponse_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                ord = UnsolicitedCancelReplaceResponse_t.from_buffer_copy(msg.value)
                OrderDump(ord)

        elif b'j' == hd.Msgtype and b'J' == hd.Evttype:
            if (sizeof(BusinessMessageRejected_t)) == msg_len:
                ord = BusinessMessageRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(BusinessMessageRejected_t)) + sizeof(Time_t) == msg_len:
                ord = BusinessMessageRejected_with_time_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"BusinessMessageRejected msg length err, len : {msg_len}")
                exit(0)
        elif b'h' == hd.Msgtype and b'G' == hd.Evttype:
            if (sizeof(TradeSessionStatus_t)) == msg_len:
                ord = TradeSessionStatus_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(TradeSessionStatus_t)) + sizeof(Time_t) == msg_len:
                ord = TradeSessionStatus_with_time_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"TradeSessionStatus msg length err, len : {msg_len}")
                exit(0)
        elif b's' == hd.Msgtype and b'L' == hd.Evttype:
            print(sizeof(EdpCrossNewOrder_t), sizeof(Time_t), msg_len)
            if (sizeof(EdpCrossNewOrder_t)) + sizeof(Time_t) == msg_len:
                ord = EdpCrossNewOrder_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpCrossNewOrder_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpCrossNewOrder_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpCrossNewOrder msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'M' == hd.Evttype:
            if (sizeof(EdpCrossAcceptance_t)) + sizeof(Time_t) == msg_len:
                ord = EdpCrossAcceptance_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpCrossAcceptance_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpCrossAcceptance_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpCrossAcceptance msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'N' == hd.Evttype:
            if (sizeof(EdpCrossRejected_t)) + sizeof(Time_t) == msg_len:
                ord = EdpCrossRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpCrossRejected_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpCrossRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpCrossRejected msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'O' == hd.Evttype:
            if (sizeof(EdpCrossExecution_t)) + sizeof(Time_t) == msg_len:
                ord = EdpCrossExecution_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpCrossExecution_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpCrossExecution_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpCrossExecution msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'P' == hd.Evttype:
            if (sizeof(EdpCrossExpired_t)) + sizeof(Time_t) == msg_len:
                ord = EdpCrossExpired_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpCrossExpired_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpCrossExpired_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpCrossExpired msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'K' == hd.Evttype:
            if (sizeof(EdpToSTNetAccepted_t)) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetAccepted_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpToSTNetAccepted_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetAccepted_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpToSTNetAccepted msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'R' == hd.Evttype:
            if (sizeof(EdpToSTNetRejected_t)) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetRejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpToSTNetRejected_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetRejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpToSTNetRejected msg length err, len : {msg_len}")
                exit(0)
        elif b'8' == hd.Msgtype and b'V' == hd.Evttype:
            if (sizeof(EdpToSTNetConfirmation_t)) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetConfirmation_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(EdpToSTNetConfirmation_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = EdpToSTNetConfirmation_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            else:
                print(f"EdpToSTNetConfirmation msg length err, len : {msg_len}")
                exit(0)
        elif b'3' == hd.Msgtype and b'I' == hd.Evttype:
            if (sizeof(Rejected_t)) + sizeof(Time_t) == msg_len:
                ord = Rejected_t.from_buffer_copy(msg.value)
                OrderDump(ord)
            elif (sizeof(Rejected_t)) + sizeof(BBO_t) + sizeof(Time_t) == msg_len:
                ord = Rejected_with_BBO_t.from_buffer_copy(msg.value)
                OrderDump(ord)
    elif 'SystemEvent' == msg.topic:
        print(msg.value)
    else:
        print("Unsupported topic type")
