# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04user\"\x1c\n\x0bUserRequest\x12\r\n\x05login\x18\x01 \x01(\t\" \n\rUserIDRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"5\n\tUserReply\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05login\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t2u\n\x0bUserService\x12/\n\x07GetUser\x12\x11.user.UserRequest\x1a\x0f.user.UserReply\"\x00\x12\x35\n\x0bGetUserByID\x12\x13.user.UserIDRequest\x1a\x0f.user.UserReply\"\x00\x62\x06proto3')



_USERREQUEST = DESCRIPTOR.message_types_by_name['UserRequest']
_USERIDREQUEST = DESCRIPTOR.message_types_by_name['UserIDRequest']
_USERREPLY = DESCRIPTOR.message_types_by_name['UserReply']
UserRequest = _reflection.GeneratedProtocolMessageType('UserRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.UserRequest)
  })
_sym_db.RegisterMessage(UserRequest)

UserIDRequest = _reflection.GeneratedProtocolMessageType('UserIDRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERIDREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.UserIDRequest)
  })
_sym_db.RegisterMessage(UserIDRequest)

UserReply = _reflection.GeneratedProtocolMessageType('UserReply', (_message.Message,), {
  'DESCRIPTOR' : _USERREPLY,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:user.UserReply)
  })
_sym_db.RegisterMessage(UserReply)

_USERSERVICE = DESCRIPTOR.services_by_name['UserService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERREQUEST._serialized_start=20
  _USERREQUEST._serialized_end=48
  _USERIDREQUEST._serialized_start=50
  _USERIDREQUEST._serialized_end=82
  _USERREPLY._serialized_start=84
  _USERREPLY._serialized_end=137
  _USERSERVICE._serialized_start=139
  _USERSERVICE._serialized_end=256
# @@protoc_insertion_point(module_scope)
