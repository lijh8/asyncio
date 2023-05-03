# https://docs.python.org/3/library/asyncio-stream.html

import asyncio
import sys

async def continuous_communication(reader, writer, message):
    seq = 0
    while True:
        try:
            seq += 1
            writer.write(f"hello server from {message} {seq}".encode())
            await writer.drain()

            data = await reader.read(100)
            if data:
                print(f'{data.decode()}')

            await asyncio.sleep(1) # test only
        except asyncio.exceptions.CancelledError:
            break
        except (ConnectionResetError):
            break

async def main():
    tag = sys.argv[1]
    ip = "192.168.1.31"
    port = 8888
    print(f"connecting to {ip}:{port}")

    try:
        reader, writer = await asyncio.open_connection(ip, port)
        await continuous_communication(reader, writer, tag)
    except ConnectionRefusedError:
        pass
    except KeyboardInterrupt:
        pass

asyncio.run(main())
