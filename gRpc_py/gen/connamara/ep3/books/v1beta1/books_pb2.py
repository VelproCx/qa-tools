# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connamara/ep3/books/v1beta1/books.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gen.connamara.ep3.instruments.v1beta1 import instruments_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_instruments__pb2
from gen.connamara.ep3.orders.v1beta1 import orders_pb2 as connamara_dot_ep3_dot_orders_dot_v1beta1_dot_orders__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'connamara/ep3/books/v1beta1/books.proto\x12\x1b\x63onnamara.ep3.books.v1beta1\x1a\x33\x63onnamara/ep3/instruments/v1beta1/instruments.proto\x1a)connamara/ep3/orders/v1beta1/orders.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19google/protobuf/any.proto\"\xf4\x01\n\x13SetBookStateRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12<\n\x05state\x18\x02 \x01(\x0e\x32-.connamara.ep3.books.v1beta1.BookStatus.State\x12\x42\n\x0bprice_limit\x18\x03 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.PriceLimit\x12K\n\x10order_size_limit\x18\x04 \x01(\x0b\x32\x31.connamara.ep3.instruments.v1beta1.OrderSizeLimit\"\xf6\x07\n\tBookStats\x12\x0c\n\x04open\x18\x01 \x01(\x03\x12\r\n\x05\x63lose\x18\x02 \x01(\x03\x12\x0c\n\x04high\x18\x03 \x01(\x03\x12\x0b\n\x03low\x18\x04 \x01(\x03\x12\x12\n\nlast_trade\x18\x05 \x01(\x03\x12\x10\n\x08open_set\x18\x06 \x01(\x08\x12\x11\n\tclose_set\x18\x07 \x01(\x08\x12\x10\n\x08high_set\x18\x08 \x01(\x08\x12\x0f\n\x07low_set\x18\t \x01(\x08\x12\x16\n\x0elast_trade_set\x18\n \x01(\x08\x12\x17\n\x0findicative_open\x18\x0b \x01(\x03\x12\x1b\n\x13indicative_open_set\x18\x0c \x01(\x08\x12\x12\n\nsettlement\x18\r \x01(\x03\x12\x16\n\x0esettlement_set\x18\x0e \x01(\x08\x12\x15\n\rshares_traded\x18\x0f \x01(\x03\x12\x19\n\x11shares_traded_set\x18\x10 \x01(\x08\x12\x17\n\x0fnotional_traded\x18\x11 \x01(\x03\x12\x1b\n\x13notional_traded_set\x18\x12 \x01(\x08\x12\x16\n\x0elast_trade_qty\x18\x13 \x01(\x03\x12\x1a\n\x12last_trade_qty_set\x18\x14 \x01(\x08\x12\x15\n\ropen_interest\x18\x15 \x01(\x03\x12\x19\n\x11open_interest_set\x18\x16 \x01(\x08\x12\x1e\n\x16settlement_preliminary\x18\x17 \x01(\x08\x12\x31\n\ropen_set_time\x18\x18 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0e\x63lose_set_time\x18\x19 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rhigh_set_time\x18\x1a \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0clow_set_time\x18\x1b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x37\n\x13last_trade_set_time\x18\x1c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12<\n\x18indicative_open_set_time\x18\x1d \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x37\n\x13settlement_set_time\x18\x1e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x16open_interest_set_time\x18\x1f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x35\n\x11notional_set_time\x18  \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xb4\x04\n\nBookStatus\x12<\n\x05state\x18\x01 \x01(\x0e\x32-.connamara.ep3.books.v1beta1.BookStatus.State\x12\x42\n\x0bprice_limit\x18\x04 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.PriceLimit\x12:\n\nbook_stats\x18\x05 \x01(\x0b\x32&.connamara.ep3.books.v1beta1.BookStats\x12K\n\x10order_size_limit\x18\x06 \x01(\x0b\x32\x31.connamara.ep3.instruments.v1beta1.OrderSizeLimit\x12\x1e\n\x16minimum_trade_quantity\x18\x07 \x01(\x03\x12\x11\n\ttick_size\x18\x08 \x01(\x03\x12\x31\n\rtransact_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12%\n\x07\x63ontext\x18\x10 \x01(\x0b\x32\x14.google.protobuf.Any\"\x8d\x01\n\x05State\x12\x10\n\x0cSTATE_CLOSED\x10\x00\x12\x0e\n\nSTATE_OPEN\x10\x01\x12\x13\n\x0fSTATE_SUSPENDED\x10\x02\x12\x11\n\rSTATE_EXPIRED\x10\x03\x12\x12\n\x0eSTATE_PRE_OPEN\x10\x04\x12\x14\n\x10STATE_TERMINATED\x10\x05\x12\x10\n\x0cSTATE_HALTED\x10\x06\"\xe8\x05\n\tBookEvent\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x19\n\x11\x62ook_state_change\x18\x03 \x01(\x08\x12\x33\n\x06orders\x18\x04 \x03(\x0b\x32#.connamara.ep3.orders.v1beta1.Order\x12\x31\n\rtransact_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x41\n\rcancel_reject\x18\x08 \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.CancelReject\x12%\n\x07trigger\x18\t \x01(\x0b\x32\x14.google.protobuf.Any\x12%\n\x07\x63ontext\x18\x10 \x01(\x0b\x32\x14.google.protobuf.Any\x12;\n\nexecutions\x18\x11 \x03(\x0b\x32\'.connamara.ep3.orders.v1beta1.Execution\x12[\n\x13\x61ssociated_statuses\x18\x12 \x03(\x0b\x32>.connamara.ep3.books.v1beta1.BookEvent.AssociatedStatusesEntry\x12W\n\x11previous_statuses\x18\x13 \x03(\x0b\x32<.connamara.ep3.books.v1beta1.BookEvent.PreviousStatusesEntry\x1a\x62\n\x17\x41ssociatedStatusesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.connamara.ep3.books.v1beta1.BookStatus:\x02\x38\x01\x1a`\n\x15PreviousStatusesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.connamara.ep3.books.v1beta1.BookStatus:\x02\x38\x01\"\xf7\x02\n\x0c\x42ookSnapshot\x12\x31\n\x04\x62ids\x18\x01 \x03(\x0b\x32#.connamara.ep3.orders.v1beta1.Order\x12\x33\n\x06offers\x18\x02 \x03(\x0b\x32#.connamara.ep3.orders.v1beta1.Order\x12\x37\n\x06status\x18\x03 \x01(\x0b\x32\'.connamara.ep3.books.v1beta1.BookStatus\x12\x36\n\tstop_bids\x18\x04 \x03(\x0b\x32#.connamara.ep3.orders.v1beta1.Order\x12\x38\n\x0bstop_offers\x18\x05 \x03(\x0b\x32#.connamara.ep3.orders.v1beta1.Order\x12.\n\nas_of_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12$\n\x1csearch_executions_page_token\x18\x07 \x01(\tBa\n\x1f\x63om.connamara.ep3.books.v1beta1B\nBooksProtoP\x01Z\x0c\x62ooksv1beta1\xa2\x02\x03\x43\x45\x42\xaa\x02\x1b\x43onnamara.Ep3.Books.V1Beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connamara.ep3.books.v1beta1.books_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037com.connamara.ep3.books.v1beta1B\nBooksProtoP\001Z\014booksv1beta1\242\002\003CEB\252\002\033Connamara.Ep3.Books.V1Beta1'
  _BOOKEVENT_ASSOCIATEDSTATUSESENTRY._options = None
  _BOOKEVENT_ASSOCIATEDSTATUSESENTRY._serialized_options = b'8\001'
  _BOOKEVENT_PREVIOUSSTATUSESENTRY._options = None
  _BOOKEVENT_PREVIOUSSTATUSESENTRY._serialized_options = b'8\001'
  _SETBOOKSTATEREQUEST._serialized_start=229
  _SETBOOKSTATEREQUEST._serialized_end=473
  _BOOKSTATS._serialized_start=476
  _BOOKSTATS._serialized_end=1490
  _BOOKSTATUS._serialized_start=1493
  _BOOKSTATUS._serialized_end=2057
  _BOOKSTATUS_STATE._serialized_start=1916
  _BOOKSTATUS_STATE._serialized_end=2057
  _BOOKEVENT._serialized_start=2060
  _BOOKEVENT._serialized_end=2804
  _BOOKEVENT_ASSOCIATEDSTATUSESENTRY._serialized_start=2608
  _BOOKEVENT_ASSOCIATEDSTATUSESENTRY._serialized_end=2706
  _BOOKEVENT_PREVIOUSSTATUSESENTRY._serialized_start=2708
  _BOOKEVENT_PREVIOUSSTATUSESENTRY._serialized_end=2804
  _BOOKSNAPSHOT._serialized_start=2807
  _BOOKSNAPSHOT._serialized_end=3182
# @@protoc_insertion_point(module_scope)
