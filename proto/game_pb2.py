# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\x12\x04game\"9\n\x04Move\x12\x0e\n\x06moving\x18\x01 \x02(\x08\x12\x11\n\tdirection\x18\x02 \x02(\x05\x12\x0e\n\x06\x61ttack\x18\x03 \x02(\x05\"\xe8\x01\n\x06Update\x12\x0e\n\x06health\x18\x01 \x02(\x05\x12\x11\n\tenemyMove\x18\x02 \x02(\x05\x12\x0e\n\x06moving\x18\x03 \x02(\x08\x12\x13\n\x0b\x65nemyHealth\x18\x04 \x02(\x05\x12\x13\n\x0b\x65nemyAttack\x18\x05 \x02(\x05\x12\t\n\x01x\x18\x06 \x02(\x05\x12\t\n\x01y\x18\x07 \x02(\x05\x12$\n\x04keys\x18\x08 \x03(\x0b\x32\x16.game.Update.KeysEntry\x12\n\n\x02id\x18\t \x02(\x08\x12\x0c\n\x04quit\x18\n \x02(\x08\x1a+\n\tKeysEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\" \n\x10JoinLobbyRequest\x12\x0c\n\x04name\x18\x01 \x02(\t\"\'\n\x12\x43reateLobbyRequest\x12\x11\n\tlobbyCode\x18\x01 \x02(\t\">\n\x13\x43reateLobbyResponse\x12\n\n\x02ok\x18\x01 \x02(\x08\x12\x0c\n\x04port\x18\x02 \x02(\x05\x12\r\n\x05start\x18\x03 \x02(\x08\"@\n\x11JoinLobbyResponse\x12\n\n\x02ok\x18\x01 \x02(\x08\x12\x10\n\x08playerId\x18\x02 \x02(\x08\x12\r\n\x05start\x18\x03 \x02(\x08\"I\n\x16\x43haracterSelectRequest\x12\n\n\x02id\x18\x01 \x02(\x08\x12\x11\n\tcharacter\x18\x02 \x02(\x05\x12\x10\n\x08lockedIn\x18\x03 \x02(\x08\"^\n\x17\x43haracterSelectResponse\x12\x10\n\x08playerId\x18\x01 \x02(\x08\x12\n\n\x02ok\x18\x02 \x02(\x08\x12\r\n\x05start\x18\x03 \x02(\x08\x12\x16\n\x0e\x65nemyCharacter\x18\x04 \x02(\x05\"E\n\x10MapSelectRequest\x12\x10\n\x08playerId\x18\x01 \x02(\x08\x12\r\n\x05mapId\x18\x02 \x02(\x05\x12\x10\n\x08lockedIn\x18\x03 \x02(\x08\"U\n\x11MapSelectResponse\x12\n\n\x02ok\x18\x01 \x02(\x08\x12\r\n\x05mapId\x18\x02 \x02(\x05\x12\r\n\x05start\x18\x03 \x02(\x08\x12\x16\n\x0e\x65nemySelection\x18\x04 \x02(\x05')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UPDATE_KEYSENTRY._options = None
  _UPDATE_KEYSENTRY._serialized_options = b'8\001'
  _MOVE._serialized_start=20
  _MOVE._serialized_end=77
  _UPDATE._serialized_start=80
  _UPDATE._serialized_end=312
  _UPDATE_KEYSENTRY._serialized_start=269
  _UPDATE_KEYSENTRY._serialized_end=312
  _JOINLOBBYREQUEST._serialized_start=314
  _JOINLOBBYREQUEST._serialized_end=346
  _CREATELOBBYREQUEST._serialized_start=348
  _CREATELOBBYREQUEST._serialized_end=387
  _CREATELOBBYRESPONSE._serialized_start=389
  _CREATELOBBYRESPONSE._serialized_end=451
  _JOINLOBBYRESPONSE._serialized_start=453
  _JOINLOBBYRESPONSE._serialized_end=517
  _CHARACTERSELECTREQUEST._serialized_start=519
  _CHARACTERSELECTREQUEST._serialized_end=592
  _CHARACTERSELECTRESPONSE._serialized_start=594
  _CHARACTERSELECTRESPONSE._serialized_end=688
  _MAPSELECTREQUEST._serialized_start=690
  _MAPSELECTREQUEST._serialized_end=759
  _MAPSELECTRESPONSE._serialized_start=761
  _MAPSELECTRESPONSE._serialized_end=846
# @@protoc_insertion_point(module_scope)
