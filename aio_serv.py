import asyncio
import os
import time

def llist():
    print(os.listdir(os.getcwd()))
    ls = os.listdir(os.getcwd())
    return_string = ""
    for f in ls:
        f_name = os.path.basename(os.getcwd() + '\\' + f)
        print(f_name, end=(30 - len(f_name)) * ' ')
        return_string += f_name + "\t"

        f_size = os.path.getsize(os.getcwd() + '\\' + f)
        print(f_size, end=(10 - len(str(f_size))) * ' ')
        return_string += str(f_size) + "\t"

        f_time = time.ctime(os.path.getctime(os.getcwd() + '\\' + f))
        print(f_time, end='\n')
        return_string += f_time + "\n"
    return return_string

# async def handle_echo(reader, writer):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')

#     print(f"Received {message!r} from {addr!r}")

#     print(f"Send: {message!r}")
#     writer.write(data)
#     await writer.drain()

#     print("Close the connection")
#     writer.close()


async def handle_commands(reader, writer):
    data = await reader.read(10000)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    if message == 'list':
        llist()
        # llist function must return a long string instead of printing
        # then encode and send back to client
        writer.write(llist().encode())
        await writer.drain()

    "change directory test"

    # print(f"Send: {message!r}")
    # writer.write(data)
    # await writer.drain()

    # print("Close the connection")
    # writer.close()

async def main():
    server = await asyncio.start_server(
        handle_commands, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())