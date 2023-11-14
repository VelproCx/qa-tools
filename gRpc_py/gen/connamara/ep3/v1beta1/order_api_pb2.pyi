from connamara.ep3.v1beta1 import api_pb2 as _api_pb2
from connamara.ep3.orders.v1beta1 import orders_pb2 as _orders_pb2
from connamara.ep3.trades.v1beta1 import trades_pb2 as _trades_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DownloadExecutionsRequest(_message.Message):
    __slots__ = ["accounts", "end_time", "start_time"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    end_time: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accounts: _Optional[_Iterable[str]] = ...) -> None: ...

class DownloadExecutionsResponse(_message.Message):
    __slots__ = ["filechunk"]
    FILECHUNK_FIELD_NUMBER: _ClassVar[int]
    filechunk: str
    def __init__(self, filechunk: _Optional[str] = ...) -> None: ...

class DownloadOrdersRequest(_message.Message):
    __slots__ = ["accounts", "end_time", "start_time"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    end_time: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accounts: _Optional[_Iterable[str]] = ...) -> None: ...

class DownloadOrdersResponse(_message.Message):
    __slots__ = ["filechunk"]
    FILECHUNK_FIELD_NUMBER: _ClassVar[int]
    filechunk: str
    def __init__(self, filechunk: _Optional[str] = ...) -> None: ...

class DownloadTradesRequest(_message.Message):
    __slots__ = ["accounts", "end_time", "start_time"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    end_time: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accounts: _Optional[_Iterable[str]] = ...) -> None: ...

class DownloadTradesResponse(_message.Message):
    __slots__ = ["filechunk"]
    FILECHUNK_FIELD_NUMBER: _ClassVar[int]
    filechunk: str
    def __init__(self, filechunk: _Optional[str] = ...) -> None: ...

class SearchExecutionsRequest(_message.Message):
    __slots__ = ["accounts", "clord_id", "end_time", "newest_first", "order_id", "page_size", "page_token", "start_time", "symbol", "types"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    CLORD_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NEWEST_FIRST_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    clord_id: str
    end_time: _timestamp_pb2.Timestamp
    newest_first: bool
    order_id: str
    page_size: int
    page_token: str
    start_time: _timestamp_pb2.Timestamp
    symbol: str
    types: _containers.RepeatedScalarFieldContainer[_orders_pb2.ExecutionType]
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., order_id: _Optional[str] = ..., clord_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., symbol: _Optional[str] = ..., types: _Optional[_Iterable[_Union[_orders_pb2.ExecutionType, str]]] = ..., newest_first: bool = ..., accounts: _Optional[_Iterable[str]] = ...) -> None: ...

class SearchExecutionsResponse(_message.Message):
    __slots__ = ["eof", "executions", "next_page_token"]
    EOF_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    eof: bool
    executions: _containers.RepeatedCompositeFieldContainer[_api_pb2.Execution]
    next_page_token: str
    def __init__(self, executions: _Optional[_Iterable[_Union[_api_pb2.Execution, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., eof: bool = ...) -> None: ...

class SearchOrdersRequest(_message.Message):
    __slots__ = ["accounts", "clord_id", "end_time", "order_id", "page_size", "page_token", "start_time", "symbol"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    CLORD_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    clord_id: str
    end_time: _timestamp_pb2.Timestamp
    order_id: str
    page_size: int
    page_token: str
    start_time: _timestamp_pb2.Timestamp
    symbol: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., order_id: _Optional[str] = ..., clord_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., symbol: _Optional[str] = ..., accounts: _Optional[_Iterable[str]] = ...) -> None: ...

class SearchOrdersResponse(_message.Message):
    __slots__ = ["next_page_token", "order"]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    order: _containers.RepeatedCompositeFieldContainer[_api_pb2.Order]
    def __init__(self, order: _Optional[_Iterable[_Union[_api_pb2.Order, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchTradesRequest(_message.Message):
    __slots__ = ["accounts", "end_time", "exec_id", "order_id", "page_size", "page_token", "start_time", "states", "symbol", "trade_id"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXEC_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TRADE_ID_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedScalarFieldContainer[str]
    end_time: _timestamp_pb2.Timestamp
    exec_id: str
    order_id: str
    page_size: int
    page_token: str
    start_time: _timestamp_pb2.Timestamp
    states: _containers.RepeatedScalarFieldContainer[_trades_pb2.TradeState]
    symbol: str
    trade_id: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., order_id: _Optional[str] = ..., trade_id: _Optional[str] = ..., exec_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., symbol: _Optional[str] = ..., accounts: _Optional[_Iterable[str]] = ..., states: _Optional[_Iterable[_Union[_trades_pb2.TradeState, str]]] = ...) -> None: ...

class SearchTradesResponse(_message.Message):
    __slots__ = ["next_page_token", "trade"]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    trade: _containers.RepeatedCompositeFieldContainer[_api_pb2.Trade]
    def __init__(self, trade: _Optional[_Iterable[_Union[_api_pb2.Trade, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...
