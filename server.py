


import asyncio
try:
    import library
except ModuleNotFoundError:
    import Assignment_3.library as library
import os
import classfile
import pickle

class Server:
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
        # The server should be at root to read reg.pickle
        os.chdir(self.absolute_path)
        if not (privileges == "admin" or privileges == "user"):
            return "Privileges must be either 'user' or 'admin'."
        try:
            with open('reg.pickle', 'rb') as f:
                userlist = pickle.load(f)
        # If no user accounts exist yet, create an empty list
        except FileNotFoundError:
            userlist = []

        new_user = classfile.User(username, password, privileges)


        if new_user.username not in [User.username for User in userlist]:
            userlist.append(new_user)
            pickle.dump(userlist, open("reg.pickle", "wb"))
            print("Register successfully")

            if privileges == "admin":
                group = "Admins"
                os.makedirs(os.path.join(group, username))
            elif privileges == "user":
                group = "Users"
                os.makedirs(os.path.join(group, username))
        
            result = "User registered sucessfully and folder " + username + " created in " + group
            return result

        else:  
            print("The username is already exits. Please enter valid")
            return "Username already exists" 


    def login(self, username, password, ip_tcp):
        os.chdir(self.absolute_path)
        try:
            with open('reg.pickle', 'rb') as f:
                userlist = pickle.load(f)
        except FileNotFoundError:
            return "No users are registered yet/File not found"

        
                
        # check if logged in already
        # not working bc elements in values are user objects, but username is a string
        # !!!!!!!!!!!!
        if username not in [user.username for user in self.logged_in.values()]:
            pass
        else:
            return "User already logged in on another port"

        # check if client already logged in
        if ip_tcp not in self.logged_in.keys():
            pass
        else:
            return "This port is already logged in with another username"

        # check if username exists
        if username in [User.username for User in userlist]:
            pass
        else:
            print(" Please enter valid Username")
            return "Invalid username"

        # save user object to variable
        for usr in userlist:
            if usr.username == username:
                user = usr
                break
        
        # compare password
        if password == user.password:
            print("Password correct")
        else:
            return "Incorrect password"


        print("login successful")

        # move to the users home folder
        group = user.privilege.capitalize() + "s"
        print("group is " + group)
        user.current_path = os.path.join(self.absolute_path, group, username)

        self.logged_in.update( {ip_tcp:user} )
        result = username + " Login Sucessfully"
        return result



    async def handle_commands(self, reader, writer):
        while True:
            data = await reader.read(10000)
            message = data.decode()
            addr = writer.get_extra_info('peername') 
            print(f"Received {message!r} from {addr!r}")

            split_message = message.split(' ')

            # identify the user object connected to the address
            try:
                user = self.logged_in[addr]
                print(user)
            except KeyError:
                print("User not yet logged in...\n...")

            if split_message[0] == 'change_folder':
                try:
                    writer.write(user.changedir(split_message[1]).encode())
                    await writer.drain()
                    os.chdir(self.absolute_path)
                    continue
                except IndexError:
                    error_msg = "change folder input should be in the form: 'change folder <name>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue

            if message == 'list':
                writer.write(user.list_function().encode())
                await writer.drain()
                os.chdir(self.absolute_path)
                continue

            if split_message[0] == 'read_file':
                try:
                    writer.write(user.readfile(split_message[1]).encode())
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
                    writer.write(user.writefile(split_message[1], split_message[2]).encode(encoding='utf-8'))
                    await writer.drain()
                    os.chdir(self.absolute_path)
                    continue
                except IndexError:
                    error_msg = "write_file input should be in the form: 'write_file <name> <input>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue

            if split_message[0] == 'create_folder':
                try:
                    writer.write(user.create_dir(split_message[1]).encode())
                    await writer.drain()
                    os.chdir(self.absolute_path)
                    continue
                except IndexError:
                    error_msg = "create folder input should be in the form: 'create_folder <name>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue
            
            if split_message[0] == 'delete':
                try:
                    writer.write(user.delete(split_message[1], split_message[2], self.absolute_path).encode())
                    await writer.drain()
                    continue
                except IndexError:
                    error_msg = "delete input should be in the form: 'register <username> <password>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue

            if split_message[0] == 'register':
                try:
                    writer.write(self.register(split_message[1], split_message[2], split_message[3]).encode())
                    await writer.drain()
                    continue
                except IndexError:
                    error_msg = "register input should be in the form: 'register <username> <password> <privilege>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue

            if split_message[0] == 'login':
                try:
                    writer.write(self.login(split_message[1], split_message[2], addr).encode())
                    await writer.drain()
                    continue
                except IndexError:
                    error_msg = "login input should be in the form: 'login <username> <password>'"
                    print(error_msg)
                    writer.write(error_msg.encode())
                    await writer.drain()
                    continue


            if message == 'quit':
                print(f"Logging out {self.logged_in[addr]}")
                writer.write(f"Logging out {self.logged_in[addr]}...".encode())
                del self.logged_in[addr]
                await writer.drain()
                continue


            writer.write("Invalid command".encode())
            await writer.drain()


    async def main(self):
        server = await asyncio.start_server(
        self.handle_commands, '127.0.0.1', 8080)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    new_server = Server()
    asyncio.run(new_server.main())

# asyncio.run(main())
