"""
Module for the server class

Server which can be connected to by the client and handle its requests
"""

import asyncio
import os
import pickle

import classfile


class Server:
    """Class for Server objects to be connected to by"""

    def __init__(self):
        # find the absolute path
        if os.path.exists("root"):
            self.absolute_path = os.path.abspath("root")
            os.chdir("root")
        else:
            os.mkdir("root")
            self.absolute_path = os.path.abspath("root")
            os.chdir("root")
        print(self.absolute_path)
        # dictionary of logged in users if empty when server starts
        self.logged_in = {}

    def register(self, username, password, privileges):
        """Register a new user and create a corresponding object of class User or class Admin"""
        # The server should be at root to read reg.pickle
        os.chdir(self.absolute_path)

        if privileges not in ("admin", "user"):
            return "Privileges must be either 'user' or 'admin'."

        try:
            with open('reg.pickle', 'rb') as userlist_file:
                userlist = pickle.load(userlist_file)
        # If no user accounts exist yet, create an empty list
        except FileNotFoundError:
            userlist = []

        if privileges == "user":
            new_user = classfile.User(username, password, privileges)
        elif privileges == "admin":
            new_user = classfile.Admin(username, password, privileges)

        if new_user.username not in [User.username for User in userlist]:
            userlist.append(new_user)
            pickle.dump(userlist, open("reg.pickle", "wb"))

            if privileges == "admin":
                group = "Admins"
                os.makedirs(os.path.join(group, username))
            elif privileges == "user":
                group = "Users"
                os.makedirs(os.path.join(group, username))

            result = "User registered sucessfully and folder " + \
                username + " created in " + group
            print(result)
            return result

        # If the entered username clashes with an older one, return error message
        print("Username already exists")
        return "Username already exists"

    def login(self, username, password, ip_tcp):
        """Log in the user, and move them to their home folder"""
        # Server must be in root to access the pickle file
        os.chdir(self.absolute_path)
        with open('reg.pickle', 'rb') as userlist_file:
            userlist = pickle.load(userlist_file)

        # Check if client already logged in
        if ip_tcp in self.logged_in.keys():
            if username in [user.username for user in self.logged_in.values()]:
                return "This port is already logged in with the same username"
            return "This port is already logged in with another username"

        # Check if user already logged in
        if username not in [user.username for user in self.logged_in.values()]:
            pass
        else:
            return "User already logged in on another port"

        # Check if username exists
        if username in [User.username for User in userlist]:
            pass
        else:
            print("Please enter valid Username")
            return "Invalid username"

        # Save user object to variable for reference later in the function
        for usr in userlist:
            if usr.username == username:
                user = usr
                break

        # Compare password
        if password == user.password:
            print("Password correct")
        else:
            return "Incorrect password"

        print("login successful")

        # Move to the user's home folder
        group = user.privilege.capitalize() + "s"
        print("group is " + group)
        user.current_path = os.path.join(self.absolute_path, group, username)

        self.logged_in.update({ip_tcp: user})
        result = username + \
            f": login successful, moved to home directory root/{group}/{username}"
        return result

    async def handle_commands(self, reader, writer):
        """The main server function, with main loop."""

        assert isinstance(reader, asyncio.streams.StreamReader), \
            "Asyncio StreamReader on server is not working"
        assert isinstance(writer, asyncio.streams.StreamWriter), \
            "Asyncio StreamWriter on server is not working"
        while True:
            # The server awaits new messages from any clients
            data = await reader.read(10000)
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"Received {message!r} from {addr!r}")
            split_message = message.split(' ')

            # Assert that address only contains numbers and period marks, as IP address should
            for char in addr[0]:
                assert (char.isnumeric() or char == "."),   \
                    "IP-address contains invalid character"
            # Assert that port is in not among the low values required for other services,
            # and also within range of unsigned int
            assert 1023 < addr[1] < 65535, "Port out of range"

            # Identify the user object connected to the address
            try:
                user = self.logged_in[addr]
                print(f"{addr} corresponds to {user}")

                # If a user object has been identified, match up command to user functions
                if message == 'list':
                    writer.write(user.list_function().encode())
                    await writer.drain()
                    os.chdir(self.absolute_path)
                    continue

                if split_message[0] == 'change_folder':
                    try:
                        writer.write(user.changedir(split_message[1]).encode())
                        await writer.drain()
                        os.chdir(self.absolute_path)
                        continue
                    except IndexError:
                        error_msg = "change folder input should be in the form: " \
                            + "'change folder <name>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if split_message[0] == 'read_file':
                    try:
                        if len(split_message) == 2:
                            writer.write(user.readfile(
                                split_message[1]).encode())
                            await writer.drain()
                            os.chdir(self.absolute_path)
                            continue
                        else:
                            writer.write(user.read_noinput().encode())
                            await writer.drain()
                            os.chdir(self.absolute_path)
                            continue
                    except IndexError:
                        error_msg = "read_file input should be in the form: 'read_file <name>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if split_message[0] == 'write_file':
                    try:
                        if len(split_message) == 3:
                            writer.write(user.writefile(
                                split_message[1], split_message[2]).encode(encoding='utf-8'))
                            await writer.drain()
                            os.chdir(self.absolute_path)
                            continue
                        else:
                            writer.write(user.write_notext(
                                split_message[1]).encode())
                            await writer.drain()
                            os.chdir(self.absolute_path)
                            continue
                    except IndexError:
                        error_msg = "write_file input should be in the form: " + \
                            "'write_file <name> <input>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if split_message[0] == 'create_folder':
                    try:
                        writer.write(user.create_dir(
                            split_message[1]).encode())
                        await writer.drain()
                        os.chdir(self.absolute_path)
                        continue
                    except IndexError:
                        error_msg = "create folder input should be in the form: " + \
                            "'create_folder <name>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if split_message[0] == 'delete':
                    try:
                        try:
                            writer.write(user.delete(
                                split_message[1], split_message[2], self.absolute_path).encode())
                            await writer.drain()
                        except AttributeError:
                            result = "Only admins have access to the delete command"
                            print(result)
                            writer.write(result.encode())
                            await writer.drain()
                        continue
                    except IndexError:
                        error_msg = "delete input should be in the form: " + \
                            "'register <username> <password>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if message == 'quit':
                    print(f"Logging out {self.logged_in[addr]}")
                    writer.write(
                        f"Logging out {self.logged_in[addr]}...".encode())
                    del self.logged_in[addr]
                    await writer.drain()
                    continue

            # If the user has not yet logged in, proceed to commands which are valid before login
            except KeyError:
                print("User not yet logged in...\n...")

                if split_message[0] == 'register':
                    try:
                        writer.write(self.register(
                            split_message[1], split_message[2], split_message[3]).encode())
                        await writer.drain()
                        continue
                    except IndexError:
                        error_msg = "register input should be in the form: " + \
                            "'register <username> <password> <privilege>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if split_message[0] == 'login':
                    try:
                        writer.write(self.login(
                            split_message[1], split_message[2], addr).encode())
                        await writer.drain()
                        continue
                    except IndexError:
                        error_msg = "login input should be in the form: " + \
                            "'login <username> <password>'"
                        print(error_msg)
                        writer.write(error_msg.encode())
                        await writer.drain()
                        continue

                if message == 'quit':
                    print("Quitting")
                    writer.write("Quitting".encode())
                    await writer.drain()
                    continue

            writer.write("Invalid command. " +
                         "Check your spelling and check if you are logged in".encode())
            await writer.drain()

    async def main(self):
        """The start of the async server"""

        server = await asyncio.start_server(
            self.handle_commands, '127.0.0.1', 8080)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    new_server = Server()
    asyncio.run(new_server.main())
