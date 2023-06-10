# python3 client.py <ip> <port> <client_tag>

import asyncio
import signal
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
            writer.write(f'hello from {message} {seq}\n'.encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100), timeout=0.1)
            if data:
                print(f'{data.decode()}', end='')

        except asyncio.TimeoutError as e:
            # INFO(f'{e}')
            continue
        except BaseException as e:
            INFO(f'{e}')
            break

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
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(main())
    shielded_task = asyncio.shield(task)
    loop.add_signal_handler(signal.SIGINT, lambda: shielded_task.cancel())
    loop.add_signal_handler(signal.SIGTERM, lambda: shielded_task.cancel())
    loop.run_until_complete(shielded_task)
except BaseException as e:
    INFO(f'{e}')
