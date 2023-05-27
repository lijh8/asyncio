# python3 server.py <port>

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
from logging2.logging2 import *

async def handle_conn(reader, writer):
    seq = 0
    addr = writer.get_extra_info('peername')
    INFO(f'accepting connection from {addr}')

    while True:
        seq += 1

        try:
            writer.write(f'hello client {seq}\n'.encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100), timeout=0.1)
            if data:
                print(f'{data.decode()}', end='')

        except asyncio.TimeoutError as e:
            INFO(f'{e}')
            continue
        except BaseException as e:
            INFO(f'{e}')
            break

    writer.close()

async def main():
    port = sys.argv[1]
    server = await asyncio.start_server(handle_conn, '', port)

    addrs = ', '.join(str(sock.getsockname())
                      for sock in server.sockets)
    INFO(f'serving on {addrs}')

    async with server:
        await server.serve_forever()

try:
    logging2_init()
    asyncio.run(main())

except asyncio.CancelledError as e:
    INFO(f'{e}')
except BaseException as e:
    INFO(f'{e}')
