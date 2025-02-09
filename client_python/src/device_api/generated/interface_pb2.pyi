import nanopb_pb2 as _nanopb_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusCodeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUCCESS: _ClassVar[StatusCodeEnum]
    GENERAL_ERROR: _ClassVar[StatusCodeEnum]
    PARAMETER_NOT_FOUND: _ClassVar[StatusCodeEnum]
SUCCESS: StatusCodeEnum
GENERAL_ERROR: StatusCodeEnum
PARAMETER_NOT_FOUND: StatusCodeEnum

class Message(_message.Message):
    __slots__ = ("set_request", "get_request", "status_response")
    SET_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_REQUEST_FIELD_NUMBER: _ClassVar[int]
    STATUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    set_request: SetRequest
    get_request: GetRequest
    status_response: StatusResponse
    def __init__(self, set_request: _Optional[_Union[SetRequest, _Mapping]] = ..., get_request: _Optional[_Union[GetRequest, _Mapping]] = ..., status_response: _Optional[_Union[StatusResponse, _Mapping]] = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: bytes
    def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ("key_values",)
    KEY_VALUES_FIELD_NUMBER: _ClassVar[int]
    key_values: _containers.RepeatedCompositeFieldContainer[KeyValue]
    def __init__(self, key_values: _Optional[_Iterable[_Union[KeyValue, _Mapping]]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, keys: _Optional[_Iterable[int]] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: StatusCodeEnum
    message: str
    def __init__(self, code: _Optional[_Union[StatusCodeEnum, str]] = ..., message: _Optional[str] = ...) -> None: ...
