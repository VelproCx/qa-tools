# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connamara/ep3/instruments/v1beta1/event.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gen.connamara.ep3.hedger.v1beta1 import hedger_pb2 as connamara_dot_ep3_dot_hedger_dot_v1beta1_dot_hedger__pb2
from gen.connamara.ep3.type.v1beta1 import type_pb2 as connamara_dot_ep3_dot_type_dot_v1beta1_dot_type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-connamara/ep3/instruments/v1beta1/event.proto\x12!connamara.ep3.instruments.v1beta1\x1a)connamara/ep3/hedger/v1beta1/hedger.proto\x1a%connamara/ep3/type/v1beta1/type.proto\"\x93\x05\n\x0f\x45ventAttributes\x12<\n\tsub_types\x18\x01 \x03(\x0b\x32).connamara.ep3.hedger.v1beta1.HedgeMarket\x12%\n\x1dposition_accountability_value\x18\x02 \x01(\x03\x12&\n\x1eunderlying_event_specification\x18\x03 \x01(\t\x12\x10\n\x08question\x18\x04 \x01(\t\x12\x15\n\rsource_agency\x18\x05 \x01(\t\x12\x14\n\x0cpayout_value\x18\x06 \x01(\x03\x12\x14\n\x0cstrike_value\x18\x07 \x01(\t\x12\x17\n\x0f\x65valuation_type\x18\x08 \x01(\t\x12\x38\n\x0etime_specifier\x18\t \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12\x10\n\x08\x65vent_id\x18\n \x01(\t\x12\x1a\n\x12\x65vent_display_name\x18\x0b \x01(\t\x12\x13\n\x0bstrike_unit\x18\x0c \x01(\t\x12P\n\x12\x63\x61lculation_method\x18\r \x01(\x0e\x32\x34.connamara.ep3.instruments.v1beta1.CalculationMethod\x12\x16\n\x0eposition_limit\x18\x0e \x01(\x03\x12\x19\n\x11source_agency_url\x18\x0f \x01(\t\x12>\n\x14\x65xpected_payout_date\x18\x10 \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12\x43\n\x14\x65xpected_payout_time\x18\x11 \x01(\x0b\x32%.connamara.ep3.type.v1beta1.TimeOfDay*\xa3\x01\n\x11\x43\x61lculationMethod\x12 \n\x1c\x43\x41LCULATION_METHOD_UNDEFINED\x10\x00\x12\'\n#CALCULATION_METHOD_MONTH_OVER_MONTH\x10\x01\x12%\n!CALCULATION_METHOD_YEAR_OVER_YEAR\x10\x02\x12\x1c\n\x18\x43\x41LCULATION_METHOD_VALUE\x10\x03\x42s\n%com.connamara.ep3.instruments.v1beta1B\nEventProtoP\x01Z\x12instrumentsv1beta1\xa2\x02\x03\x43\x45I\xaa\x02!Connamara.Ep3.Instruments.V1Beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connamara.ep3.instruments.v1beta1.event_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.connamara.ep3.instruments.v1beta1B\nEventProtoP\001Z\022instrumentsv1beta1\242\002\003CEI\252\002!Connamara.Ep3.Instruments.V1Beta1'
  _CALCULATIONMETHOD._serialized_start=829
  _CALCULATIONMETHOD._serialized_end=992
  _EVENTATTRIBUTES._serialized_start=167
  _EVENTATTRIBUTES._serialized_end=826
# @@protoc_insertion_point(module_scope)