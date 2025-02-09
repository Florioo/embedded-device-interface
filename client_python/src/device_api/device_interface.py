from typing import List
from eros import (
    ErosInterface,
    PacketTransport,
    ErosPacketTransport,
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
    def __init__(self, packet_transport: ErosPacketTransport):
        self.packet_transport = packet_transport

    @classmethod
    def from_eros(
        cls,
        eros: ErosInterface,
        source_id: int = 2,
        source_realm: int = 5,
        target_id: int = 6,
        target_realm: int = 0,
    ):
        return cls(
            eros.get_transport(
                source=ErosTarget(id=source_id, realm=source_realm),
                target=ErosTarget(id=target_id, realm=target_realm),
            )
        )

    async def set_values(
        self, values: list[GenericModel] | GenericModel, expect_response: bool = False
    ) -> interface_pb2.Message:
        if isinstance(values, GenericModel):
            data = {values.ID: values.encode()}
        else:
            data = {value.ID: value.encode() for value in values}
        return await self.set_request(data, expect_response)

    async def set_request(
        self, data: dict[int, bytes], expect_response: bool = False
    ) -> interface_pb2.Message:
        request = interface_pb2.Message(
            set_request=interface_pb2.SetRequest(
                key_values=[
                    interface_pb2.KeyValue(key=key, value=value)
                    for key, value in data.items()
                ]
            )
        )
        if expect_response:
            return await self.send_request(request)
        else:
            return await self.send_request_no_response(request)

    async def send_request_no_response(
        self, message: interface_pb2.Message
    ) -> interface_pb2.Message:
        packed = message.SerializeToString()
        await self.packet_transport.send(packed)

    async def send_request(
        self, message: interface_pb2.Message
    ) -> interface_pb2.Message:
        packed = message.SerializeToString()

        max_retries = 10
        timeout = 0.3  # seconds

        for attempt in range(max_retries):
            try:
                await asyncio.wait_for(self.packet_transport.send(packed), timeout)

                # TODO: Fix the list, it should conceptually not be a list here since we are only expecting one message (the first)
                result = await asyncio.wait_for(
                    self.packet_transport.receive(), timeout
                )

                # Serialize the result
                response = interface_pb2.Message()
                response.ParseFromString(result[0])

                return response
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    continue  # Retry
                else:
                    raise  # Exhausted retries
