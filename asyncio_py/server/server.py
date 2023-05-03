# https://docs.python.org/3/library/asyncio-stream.html

import asyncio

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"accepting connection from {addr}")

    seq = 0
    while True:
        try:
            seq += 1
            writer.write(f"hello client {seq}".encode())
            await writer.drain()

            data = await reader.read(100)
            if data:
                print(f"{data.decode()}")

        except (ConnectionResetError):
            break
        except (BrokenPipeError):
            break
        except (asyncio.exceptions.CancelledError):
            break
        except asyncio.exceptions.IncompleteReadError:
            break

async def main():

    server = await asyncio.start_server(
        handle_echo, '192.168.1.31', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'serving on {addrs}')

    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        pass
    except asyncio.exceptions.CancelledError:
        pass

asyncio.run(main())
