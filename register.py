import pickle
import os
import asyncio
from collections import namedtuple

User = namedtuple('User', 'username password privileges')

def reg():
    try:
        with open('reg.pickle', 'rb') as f:
            userlist = pickle.load(f)
    except:
        userlist = []

    username = input("username")
    password = input("password")
    privileges = input("privileges")
    
    new_user = User(username, password, privileges)

    if new_user.username not in [User.username for User in userlist]:
        userlist.append(new_user)
        pickle.dump(userlist, open("reg.pickle", "wb"))
        print("Register successfully")
        os.mkdir(username)
        result = "User registered Sucessfully and Directory " + username + " created"
        return result

    else:  
        print("the username is already exits. Please enter valid")
        return "Username already exists" 

reg()