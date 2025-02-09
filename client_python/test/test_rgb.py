import asyncio

from eros.transport.websocket import WebsocketInterface
from eros.transport.udp import UDPInterface
from eros import ErosInterface
from device_api import DeviceInterface
import time
from pydantic import BaseModel
import struct
import colorsys
from device_api.models import RGBLed, Servo

from device_api.models import RGBLed

AUTH_INFO = 0x00010000
RGB_LED = 0x0A000000

SERVO_FRONT_LEFT = 0x01010000
SERVO_FRONT_RIGHT = 0x01020000
SERVO_BACK_LEFT = 0x01030000
SERVO_BACK_RIGHT = 0x01040000
SERVO_BACK_CENTER_LEFT = 0x01050000
SERVO_BACK_CENTER_RIGHT = 0x01060000


async def set_color(interface: DeviceInterface, led: RGBLed):
    await interface.set_request({RGB_LED: led.encode()}, expect_response=False)


async def main():
    async with UDPInterface("udp://192.168.1.181:1234", debug=False) as transport:
        # async with WebsocketInterface("ws://192.168.1.181/ws", debug=True) as transport:
        eros = ErosInterface(transport, debug=True)
        await eros.start()
        interface = DeviceInterface.from_eros(eros, source_realm=6)
        while 1:
            STEPS = 100
            DELAY = 0.05
            for i in range(STEPS):
                await interface.set_values(
                    [
                        RGBLed.from_hsv(i / STEPS, 1, 1),
                        Servo(ID=SERVO_FRONT_LEFT, value=10),
                        Servo(ID=SERVO_BACK_LEFT, value=20),
                        Servo(ID=SERVO_FRONT_RIGHT, value=30),
                    ],
                    expect_response=False,
                )
                await asyncio.sleep(DELAY)
                await interface.set_values(RGBLed.from_hsv(i / STEPS, 1, 0))
                await asyncio.sleep(DELAY)

        await asyncio.sleep(1)
        await eros.stop()


if __name__ == "__main__":
    asyncio.run(main())
