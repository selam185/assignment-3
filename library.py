import asyncio
import os
import time
import signal
import pickle
from collections import namedtuple

signal.signal(signal.SIGINT, signal.SIG_DFL)

User = namedtuple('User', 'username password privileges')

logged_in = {}


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

    return_string += str(logged_in)
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

def register(username, password, privileges, path):
    if not (privileges == "admin" or privileges == "user"):
        return "Privileges must be either 'user' or 'admin'."
    try:
        with open('reg.pickle', 'rb') as f:
            userlist = pickle.load(f)
    except:
        userlist = []

    new_user = User(username, password, privileges)

    
    if new_user.username not in [User.username for User in userlist]:
        userlist.append(new_user)
        pickle.dump(userlist, open("reg.pickle", "wb"))
        #os
        print("Register successfully")
        changeDir("root")
        #path1 = "root"
        path3 = username
        if privileges == "admin":
            path2 = "Admins"
            os.makedirs(os.path.join(path2, path3))
        elif privileges == "user":
            path2 = "users"
            os.makedirs(os.path.join(path2,path3))
      
        #old_path = os.getcwd()
        #os.chdir(path)
        #os.mkdir(username)
        #os.chdir(old_path)
        result = "User registered Sucessfully and Directory " + username + " created"
        return result

    else:  
        print("the username is already exits. Please enter valid")
        return "Username already exists" 
    return userlist


def login(username, password, ip_tcp):
    result = os.getcwd()
    path = os.path.basename(os.path.normpath(result))
    if path == ("Admins"):
        print ("yea")
        changeDir('..')
        changeDir('..')
    if path == ("users"):
        changeDir('..')
        changeDir('..')
     
    try:
        with open('reg.pickle', 'rb') as f:
            userlist = pickle.load(f)
        
    except:
        userlist = []
    print("userlist")

    global logged_in
    for user in userlist:    
        if user.privileges == "admin":
            result = os.getcwd()
            path = os.path.basename(os.path.normpath(result))
            changeDir("root")
            changeDir("Admins")
            print(user.privileges)
        if user.privileges == "user": 
            result = os.getcwd()
            path = os.path.basename(os.path.normpath(result))
            changeDir("root")
            changeDir("users")
            print(user.privileges)
    if username in [User.username for User in userlist]:
        if password in [User.password for User in userlist]:
            if username not in logged_in.keys():
                if ip_tcp not in logged_in.values():
                    print("login successfully")
                    logged_in.update( {username:ip_tcp} )
                    result = username + " Login Sucessfully"
                    return result
                else:
                    return "This port is already logged in with another username"
            else:
                return "User already logged in"
        else:
            return "Incorrect password"
    else:
        while username not in [User.username for User in userlist]:      
            print(" Please enter valid Username")
            return "Invalid username"
  

def delete(username,password):
    try:
        with open('reg.pickle', 'rb') as f:
            userlist = pickle.load(f)
  
    except:
        userlist = []

    if logged_in[username].privileges == "admin":
        if logged_in[username].password == password:
            if username in [User.username for USer in userlist]:
                new_userlist = []
                os.rmdir(username)
                remove = username
                for word in userlist:
                    if word != remove:
                        new_userlist += [word]
                f = open ('reg.pickle', 'w')
                pickle.dump(new_userlist, f)
                print("deleted")
                
            else:
                print("username does not exit")
        else:
            print("Incorrect password")
    else:
        print("access level is not admin")



