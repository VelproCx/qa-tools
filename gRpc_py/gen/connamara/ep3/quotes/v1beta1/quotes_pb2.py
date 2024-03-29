# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connamara/ep3/quotes/v1beta1/quotes.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gen.connamara.ep3.orders.v1beta1 import orders_pb2 as connamara_dot_ep3_dot_orders_dot_v1beta1_dot_orders__pb2
from gen.connamara.ep3.orders.v1beta1 import orders_context_pb2 as connamara_dot_ep3_dot_orders_dot_v1beta1_dot_orders__context__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)connamara/ep3/quotes/v1beta1/quotes.proto\x12\x1c\x63onnamara.ep3.quotes.v1beta1\x1a)connamara/ep3/orders/v1beta1/orders.proto\x1a\x31\x63onnamara/ep3/orders/v1beta1/orders_context.proto\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc6\x04\n\x05Quote\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tclient_id\x18\x03 \x01(\t\x12\x18\n\x10quote_request_id\x18\x04 \x01(\t\x12\r\n\x05price\x18\x05 \x01(\x03\x12\x30\n\x04side\x18\x06 \x01(\x0e\x32\".connamara.ep3.orders.v1beta1.Side\x12\x11\n\torder_qty\x18\x07 \x01(\x03\x12\x0e\n\x06symbol\x18\x08 \x01(\t\x12\x33\n\x0f\x65xpiration_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07\x61\x63\x63ount\x18\n \x01(\t\x12\x0c\n\x04user\x18\x0b \x01(\t\x12\x0c\n\x04\x66irm\x18\x0c \x01(\t\x12;\n\x07\x63ontext\x18\r \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.OrderContext\x12\x42\n\x0eparent_context\x18\x0e \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.OrderContext\x12\x39\n\x06status\x18\x0f \x01(\x0e\x32).connamara.ep3.quotes.v1beta1.QuoteStatus\x12\x10\n\x08\x63lord_id\x18\x11 \x01(\t\x12/\n\x0binsert_time\x18\x12 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x18\n\x10risk_approval_id\x18\x13 \x01(\t\x12\x17\n\x0fsubmitting_user\x18\x14 \x01(\t\"\xc6\x03\n\x0fRequestForQuote\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tclient_id\x18\x03 \x01(\t\x12\x30\n\x04side\x18\x04 \x01(\x0e\x32\".connamara.ep3.orders.v1beta1.Side\x12\x11\n\torder_qty\x18\x05 \x01(\x03\x12\x0e\n\x06symbol\x18\x06 \x01(\t\x12\x33\n\x0f\x65xpiration_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07\x61\x63\x63ount\x18\x08 \x01(\t\x12\x0c\n\x04user\x18\t \x01(\t\x12\r\n\x05\x66irms\x18\n \x03(\t\x12/\n\x0binsert_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12;\n\x07\x63ontext\x18\x0c \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.OrderContext\x12\x39\n\x06status\x18\r \x01(\x0e\x32).connamara.ep3.quotes.v1beta1.QuoteStatus\x12\x0c\n\x04\x66irm\x18\x0e \x01(\t\x12\x17\n\x0fsubmitting_user\x18\x0f \x01(\t\"v\n\x0bQuoteCancel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\x12;\n\x07\x63ontext\x18\x0c \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.OrderContext\"t\n\tQuotePass\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\x12;\n\x07\x63ontext\x18\x0c \x01(\x0b\x32*.connamara.ep3.orders.v1beta1.OrderContext\"\x81\x03\n\x0bQuoteReject\x12J\n\x11request_for_quote\x18\x01 \x01(\x0b\x32-.connamara.ep3.quotes.v1beta1.RequestForQuoteH\x00\x12\x34\n\x05quote\x18\x02 \x01(\x0b\x32#.connamara.ep3.quotes.v1beta1.QuoteH\x00\x12\x41\n\x0cquote_cancel\x18\x03 \x01(\x0b\x32).connamara.ep3.quotes.v1beta1.QuoteCancelH\x00\x12=\n\nquote_pass\x18\x05 \x01(\x0b\x32\'.connamara.ep3.quotes.v1beta1.QuotePassH\x00\x12\x46\n\rreject_reason\x18\n \x01(\x0e\x32/.connamara.ep3.quotes.v1beta1.QuoteRejectReason\x12\x0c\n\x04text\x18\x0b \x01(\t\x12\x0e\n\x06symbol\x18\x0c \x01(\tB\x08\n\x06parent\"8\n\nQuoteEvent\x12*\n\x0cquote_events\x18\x05 \x03(\x0b\x32\x14.google.protobuf.Any*\x81\x02\n\x0bQuoteStatus\x12\x1a\n\x16QUOTE_STATUS_UNDEFINED\x10\x00\x12\x18\n\x14QUOTE_STATUS_PENDING\x10\x01\x12\x19\n\x15QUOTE_STATUS_ACCEPTED\x10\x02\x12\x18\n\x14QUOTE_STATUS_DELETED\x10\x03\x12\x18\n\x14QUOTE_STATUS_EXPIRED\x10\x04\x12\x17\n\x13QUOTE_STATUS_PASSED\x10\x05\x12\x1a\n\x16QUOTE_STATUS_DONE_AWAY\x10\x06\x12\x1d\n\x19QUOTE_STATUS_PENDING_RISK\x10\x07\x12\x19\n\x15QUOTE_STATUS_REJECTED\x10\x08*\xa6\x01\n\x11QuoteRejectReason\x12!\n\x1dQUOTE_REJECT_REASON_UNDEFINED\x10\x00\x12\x1d\n\x19QUOTE_REJECT_REASON_OTHER\x10\x01\x12&\n\"QUOTE_REJECT_REASON_UNKNOWN_SYMBOL\x10\x02\x12\'\n#QUOTE_REJECT_REASON_EXCHANGE_CLOSED\x10\x03\x42\x65\n com.connamara.ep3.quotes.v1beta1B\x0bQuotesProtoP\x01Z\rquotesv1beta1\xa2\x02\x03\x43\x45Q\xaa\x02\x1c\x43onnamara.Ep3.Quotes.V1Beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connamara.ep3.quotes.v1beta1.quotes_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n com.connamara.ep3.quotes.v1beta1B\013QuotesProtoP\001Z\rquotesv1beta1\242\002\003CEQ\252\002\034Connamara.Ep3.Quotes.V1Beta1'
  _QUOTESTATUS._serialized_start=1956
  _QUOTESTATUS._serialized_end=2213
  _QUOTEREJECTREASON._serialized_start=2216
  _QUOTEREJECTREASON._serialized_end=2382
  _QUOTE._serialized_start=230
  _QUOTE._serialized_end=812
  _REQUESTFORQUOTE._serialized_start=815
  _REQUESTFORQUOTE._serialized_end=1269
  _QUOTECANCEL._serialized_start=1271
  _QUOTECANCEL._serialized_end=1389
  _QUOTEPASS._serialized_start=1391
  _QUOTEPASS._serialized_end=1507
  _QUOTEREJECT._serialized_start=1510
  _QUOTEREJECT._serialized_end=1895
  _QUOTEEVENT._serialized_start=1897
  _QUOTEEVENT._serialized_end=1953
# @@protoc_insertion_point(module_scope)
