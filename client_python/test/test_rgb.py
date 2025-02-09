import asyncio

from eros.transport.udp import UDPInterface
from eros import ErosEndpoint, ErosInterface, ErosTarget
from device_api import DeviceInterface
from device_api.models import RGBLed, Servo


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


IP = "192.168.1.181"


async def main():
    async with UDPInterface(f"udp://{IP}:1234", debug=True) as transport:
        # async with WebsocketInterface(f"ws://{IP}/ws", debug=True) as transport:
        eros = ErosInterface(transport, debug=True)
        await eros.start()

        endpoint = ErosEndpoint(
            eros=eros,
            source=ErosTarget(id=2, realm=transport.REALM),
            target=DeviceInterface.TARGET,
        )

        interface = DeviceInterface(endpoint)

        while 1:
            STEPS = 100
            DELAY = 0.05
            for i in range(STEPS):
                await interface.set(
                    [
                        RGBLed.from_hsv(i / STEPS, 1, 1),
                        Servo(ID=SERVO_FRONT_LEFT, value=10),
                        Servo(ID=SERVO_BACK_LEFT, value=20),
                        Servo(ID=SERVO_FRONT_RIGHT, value=30),
                    ],
                    expect_response=False,
                )
                await asyncio.sleep(DELAY)
                await interface.set(RGBLed.from_hsv(i / STEPS, 1, 0))
                await asyncio.sleep(DELAY)

        await asyncio.sleep(1)
        await eros.stop()


if __name__ == "__main__":
    asyncio.run(main())
