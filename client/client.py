# https://docs.python.org/3/library/asyncio-stream.html

# python3 client.py foo
# python3 client.py bar

import asyncio
import signal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging2.logging2 import *


async def read_write_func(reader, writer, message):
    seq = 0
    while True:
        try:
            seq += 1
            writer.write(f"hello server from {message} {seq}".encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100), timeout=0.1)
            if data:
                INFO(f'{data.decode()}')

            # await asyncio.sleep(1) # test only

        except asyncio.exceptions.IncompleteReadError as e:
            # INFO(f"Info: {e}")
            break
        except BrokenPipeError as e:
            # INFO(f"Info: {e}")
            break
        except ConnectionResetError as e:
            # INFO(f"Info: {e}")
            break
        except asyncio.exceptions.CancelledError as e:
            # INFO(f"Info: {e}")
            break
        except KeyboardInterrupt as e:
            # INFO(f"Info: {e}")
            break
        except asyncio.TimeoutError as e:
            # INFO(f"Info: {e}")
            continue
        except GeneratorExit as e:
            INFO(f"Info: {e}")
            break


async def main():
    tag = sys.argv[1]
    ip = "192.168.1.31"
    port = 8888
    INFO(f"connecting to {ip}:{port}")

    reader, writer = await asyncio.open_connection(ip, port)
    await read_write_func(reader, writer, tag)


def handle_sigpipe(*args):
    INFO(f"SIGPIPE handled")


try:
    signal.signal(signal.SIGPIPE, handle_sigpipe)
    logging2_init()
    asyncio.run(main())
except BaseException as e:
    INFO(f"Info: {e}")
    pass
