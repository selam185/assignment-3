import os
import time
# import reg.pickle from root

#import logged_in from library

logged_in = {}

class User:
    def __init__(self, username, password, privileges):
        self.username = username
        self.password = password
        self.privileges = privileges
        self.filename = ""
        self.index = 0
        self.current_path = ""


    def __repr__(self):
        return self.username
        # f'{self.username} is created successfully'

    def __setusername__(self):
        try:
            with open('reg.pickle', 'rb') as f:
                userlist = pickle.load(f)
        except:
            userlist = []
        if self.username in [User.username for User in userlist]:
            if self.password in [User.password for User in userlist]:
                return self.username
        else:
            return "User doesn't exists"

    def __getusername__(self,username):
        return self.username
        
        
    def __setpath__(self,absolute_path):
        try:
            if os.path.exists("root"):
                self.absolute_path = os.path.abspath("root")
            else:
                os.mkdir("root")
                self.absolute_path = os.path.abspath("root")
                print(absolute_path)
        except OSError:
            print("Request denied")
        

    def __getpath__(self):
        return self.absolute_path


    def readfile(self, filename):

        try:              
            if self.filename:
                f = open(self.filename, 'r')
                for char in f:
                    print("if")
                    result = char[self.index : self.index + 10]
                    self.index = self.index + 10
                    print(result)
                    return result
            else:
                self.filename = filename
                print(self.filename)
                f = open(self.filename, 'r')
                for char in f:
                    print("else")
                    result = char[0:10]
                    self.index = self.index + 10
                    #result = f.read(100)
                    print(result)         
                return "file reading:    " + result
                
        except OSError:
            print("Request denied")
            return "Request denied"

        # finally:
        #         f.close()


    def writefile(self, filename, text):
        try:              
            if self.filename:
                f = open(self.filename, 'a')
                f.write(text)
                f.close()
                result = "File " + self.filename + "updated"
                print(result)
            else:
                self.filename = filename
                print(self.filename)
                f = open(self.filename, 'w')
                f.write(text)
                f.close()
                result = "File " + self.filename + "Created"
                print(result)                      

            return result

        except OSError:
            print("Request denied")
            return "Request denied"

        finally:
                f.close()


    def create_dir(self, folder_name):
        try:        
            os.mkdir(folder_name)
            result = "Directory " + folder_name + " created"
            print(result)
        except FileExistsError:
            result = "Directory " + folder_name + " already exists"
            print(result)
        return result


    def changedir(self,dir_name):
        print("CHANGE FOLDER FUNCTION FROM CLASS")
        self.dir_name = dir_name
        print("Current Working Directory " , os.getcwd())
        try:
            if self.dir_name == '..':
                os.chdir('..')
                print("previous directory changed", os.getcwd())
            else:
                os.chdir(self.dir_name)
                print("inside directory changed", os.getcwd())

            print("Current Working Directory " , os.getcwd())
            result = os.getcwd()
            return "Current working directory " + result
        
        except OSError:
            print("Request denied")
            return "Request denied"
        

    def list(self):
        print("LIST FUNCTION FROM CLASS")
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
            print(return_string)

        return return_string

class Admin(User):
    def __init__(self, username, password, privileges):
        super().__init__(username, password, privileges)
        

    def __del__(self):
        self.privileges = "admin"
      
        if self.privileges:
            name = input("\n Please input the user name you want to delete :\n")
            username = self.__getusername__(name)
            if username == None:
                print ("The user does not exist")
            # else: self.userlist.remove(username)       
        else:
            print("\n Only administrators with full admin rights can remove \n")
        
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

    

#user = Admin('ss','sss','admin')
#user.__repr__()
#user.Admin('ss')
#user.createdir()
#user.changedir('telvi7')
#user.list()
# user=User('a','b','user')

#user.readfile("Newtext.txt")
#user.readfile("Newtext.txt")
# user.readfile("new.txt")

#user.writefile("new.txt", "hello")
#user.writefile("new.txt", "world")
