from enum import Enum
from typing import List
from eros import (
    ErosInterface,
    PacketTransport,
    ErosEndpoint,
    ErosMessage,
    ErosTarget,
)
from google.protobuf.message import Message

from .generated import interface_pb2
import asyncio
from .models import RGBLed, Servo, GenericModel


AUTH_INFO = 0x00010000
RGB_LED = 0x0A000000
SERVO_FRONT_LEFT = 0x01010000
SERVO_FRONT_RIGHT = 0x01020000
SERVO_BACK_LEFT = 0x01030000
SERVO_BACK_RIGHT = 0x01040000
SERVO_BACK_CENTER_LEFT = 0x01050000
SERVO_BACK_CENTER_RIGHT = 0x01060000


class DeviceInterface:
    TARGET = ErosTarget(id=6, realm=0)

    def __init__(self, endpoint: ErosEndpoint):
        self.endpoint = endpoint

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

    async def set_request(
        self, data: dict[int, bytes], expect_response: bool = False
    ) -> interface_pb2.Message | None:
        request = interface_pb2.Message(
            set_request=interface_pb2.SetRequest(
                ack_required=expect_response,
                key_value_pairs=[
                    interface_pb2.KeyValue(key=key, value=value)
                    for key, value in data.items()
                ],
            )
        )
        if expect_response:
            return await self.send_and_receive(request)
        else:
            return await self.send(request)

    async def send_and_receive(
        self, message: interface_pb2.Message
    ) -> interface_pb2.Message:
        packed = message.SerializeToString()
        result = await self.endpoint.send_and_receive(packed)
        response = interface_pb2.Message()
        response.ParseFromString(result)
        return response

    async def send(self, message: interface_pb2.Message) -> None:
        packed = message.SerializeToString()
        await self.endpoint.send(packed)

    # async def send_request_no_response(
    #     self, message: interface_pb2.Message
    # ) -> interface_pb2.Message:
    #     packed = message.SerializeToString()
    #     await self.endpoint.send(packed)

    # async def send_request(
    #     self, message: interface_pb2.Message
    # ) -> interface_pb2.Message:
    #     packed = message.SerializeToString()

    #     max_retries = 10
    #     timeout = 0.3  # seconds

    #     for attempt in range(max_retries):
    #         try:
    #             await asyncio.wait_for(self.endpoint.send(packed), timeout)

    #             # TODO: Fix the list, it should conceptually not be a list here since we are only expecting one message (the first)
    #             result = await asyncio.wait_for(self.endpoint.receive(), timeout)

    #             # Serialize the result
    #             response = interface_pb2.Message()
    #             response.ParseFromString(result[0])

    #             return response
    #         except asyncio.TimeoutError:
    #             if attempt < max_retries - 1:
    #                 continue  # Retry
    #             else:
    #                 raise  # Exhausted retries
