# https://docs.python.org/3/library/asyncio-stream.html

# python3 client.py foo
# python3 client.py bar

import asyncio
import signal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging2.logging2 import *

async def read_write_cb(reader, writer, message):
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

        except asyncio.exceptions.CancelledError as e:
            # INFO(f"Error: {e}")
            break
        except asyncio.TimeoutError as e:
            # INFO(f"Error: {e}")
            continue
        except ConnectionResetError as e:
            # INFO(f"Error: {e}")
            break
        except KeyboardInterrupt as e:
            # INFO(f"Error: {e}")
            break
        except Exception as e:
            INFO(f"Error: {e}")
            break

async def main():
    tag = sys.argv[1]
    ip = "192.168.1.31"
    port = 8888
    INFO(f"connecting to {ip}:{port}")

    try:
        reader, writer = await asyncio.open_connection(ip, port)
        await read_write_cb(reader, writer, tag)
    except ConnectionRefusedError as e:
        # INFO(f"Error: {e}")
        sys.exit(1) # OK
        pass
    except KeyboardInterrupt as e:
        # INFO(f"Error: {e}")
        sys.exit(1) # OK
        pass
    except OSError as e:
        INFO(f"Error: {e}")
        sys.exit(1) # OK
        pass

def handle_sigpipe(*args):
    INFO(f"SIGPIPE")


try:
    signal.signal(signal.SIGPIPE, handle_sigpipe)
    logging2_init()
    asyncio.run(main())
except KeyboardInterrupt as e:
    # INFO(f"Error: {e}")
    pass
except Exception as e:
    INFO(f"Error: {e}")
    pass
