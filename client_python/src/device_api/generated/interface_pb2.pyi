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
    ODIN_ERROR: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_NO_PARAMETER: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_INVALID_ARGUMENT: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_PARAMETER_NOT_FOUND: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_SIZE_MISMATCH: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_BUFFER_TOO_SMALL: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_PERMISSION_DENIED: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_UNSUPPORTED_FORMAT: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_NOT_SUPPORTED: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_FILE_NOT_FOUND: _ClassVar[StatusCodeEnum]
    ODIN_ERROR_VALIDATION: _ClassVar[StatusCodeEnum]
SUCCESS: StatusCodeEnum
GENERAL_ERROR: StatusCodeEnum
PARAMETER_NOT_FOUND: StatusCodeEnum
ODIN_ERROR: StatusCodeEnum
ODIN_ERROR_NO_PARAMETER: StatusCodeEnum
ODIN_ERROR_INVALID_ARGUMENT: StatusCodeEnum
ODIN_ERROR_PARAMETER_NOT_FOUND: StatusCodeEnum
ODIN_ERROR_SIZE_MISMATCH: StatusCodeEnum
ODIN_ERROR_BUFFER_TOO_SMALL: StatusCodeEnum
ODIN_ERROR_PERMISSION_DENIED: StatusCodeEnum
ODIN_ERROR_UNSUPPORTED_FORMAT: StatusCodeEnum
ODIN_ERROR_NOT_SUPPORTED: StatusCodeEnum
ODIN_ERROR_FILE_NOT_FOUND: StatusCodeEnum
ODIN_ERROR_VALIDATION: StatusCodeEnum

class Message(_message.Message):
    __slots__ = ("set_request", "set_response", "get_request", "get_response", "status_response")
    SET_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    set_request: SetRequest
    set_response: SetResponse
    get_request: GetRequest
    get_response: GetResponse
    status_response: StatusResponse
    def __init__(self, set_request: _Optional[_Union[SetRequest, _Mapping]] = ..., set_response: _Optional[_Union[SetResponse, _Mapping]] = ..., get_request: _Optional[_Union[GetRequest, _Mapping]] = ..., get_response: _Optional[_Union[GetResponse, _Mapping]] = ..., status_response: _Optional[_Union[StatusResponse, _Mapping]] = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: bytes
    def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...

class KeyStatus(_message.Message):
    __slots__ = ("key", "code")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    key: int
    code: StatusCodeEnum
    def __init__(self, key: _Optional[int] = ..., code: _Optional[_Union[StatusCodeEnum, str]] = ...) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ("key_value_pairs", "ack_required")
    KEY_VALUE_PAIRS_FIELD_NUMBER: _ClassVar[int]
    ACK_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    key_value_pairs: _containers.RepeatedCompositeFieldContainer[KeyValue]
    ack_required: bool
    def __init__(self, key_value_pairs: _Optional[_Iterable[_Union[KeyValue, _Mapping]]] = ..., ack_required: bool = ...) -> None: ...

class SetResponse(_message.Message):
    __slots__ = ("success", "key_status_pairs")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    KEY_STATUS_PAIRS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    key_status_pairs: _containers.RepeatedCompositeFieldContainer[KeyStatus]
    def __init__(self, success: bool = ..., key_status_pairs: _Optional[_Iterable[_Union[KeyStatus, _Mapping]]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: int
    def __init__(self, key: _Optional[int] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("code", "key_value_pairs")
    CODE_FIELD_NUMBER: _ClassVar[int]
    KEY_VALUE_PAIRS_FIELD_NUMBER: _ClassVar[int]
    code: StatusCodeEnum
    key_value_pairs: _containers.RepeatedCompositeFieldContainer[KeyValue]
    def __init__(self, code: _Optional[_Union[StatusCodeEnum, str]] = ..., key_value_pairs: _Optional[_Iterable[_Union[KeyValue, _Mapping]]] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: StatusCodeEnum
    message: str
    def __init__(self, code: _Optional[_Union[StatusCodeEnum, str]] = ..., message: _Optional[str] = ...) -> None: ...
