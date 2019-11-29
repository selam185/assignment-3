"""
Module for the Client class
"""

import asyncio
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


class Client:
    """
    Class for client objects to connect to the server
    Either pass on the commands to server, or handle them itself
    """

    def __init__(self):
        self.command_list = []

    async def client(self, address, port):
        """
        The main client function, sets up the connection and handles inputs in a while loop
        """
        # Assert that address only contains numbers and period marks, as IP address should
        for char in address:
            assert (char.isnumeric() or char == "."),   \
                "IP-address contains invalid character"
        # Assert that port is in not among the low values required for other services,
        # and also within range of unsigned int
        assert 1023 < port < 65535, "Port out of range"

        # Create the connection to the server
        reader, writer = await asyncio.open_connection(
            address, port)
        assert isinstance(reader, asyncio.streams.StreamReader), \
            "Asyncio StreamReader on server is not working"
        assert isinstance(writer, asyncio.streams.StreamWriter), \
            "Asyncio StreamWriter on server is not working"

        print("\n Use commands register or login to access the server")

        while True:
            command = input('\nClient waiting\n')
            # strip command of whitespaces for exact matches in the if-statements
            command = command.strip()
            # Split commands on spaces to handle separate words, e.g. read_file filename
            split_command = command.split()
            if len(split_command) == 0:
                continue
            # Append the command to command history
            self.command_list.append(command)

            if command == 'quit':
                # Send quit command to the server
                # Logout the user in case they had logged in on this client
                writer.write(command.encode())
                data = await reader.read(10000)
                print(f'\nReceived:\n{data.decode()}')
                # Close the connection unilaterally
                # Regardless of whether a user was logged in on this client or not
                print('Close the connection')
                writer.close()
                break

            if command == 'commands':
                print("\nList of all available commands")
                commands = """
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

            # If the command was 'commands', but also had some option
            if split_command[0] == "commands":
                if split_command[1] == "issued":
                    print("\nHistory of commands issued:")
                    for cmd in self.command_list:
                        print(cmd)
                if split_command[1] == "clear":
                    self.command_list = []
                    print("\nCommand history cleared")
                continue

            print(f'Send: {command}')
            writer.write(command.encode())

            data = await reader.read(10000)
            print(f'\nReceived:\n{data.decode()}')


if __name__ == "__main__":
    client = Client()
    asyncio.run(client.client('127.0.0.1', 8080))
