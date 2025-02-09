import asyncio

from eros.transport.websocket import WebsocketInterface
from eros.transport.udp import UDPInterface
from eros import ErosInterface
from device_api import DeviceInterface
import time


async def main():
    # async with UDPInterface("udp://192.168.1.181:1234", debug=True) as transport:
    async with WebsocketInterface("ws://192.168.1.181/ws", debug=True) as transport:
        eros = ErosInterface(transport, debug=True)
        await eros.start()
        interface = DeviceInterface.from_eros(eros, source_realm=5)
        start_time = time.time()
        N = 30
        tasks = []
        for i in range(N):
            tasks.append(interface.set_request({0x01040001: bytes([0x01, 0x02, 0x03, 0x04])}))
            
        await asyncio.gather(*tasks)
            
            
        ms_delay = (time.time() - start_time) * 1000
            
        print(f"Time taken ms: {ms_delay}")
        print("Time per packet ms: ", ms_delay / N)
        
        await asyncio.sleep(1)
        await eros.stop()


if __name__ == "__main__":
    asyncio.run(main())
