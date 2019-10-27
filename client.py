import asyncio
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection(
#         '127.0.0.1', 8888)

#     print(f'Send: {message!r}')
#     writer.write(message.encode())

#     data = await reader.read(10000)
#     print(f'Received: {data.decode()!r}')

#     print('Close the connection')
#     writer.close()

async def client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    while True:
        command = input('Client waiting\n')

        if command == 'quit':
            # logout from server
            # send message to logout the user corresponding to the client
            writer.write(command.encode())
            data = await reader.read(10000)
            print(f'Received: {data.decode()!r}')

            print('Close the connection')
            writer.close
            break

        if command == 'commands':
            print("List of all available commands")
            continue

        print(f'Send: {command!r}')
        writer.write(command.encode())

        data = await reader.read(10000)
        print(f'Received: {data.decode()}')

asyncio.run(client())

