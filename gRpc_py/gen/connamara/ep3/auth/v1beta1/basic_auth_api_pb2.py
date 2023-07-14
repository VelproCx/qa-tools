# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connamara/ep3/auth/v1beta1/basic_auth_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/connamara/ep3/auth/v1beta1/basic_auth_api.proto\x12\x1a\x63onnamara.ep3.auth.v1beta1\x1a\x1fgoogle/protobuf/timestamp.proto\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\xa4\x02\n\rLoginResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x35\n\x11\x61\x63\x63\x65ss_issue_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x16\x61\x63\x63\x65ss_expiration_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\rrefresh_token\x18\x04 \x01(\t\x12\x36\n\x12refresh_issue_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12;\n\x17refresh_expiration_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"<\n\rLogoutRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x15\n\rrefresh_token\x18\x02 \x01(\t\"\x10\n\x0eLogoutResponse\"2\n\x0fRegisterRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x12\n\x10RegisterResponse\"2\n\x19RefreshAccessTokenRequest\x12\x15\n\rrefresh_token\x18\x01 \x01(\t\"\xa5\x01\n\x1aRefreshAccessTokenResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x35\n\x11\x61\x63\x63\x65ss_issue_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x16\x61\x63\x63\x65ss_expiration_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"U\n\x15\x43hangePasswordRequest\x12\x14\n\x0cold_password\x18\x01 \x01(\t\x12\x14\n\x0cnew_password\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\"\x18\n\x16\x43hangePasswordResponse2\xb3\x04\n\x0c\x42\x61sicAuthAPI\x12\\\n\x05Login\x12(.connamara.ep3.auth.v1beta1.LoginRequest\x1a).connamara.ep3.auth.v1beta1.LoginResponse\x12\x65\n\x08Register\x12+.connamara.ep3.auth.v1beta1.RegisterRequest\x1a,.connamara.ep3.auth.v1beta1.RegisterResponse\x12_\n\x06Logout\x12).connamara.ep3.auth.v1beta1.LogoutRequest\x1a*.connamara.ep3.auth.v1beta1.LogoutResponse\x12\x83\x01\n\x12RefreshAccessToken\x12\x35.connamara.ep3.auth.v1beta1.RefreshAccessTokenRequest\x1a\x36.connamara.ep3.auth.v1beta1.RefreshAccessTokenResponse\x12w\n\x0e\x43hangePassword\x12\x31.connamara.ep3.auth.v1beta1.ChangePasswordRequest\x1a\x32.connamara.ep3.auth.v1beta1.ChangePasswordResponseBe\n\x1e\x63om.connamara.ep3.auth.v1beta1B\x11\x42\x61sicAuthApiProtoP\x01Z\x0b\x61uthv1beta1\xa2\x02\x03\x43\x45\x41\xaa\x02\x1a\x43onnamara.Ep3.Auth.V1Beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connamara.ep3.auth.v1beta1.basic_auth_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.connamara.ep3.auth.v1beta1B\021BasicAuthApiProtoP\001Z\013authv1beta1\242\002\003CEA\252\002\032Connamara.Ep3.Auth.V1Beta1'
  _LOGINREQUEST._serialized_start=112
  _LOGINREQUEST._serialized_end=162
  _LOGINRESPONSE._serialized_start=165
  _LOGINRESPONSE._serialized_end=457
  _LOGOUTREQUEST._serialized_start=459
  _LOGOUTREQUEST._serialized_end=519
  _LOGOUTRESPONSE._serialized_start=521
  _LOGOUTRESPONSE._serialized_end=537
  _REGISTERREQUEST._serialized_start=539
  _REGISTERREQUEST._serialized_end=589
  _REGISTERRESPONSE._serialized_start=591
  _REGISTERRESPONSE._serialized_end=609
  _REFRESHACCESSTOKENREQUEST._serialized_start=611
  _REFRESHACCESSTOKENREQUEST._serialized_end=661
  _REFRESHACCESSTOKENRESPONSE._serialized_start=664
  _REFRESHACCESSTOKENRESPONSE._serialized_end=829
  _CHANGEPASSWORDREQUEST._serialized_start=831
  _CHANGEPASSWORDREQUEST._serialized_end=916
  _CHANGEPASSWORDRESPONSE._serialized_start=918
  _CHANGEPASSWORDRESPONSE._serialized_end=942
  _BASICAUTHAPI._serialized_start=945
  _BASICAUTHAPI._serialized_end=1508
# @@protoc_insertion_point(module_scope)