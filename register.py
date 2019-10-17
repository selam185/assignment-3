import pickle

try:
    with open('users.pickle', 'rb') as f:
        users = pickle.load(f)
        userlist = users
        
except:
    users = None
    userlist = {}

username =  input("Enter a user name  ")
if username not in userlist.keys():
    password = input("Enter a password  ")
    userlist[username] = password
    pickle.dump( userlist, open( "users.pickle", "wb" ) )
    user = pickle.load( open( "users.pickle", "rb" ) )
    print("sign-up successfully")
    
else:
    while username in userlist.keys():       
        print("the username is taken. Try another")
        username = input("Enter a username  ")
        if username not in userlist.keys():
            password = input("Enter a password  ")
            userlist[username] = password
            pickle.dump( userlist, open( "users.pickle", "wb" ) )
            user = pickle.load( open( "users.pickle", "rb" ) )
            print("sign-up successfully")
            break


