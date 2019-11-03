import os
import time
import  pickle
import os.path


class User:
    def __init__(self, username, password, privileges):
        self.username = username
        self.password = password
        self.privilege = privileges
        self.filename = ""
        self.index = 0
        self.current_path = ""


    def __repr__(self):
        return self.username

    # def __setusername__(self):
    #     try:
    #         with open('reg.pickle', 'rb') as f:
    #             userlist = pickle.load(f)
    #     except:
    #         userlist = []
    #     if self.username in [User.username for User in userlist]:
    #         if self.password in [User.password for User in userlist]:
    #             return self.username
    #     else:
    #         return "User doesn't exists"

    # def __getusername__(self,username):
    #     return self.username
        
        
    # def __setpath__(self,absolute_path):
    #     try:
    #         if os.path.exists("root"):
    #             self.absolute_path = os.path.abspath("root")
    #         else:
    #             os.mkdir("root")
    #             self.absolute_path = os.path.abspath("root")
    #             print(absolute_path)
    #     except OSError:
    #         print("Request denied")
        

    # def __getpath__(self):
    #     return self.absolute_path

    def read_noinput(self):
        # read file without filename
        temp = self.filename
        self.filename = ""
        self.index = 0
        return "file has been closed "+ temp


    def readfile(self, filename):
        # move to the user's current location
        os.chdir(self.current_path)
        # open file to read    
        try:
            if self.filename:
                f = open(self.filename, 'r')
                result = f.read(self.index + 10)
                result = result[self.index :]
                if len(result) < 10:
                    self.index = -10
                f.close()
                self.index = self.index + 10
            else:
                self.filename = filename
                f = open(self.filename, 'r')
                result = f.read(10)
                f.close()             
                self.index = 10                  
            return "Content of line in reading file: \n\n" +result+"\n"

        except OSError:
            print("Request denied")
            return "Request denied"

    
    def write_notext(self, filename):
        # move to the user's current location
        os.chdir(self.current_path)

        # open file to erase the content
        
        f = open(filename, 'w')
        f.close()
        result = "File " + filename + " Erased"          
        print(result)
        return result       

    def writefile(self, filename, text):
        # move to the user's current location
        os.chdir(self.current_path)

        # open file to write to
        try:
            if os.path.isfile(filename):
                f = open(filename, 'a')
                f.write(text + "\n")
                f.close()
                result = "File " + filename + " Updated"
                return result
                
            elif not os.path.isfile(filename):            
                f = open(filename, 'w')
                f.write(text + "\n")
                f.close()
                result = "File " + filename + " Created"
                return result

        except FileNotFoundError:
            print("Request denied")
            return "Request denied"

        

    def create_dir(self, folder_name):
        try:
            os.chdir(self.current_path)
            os.mkdir(folder_name)
            result = "Directory created " + folder_name
            print(result)
        except FileExistsError:
            result = "Directory already exists " + folder_name
            print(result)
        return result

    # add limitation, only inside their own home folder
    def changedir(self, dir_name):
        print("Current Working Directory " , os.getcwd())
        try:
            if dir_name == '..':
                # check not leaving home-folder for user, allowed only for admin
                if self.privilege == "user" and os.path.basename(self.current_path) == self.username:
                    result = "User is not allowed to leave the home folder"
                    print(result)
                    return result
                if self.privilege == "admin" and os.path.basename(self.current_path) == "root":
                    result= "It's not allowed to leave the root directory"
                    return result
             
                os.chdir(self.current_path)
                os.chdir('..')
                self.current_path = os.getcwd()
                print("Moved to outer folder", self.current_path)
            else:
                os.chdir(self.current_path)
                os.chdir(dir_name)
                self.current_path = os.getcwd()
                print("Moved to folder", self.current_path)

            return "Current working directory " + self.current_path

        except FileNotFoundError:
            print("Folder not found")
            return "Folder not found"
        
    def list_function(self):
        os.chdir(self.current_path)
        ls = os.listdir(os.getcwd())
        return_string = ""

        if len(ls):
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
        else:
            return_string = "(This folder is empty)"

        return return_string

class Admin(User):
    def delete(self, username, password, root_path):
        os.chdir(root_path)
        try:
            with open('reg.pickle', 'rb') as f:
                userlist = pickle.load(f)
        except FileNotFoundError:
            return "No users are registered yet/File not found"

        if self.privilege== "admin":
            if self.password == password:
                if username in [User.username for User in userlist]:
                    # Remove the users home directory
                    try:
                        os.removedirs(os.path.join("Users", username))
                    except FileNotFoundError:
                        os.removedirs(os.path.join("Admins", username))
                    # Remove the user from the pickle file
                    new_userlist = []
                    for user in userlist:
                        if user.username != username:
                            new_userlist.append(user)
                    f = open ('reg.pickle', 'wb')
                    pickle.dump(new_userlist, f)
                    result = f"{username} has been deleted"
                    print(result)
                    return result
                else:
                    result = f"{username} does not exist"
                    print(result)
                    return result
            else:
                result = f"Incorrect password for admin {self.username}"
                print(result)
                return result
        else:
            result = "Privilege must be Admin"
            print(result)
            return result

