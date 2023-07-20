#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
import os, time
from ctypes import *

consumer = KafkaConsumer(
    'KAFKA_FSX',
    bootstrap_servers=['172.20.214.62:9092']
)


class Header_t(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char)
    ]


class Time_t(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('tv_sec', c_longlong),
        ('tv_usec', c_longlong)
    ]


class BBO_t(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('LastTime', Time_t),
        ('LastPrice', c_double),
        ('LastQty', c_double),
        ('BidTime', Time_t),
        ('BidPrice', c_double),
        ('BidQty', c_double),
        ('AskTime', Time_t),
        ('AskPrice', c_double),
        ('AskQty', c_double)
    ]


class NewOrder_t(LittleEndianStructure):
    _pack_ = 1
    _filed_ = [
        ('Msgtype', c_char),
        ('Evttype', c_char),
        ('SenderID', c_char * 31),
        ('TargetID', c_char * 31),
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
    ]


class NewOrder_with_BBO_t(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('NewOrder', NewOrder_t),
        ('RecvTime', Time_t),
        ('BBO', BBO_t)
    ]


for messgae in consumer:
    print(messgae)
