import asyncio

from eros.transport.websocket import WebsocketInterface
from eros.transport.udp import UDPInterface
from eros import ErosEndpoint, ErosInterface, ErosTarget
from device_api import DeviceInterface
from device_api.models import RGBLed, Servo
import time
from pydantic import BaseModel

SERVO_FRONT_LEFT = 0x01010000

IP = "192.168.1.181"


async def main():
    # async with UDPInterface(f"udp://{IP}:1234", debug=True) as transport:
    async with WebsocketInterface(f"ws://{IP}/ws", debug=True) as transport:
        eros = ErosInterface(transport, debug=True)
        await eros.start()

        endpoint = ErosEndpoint(
            eros=eros,
            source=ErosTarget(id=2, realm=transport.REALM),
            target=ErosTarget(id=2, realm=transport.REALM),
        )
        interface = DeviceInterface(endpoint)

        start_time = time.time()

        # Test once
        N = 1
        # await interface.set(Servo(ID=SERVO_FRONT_LEFT, value=10), expect_response=True)

        # Test with gather
        N = 16
        await asyncio.gather(
            *[interface.set(Servo(ID=SERVO_FRONT_LEFT, value=10), expect_response=True) for _ in range(N)]
        )
        
        ms_delay = (time.time() - start_time) * 1000

        await asyncio.sleep(0.1)
        await eros.stop()

        print("Finished")

        print(f"Time taken ms: {ms_delay}")
        print("Time per packet ms: ", ms_delay / N)


if __name__ == "__main__":
    asyncio.run(main())
