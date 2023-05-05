# python3 client.py <ip> <port> <client_tag>

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
from logging2.logging2 import *


async def handle_conn(reader, writer, message):
    seq = 0

    while True:
        seq += 1

        try:
            writer.write(f'hello server from {message} {seq}\n'.encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100),
                                          timeout=0.01)
            if data:
                print(f'{data.decode()}', end='')

        except asyncio.TimeoutError as e:
            # INFO(f'{e}')
            continue
        except KeyboardInterrupt as e:
            INFO(f'{e}')
            break

        # await asyncio.sleep(1) # test only

    writer.close()


async def main():
    ip = sys.argv[1]
    port = sys.argv[2]
    tag = sys.argv[3]
    INFO(f'connecting to {ip}:{port}')

    reader, writer = await asyncio.open_connection(ip, port)
    await handle_conn(reader, writer, tag)


try:
    logging2_init()
    asyncio.run(main())
except KeyboardInterrupt as e:
    INFO(f'{e}')
    pass
except ConnectionResetError as e:
    INFO(f'{e}')
    pass
except ConnectionRefusedError as e:
    INFO(f'{e}')
    pass
except BrokenPipeError as e:
    INFO(f'{e}')
    pass
