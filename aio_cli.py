import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

# msg = input('Send message to server\n')
# asyncio.run(tcp_echo_client(msg))

async def client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    while True:
        command = input("Client waiting\n")

        if command == "quit":
            print('Close the connection')
            writer.close()
            break

        if command == "commands":
            # if check for options
            #   handle options
            # if no option:
            print("<list of all available commands>")
            continue


        print(f'Send: {command!r}')
        writer.write(command.encode())

        # response from server
        data = await reader.read(10000)
        print(f'Received: {data.decode()!r}')


asyncio.run(client())