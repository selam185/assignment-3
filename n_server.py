import asyncio
import os
import time
import signal
import pickle

signal.signal(signal.SIGINT, signal.SIG_DFL)



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

def createDir(dir_name):

    try:
        os.mkdir(dir_name)
        result = "Directory " + dir_name + " created"
        print(result)
    except FileExistsError:
        result = "Directory " + dir_name + " already exists"
        print(result)

    return result

def changeDir(name):
    
    print("Current Working Directory " , os.getcwd())

    try:
        if name == '..':
            os.chdir('..')
            print("previous directory changed", os.getcwd())
        else:
            os.chdir(name)
            print("inside directory changed", os.getcwd())

        print("Current Working Directory " , os.getcwd())
        result = os.getcwd()
        return "Current working directory " + result
    
    except OSError:
        print("Request denied")
        return "Request denied"

    

def writefile(name, text):

    f = open(name, 'w')
    f.write(text)
    #f.write("This is Assignment3 related to file handling.")
    f.close()
    result = "File " + name + " created"
    return result
    
def readfile(name):

    try:
        f = open(name, 'r')
        for char in f:
            result = (char[:100])
            print(result)
            f.close()
            return "file reading:    " + result
    except OSError:
        print("Request denied")
        return "Request denied"

def register(username, password):
    try:
        with open('reg.pickle', 'rb') as f:
            users = pickle.load(f)
            userlist = users      
    except:
        users = None
        userlist = {}

    
    if username not in userlist.keys():
        userlist[username] = password
        pickle.dump( userlist, open( "reg.pickle", "wb" ) )
        #user = pickle.load( open( "reg.pickle", "rb" ) )
        print("Register successfully")
        result = username + " registered Sucessfully"
        os.mkdir(username)
        result = "User registered Sucessfully and Directory " + username + " created"
        return result
    
    else:  
        print("the username is already exits. Please enter valid")
        return "Username already exists" 


def login(username, password):
    try:
        with open('reg.pickle', 'rb') as f:
            users = pickle.load(f)
            userlist = users
        
    except:
        users = None
        userlist = {}

    if username in userlist.keys():
        if password in userlist.values():
            print("login successfully")
            result = username + " Login Sucessfully"
            return result
        else:
            return "Incorrect password"

    else:
        while username not in userlist.keys():       
            print(" Please enter valid Username")
            return "Invalid username"


async def handle_commands(reader, writer):
    data = await reader.read(10000)
    message = data.decode()
    addr = writer.get_extra_info('peername') 
    print(f"Received {message!r} from {addr!r}")

    split_message = message.split(' ')

    if split_message[0] == 'register':
        #register(split_message[1], split_message[2])
        writer.write(register(split_message[1], split_message[2]).encode())
        await writer.drain()

    if split_message[0] == 'login':
        #login(split_message[1], split_message[2])
        writer.write(login(split_message[1], split_message[2]).encode())
        await writer.drain()

    if message == 'list':
        llist()
        writer.write(llist().encode())
        await writer.drain()

    if split_message[0] == 'readfile':
        readfile(split_message[1])
        writer.write(readfile(split_message[1]).encode())
        await writer.drain()

    if split_message[0] == 'writefile':
        writefile(split_message[1], split_message[2])
        writer.write(writefile(split_message[1], split_message[2]).encode(encoding='utf-8'))
        await writer.drain()

    if split_message[0] == 'change' and split_message[1] == 'directory':
        writer.write(changeDir(split_message[2]).encode())
        await writer.drain()
        
    if split_message[0] == 'create' and split_message[1] == 'directory':
        writer.write(createDir(split_message[2]).encode())
        await writer.drain()

async def main():
    server = await asyncio.start_server(
        handle_commands, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
