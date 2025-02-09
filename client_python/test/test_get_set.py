import asyncio
from eros import ErosInterface, ErosEndpoint, ErosTarget
from eros.transport.udp import UDPInterface
from eros.transport.websocket import WebsocketInterface
from pydantic import BaseModel

from device_api import DeviceInterface
from device_api.models import RGBColors, RGBLed, Servo

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

        endpoint = ErosEndpoint(
            eros=eros,
            source=ErosTarget(id=2, realm=transport.REALM),
            target=DeviceInterface.TARGET,
        )

        interface = DeviceInterface(endpoint)


        result = await interface.set(
            RGBColors.RED,
            expect_response=True,
        )

        await interface.set(
            RGBColors.INVALID_BLUE,
            expect_response=True,
        )

        await interface.set(
            RGBColors.GREEN,
            expect_response=False,
        )

        await interface.set(
            RGBColors.INVALID_BLUE,
            expect_response=False,
        )
        
        await asyncio.sleep(0.5)

        await eros.stop()


if __name__ == "__main__":
    asyncio.run(main())
