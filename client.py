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
            # strip command of whitespaces for exact matches in the if-statements
            command = command.strip()
            self.command_list.append(command)
            split_command = command.split()

            if command == 'quit':
                # logout from server
                # send message to logout the user corresponding to this client
                writer.write(command.encode())
                data = await reader.read(10000)
                print(f'Received: {data.decode()!r}')

                print('Close the connection')
                writer.close
                break

            if command == 'commands':
                print("List of all available commands")
                commands="""
                    commands                                             Descriptions
                change_folder <name>                             Move the current working directory
                list                                             Print all files and folders in the current working directory
                read_file <name>                                 Read data from the file <name> in the current working director
                write_file <name> <input>                        Write the data in <input> to the end of the file <name> in 
                                                                    the current working directory
                create_folder <name>                            Create a new folder with the specified <name> in the current
                                                                    working directory 
                register <username> <password> <privileges>     Register a new user with the <privileges> to the server using
                                                                    the <username> and <password> 
                login <username> <password>                     Log in the user conforming with <username> and <password>
                delete <username> <password>                    Delete the user by conforming with admin password
                """
                print(commands)
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

