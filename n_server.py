# import socket
# import sys

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('127.0.0.1', 8880)
# sock.bind(server_address)
# sock.listen(2)

# while True:
#     # Wait for a connection
#     connection, client_address = sock.accept()
#     buffer = connection.recv(64)
#     if len(buffer) > 0:
#         #print(buffer)
#         print(bytes.decode(buffer))
#         break

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

def createDir(dir_name):

    try:
        os.mkdir(dir_name)
        result = "Directory " + dir_name + " created"
        print(result)
    except FileExistsError:
        result = "Directory " + dir_name + " already exists"
        print(result)
    return result

def changeDir():
     
    print("Current Working Directory " , os.getcwd())  
    try:
        # Change the current working Directory    
        os.chdir("..")
        print("Directory changed")
    except OSError:
        print("Can't change the Current Working Directory")
    print("Current Working Directory " , os.getcwd())
    temp = os.getcwd()
    return temp

def writefile():

    f = open('newfile.txt', 'w')
    f.write("Hello World!!")
    f.close()
    return f
    # print("This is write file")

    # with open('newfile.txt', 'w') as writefile:
    #     writefile.write('Hello world!!This is Selvi')
    #     writefile.close()
    #     wr_file = ("File created successfully")
    #     return wr_file

def readfile():

    f = open('newfile.txt', 'r')
    for line in f:
    #f.read()
        print(line)
        return line

    # with open('newfile.txt', 'r') as readfile:
    #     for line in readfile:
    #         #print(line)
    #         return line
    #     readfile.close()

async def handle_commands(reader, writer):
    data = await reader.read(10000)
    message = data.decode()
    addr = writer.get_extra_info('peername') 
    print(f"Received {message!r} from {addr!r}")

    split_message = message.split(' ')

    if message == 'list':
        llist()
        writer.write(llist().encode())
        await writer.drain()

    if message == 'readfile':
        readfile()
        writer.write(readfile().encode())
        await writer.drain()

    if message == 'writefile':
        writefile()
        writer.write(writefile().encode())
        await writer.drain()
        
    if message == 'change directory':
        #changeDir()
        writer.write(changeDir().encode())
        await writer.drain()

    if split_message[0] == 'create' and split_message[1] == 'directory':
        writer.write(createDir(split_message[2]).encode())
        await writer.drain()

    # if message == 'create directory ':
    #     #createDir()
    #     writer.write(createDir().encode())
    #     await writer.drain()

    
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
#changeDir()
#writefile()
#readfile()
