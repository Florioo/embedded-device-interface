from enum import Enum
from typing import Dict
from eros import (
    ErosEndpoint,
    ErosTarget,
)

from .generated import interface_pb2
from .models import GenericModel


class DeviceInterface:
    TARGET = ErosTarget(id=6, realm=0)

    def __init__(self, endpoint: ErosEndpoint):
        self.endpoint = endpoint
        self.endpoint.unexpected_message_callback = self.unexpected_message_callback
        
    def unexpected_message_callback(self, data: bytes):
        print(f"Received unexpected message: {data}")
        
        response = interface_pb2.Message()
        response.ParseFromString(data)
        
        print(f"Response: {response}")
    async def set(
        self,
        values: list[GenericModel] | GenericModel | Enum,
        expect_response: bool = False,
    ) -> interface_pb2.Message | None:
        if isinstance(values, Enum):
            values = values.value
            assert isinstance(values, GenericModel)

        if isinstance(values, GenericModel):
            data = {values.ID: values.encode()}
        else:
            data = {value.ID: value.encode() for value in values}

        return await self.set_request(data, expect_response)

    async def get_single(
        self,
        key: int,
    ) -> bytes | None:
        return (await self.get(key))[key]  # type: ignore

    async def get(
        self,
        keys: list[int] | int,
    ) -> Dict[int, bytes] | None:
        if isinstance(keys, int):
            keys = [keys]

        request = interface_pb2.Message(
            get_request=interface_pb2.GetRequest(
                keys=keys,
            )
        )
        value = await self.send_and_receive(request)
        return {pair.key: pair.value for pair in value.get_response.key_value_status_pairs}  # type: ignore

    async def set_request(self, data: dict[int, bytes], expect_response: bool = False) -> interface_pb2.Message | None:
        request = interface_pb2.Message(
            set_request=interface_pb2.SetRequest(
                ack_required=expect_response,
                key_value_pairs=[interface_pb2.KeyValue(key=key, value=value) for key, value in data.items()],
            )
        )
        if expect_response:
            return await self.send_and_receive(request)
        else:
            return await self.send(request)

    async def send_and_receive(self, message: interface_pb2.Message) -> interface_pb2.Message:
        packed = message.SerializeToString()
        result = await self.endpoint.send_and_receive(packed)
        response = interface_pb2.Message()
        response.ParseFromString(result)
        return response

    async def send(self, message: interface_pb2.Message) -> None:
        packed = message.SerializeToString()
        await self.endpoint.send(packed)
