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
class Client:
    def __init__(self):
        self.command_list = []

    async def client(self, address, port):
        reader, writer = await asyncio.open_connection(
           address, port)

        while True:
            command = input('Client waiting\n')
            self.command_list.append(command)
            split_command = command.split()

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
                print("Here we should add a long string explaning all of them... as in canvas")
                continue

            if split_command[0] == "commands":
                if split_command[1] == "issued":
                    print("History of commands issued:")
                    for cmd in self.command_list:
                        print(cmd)
                if split_command[1] == "clear":
                    self.command_list = []
                continue

            print(f'Send: {command!r}')
            writer.write(command.encode())

            data = await reader.read(10000)
            print(f'Received: {data.decode()}')

if __name__ == "__main__":
    client = Client()
    asyncio.run(client.client('127.0.0.1', 8080))

