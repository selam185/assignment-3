


import asyncio
import library

# import os
# import time
# import signal
# import pickle
# from collections import namedtuple

# signal.signal(signal.SIGINT, signal.SIG_DFL)

# User = namedtuple('User', 'username password privileges')

# logged_in = {}


# def llist():

#     print(os.listdir(os.getcwd()))
#     ls = os.listdir(os.getcwd())
#     return_string = ""

#     for f in ls:
#         f_name = os.path.basename(os.getcwd() + '\\' + f)
#         print(f_name, end=(30 - len(f_name)) * ' ')
#         return_string += f_name + "\t"

#         f_size = os.path.getsize(os.getcwd() + '\\' + f)
#         print(f_size, end=(10 - len(str(f_size))) * ' ')
#         return_string += str(f_size) + "\t"

#         f_time = time.ctime(os.path.getctime(os.getcwd() + '\\' + f))
#         print(f_time, end='\n')
#         return_string += f_time + "\n"

#     return_string += str(logged_in)
#     return return_string

# def createDir(dir_name):

#     try:
#         os.mkdir(dir_name)
#         result = "Directory " + dir_name + " created"
#         print(result)
#     except FileExistsError:
#         result = "Directory " + dir_name + " already exists"
#         print(result)

#     return result

# def changeDir(name):
    
#     print("Current Working Directory " , os.getcwd())

#     try:
#         if name == '..':
#             os.chdir('..')
#             print("previous directory changed", os.getcwd())
#         else:
#             os.chdir(name)
#             print("inside directory changed", os.getcwd())

#         print("Current Working Directory " , os.getcwd())
#         result = os.getcwd()
#         return "Current working directory " + result
    
#     except OSError:
#         print("Request denied")
#         return "Request denied"

    

# def writefile(name, text):

#     f = open(name, 'w')
#     f.write(text)
#     #f.write("This is Assignment3 related to file handling.")
#     f.close()
#     result = "File " + name + " created"
#     return result
    
# def readfile(name):

#     try:
#         f = open(name, 'r')
#         for char in f:
#             result = (char[:100])
#             print(result)
#             f.close()
#             return "file reading:    " + result
#     except OSError:
#         print("Request denied")
#         return "Request denied"

# def register(username, password, privileges):
#     # if privileges != "admin" or privileges != "user":
#     #     return "Privileges must be either 'user' or 'admin'."
#     try:
#         with open('reg.pickle', 'rb') as f:
#             userlist = pickle.load(f)
#     except:
#         userlist = []

#     new_user = User(username, password, privileges)

    
#     if new_user.username not in [User.username for User in userlist]:
#         userlist.append(new_user)
#         pickle.dump(userlist, open("reg.pickle", "wb"))
#         print("Register successfully")
#         os.mkdir(username)
#         result = "User registered Sucessfully and Directory " + username + " created"
#         return result

#     else:  
#         print("the username is already exits. Please enter valid")
#         return "Username already exists" 


# def login(username, password, ip_tcp):
#     try:
#         with open('reg.pickle', 'rb') as f:
#             userlist = pickle.load(f)
        
#     except:
#         userlist = []

#     global logged_in

#     if username in [User.username for User in userlist]:
#         if password in [User.password for User in userlist]:
#             if username not in logged_in.keys():
#                 print("login successfully")
#                 changeDir(username)
#                 logged_in[username] = ip_tcp
#                 result = username + " Login Sucessfully"
#                 return result
#             else:
#                 return "User already logged in"
#         else:
#             return "Incorrect password"
#     else:
#         while username not in [User.username for User in userlist]:      
#             print(" Please enter valid Username")
#             return "Invalid username"


async def handle_commands(reader, writer):
    while True:
        data = await reader.read(10000)
        message = data.decode()
        addr = writer.get_extra_info('peername') 
        print(f"Received {message!r} from {addr!r}")

        split_message = message.split(' ')

        if split_message[0] == 'register':
            #register(split_message[1], split_message[2])
            writer.write(library.register(split_message[1], split_message[2], split_message[3]).encode())
            await writer.drain()
            continue

        if split_message[0] == 'login':
            #login(split_message[1], split_message[2])
            writer.write(library.login(split_message[1], split_message[2], addr).encode())
            await writer.drain()
            continue

        if message == 'list':
            library.llist()
            writer.write(library.llist().encode())
            await writer.drain()
            continue

        if message == 'quit':
            for usr, tcp in library.logged_in.items():
                if tcp == addr:
                    user = usr
            del library.logged_in[user]
            print("Logged out")
            writer.write("Logging out...".encode())
            await writer.drain()
            continue

        if split_message[0] == 'readfile':
            library.readfile(split_message[1])
            writer.write(library.readfile(split_message[1]).encode())
            await writer.drain()
            continue

        if split_message[0] == 'writefile':
            library.writefile(split_message[1], split_message[2])
            writer.write(library.writefile(split_message[1], split_message[2]).encode(encoding='utf-8'))
            await writer.drain()
            continue

        if split_message[0] == 'change' and split_message[1] == 'directory':
            writer.write(library.changeDir(split_message[2]).encode())
            await writer.drain()
            continue
            
        if split_message[0] == 'create' and split_message[1] == 'directory':
            writer.write(library.createDir(split_message[2]).encode())
            await writer.drain()
            continue

        writer.write("Invalid command".encode())
        await writer.drain()


async def main():
    server = await asyncio.start_server(
        handle_commands, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
