# python3 server.py <port>

import asyncio
import signal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
from logging2.logging2 import *


running = True


async def handle_conn(reader, writer):
    seq = 0
    addr = writer.get_extra_info('peername')
    INFO(f'accepting connection from {addr}')

    while running:
        seq += 1

        try:
            writer.write(f'hello client {seq}\n'.encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100),
                                          timeout=0.01)

            if data:
                print(f'{data.decode()}', end='')

        except asyncio.TimeoutError as e:
            # INFO(f'{e}')
            continue
        except ConnectionResetError as e:
            INFO(f'{e}')
            break
        except BrokenPipeError as e:
            INFO(f'{e}')
            break
        except KeyboardInterrupt as e:
            INFO(f'{e}')
            break
        except RuntimeError as e:
            INFO(f'{e}')
            break

        # await asyncio.sleep(1) # test only

    writer.close()


async def main():
    port = sys.argv[1]
    server = await asyncio.start_server(handle_conn, '', port)

    addrs = ', '.join(str(sock.getsockname())
                      for sock in server.sockets)
    INFO(f'serving on {addrs}')

    async with server:
        await server.serve_forever()


def handle_sigint(signum, frame):
    global running
    running = False

    for task in asyncio.all_tasks():
        task.cancel()

    asyncio.get_event_loop().stop()
    signal.default_int_handler(signum, frame)


try:
    logging2_init()
    signal.signal(signal.SIGINT, handle_sigint)
    asyncio.run(main())
except RuntimeError as e:
    INFO(f'{e}')
    pass
except KeyboardInterrupt as e:
    INFO(f'{e}')
    pass

