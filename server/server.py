# https://docs.python.org/3/library/asyncio-stream.html

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging2.logging2 import *

async def connect_cb(reader, writer):
    addr = writer.get_extra_info('peername')
    INFO(f"accepting connection from {addr}")

    seq = 0
    while True:
        try:
            seq += 1
            writer.write(f"hello client {seq}".encode())
            await writer.drain()

            data = await asyncio.wait_for(reader.read(100), timeout=0.1)
            if data:
                INFO(f"{data.decode()}")
        except asyncio.exceptions.CancelledError as e:
            # INFO(f"Error: {e}")
            break
        except asyncio.exceptions.IncompleteReadError as e:
            # INFO(f"Error: {e}")
            break
        except asyncio.TimeoutError as e:
            # INFO(f"Error: {e}")
            continue
        except ConnectionResetError as e:
            # INFO(f"Error: {e}")
            break
        except BrokenPipeError as e:
            # INFO(f"Error: {e}")
            break
        except KeyboardInterrupt as e:
            # INFO(f"Error: {e}")
            break
        except Exception as e:
            INFO(f"Error: {e}")
            break

async def main():
    server = await asyncio.start_server(
        connect_cb, '192.168.1.31', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    INFO(f'serving on {addrs}')

    try:
        async with server:
            await server.serve_forever()
    except asyncio.exceptions.CancelledError as e:
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


try:
    logging2_init()
    asyncio.run(main())
except KeyboardInterrupt as e:
    # INFO(f"Error: {e}")
    pass
except Exception as e:
    INFO(f"Error: {e}")
    pass
