"""This Module contains the class User and Admin for client-server solution for file management."""

import os
import time
import pickle
import shutil


class User:
    """Class for user with a privilege User.

    Attributes:
    -----------------------------------------------------
    username : string
        name of the user used for registration.

    password : string
        password for the user

    privileges : string
        privileges must be either user or admin.

    filename : string
        name of the file used for read and write function.

    current_path : string
        location of current working directory.

    Methods:
    -------------------------------------------------------
    read_noinput :
        If the User request read file services without filename.
        It will close the file that open currently for reading.

    readfile :
        If the User request read file services with filename,
        this function will read data from the user specified file.
        At first time call, it will read first 100 characters and
        each subsequent calls from same user it will read next 100 characters. 

    write_notext :
        If the User request write file functionality without input data. It will
        erase the content of the filename that user specified in request.

    write_file :
        If the User request write function with filename and input data.It 
        will create new text file and updated with input data.If the User 
        calls this function second time with same filename and new input data.
        It will updated new input data in existing file not created new file.

    create_dir :
        This function is used to create new directory for user with . If the directory
        already exist it will throw error message.

    changedir :
        This function is used to change the path of directory. If User specifies input with ".."
        then it will moves to previous folder.But this happen only user needs to be inside
        their current working directory. They are not allowed to move back if they are in home.

    list_function :
        This function will list all the files and folders in the current working directory.

        """

    def __init__(self, username, password, privileges):
        """Initialize the User class"""
        self.username = username
        self.password = password
        self.privilege = privileges
        self.filename = ""
        self.index = 0
        self.current_path = ""

    def __repr__(self):
        return self.username

    def read_noinput(self):
        """ This function will close the file that the user already logged
        in and read some content of file and then user request this service
        with out filename. Before closing the file it will reset the index
        value to zero then only it will start read from the beginning when 
        next time this function calls.

        Parameters :
        ============
        temp : conatains the name of the file that is already opened.
        index : contains position of characters in the file.

        Return :
        =========
        String which shows message such that file is closed.

        """
        temp = self.filename
        self.filename = ""
        self.index = 0
        return temp + " has been closed"

    def readfile(self, filename):
        """This function will read data from the file <filename> in the
         current working directory.If the user request the service with
         file name at first time. It will start read first 100 characters
         and then second time call it will read next 100 characters and so on.
            
        Incase if the user already open one read file and later request
        service such as read another file then the file opened earlier
        will close and read data from new file.

        If length of file contains less than 100 characters then initialize
        the index value to zero and then read it from beginning of the file.

        If the user specified filename that does not exists then it means
        request denied.

        Parameters:
        ===========
        filename - name of the file that user specified.
        index   - contains position of characters in the read file.
        result  - contains 100 characters from read file.

        Return :
        =========
        String which displays 100 characters from the read file.
         """
        # move to the user's current location
        os.chdir(self.current_path)

        # open file to read
        try:
            # File is in the middle of being read
            if self.filename == filename:
                file_to_read = open(self.filename, 'r')
                result = file_to_read.read(self.index + 100)
                result = result[self.index:]
                if len(result) < 100:
                    self.index = -100
                file_to_read.close()
                self.index = self.index + 100
            # File is being read from the beginning
            else:
                self.filename = filename
                file_to_read = open(self.filename, 'r')
                result = file_to_read.read(100)
                file_to_read.close()
                self.index = 100
            return "Content of line in reading file: \n\n" + result+"\n"

        except OSError:
            print("Request denied")
            return "Request denied"

    def write_notext(self, filename):
        """ This function is used to write a file with no input data.
            It means it will erase the content in that file.It just
            empty the file not delete.

            Parameters:
            ===========
            filename - name of the file that user specified.
                    
            Return:
            =======
            String which display message such that file is erased.
        
        """
        # Move to the user's current location
        os.chdir(self.current_path)

        # Open file to erase the content
        file_to_erase = open(filename, 'w')
        file_to_erase.close()
        result = "File " + filename + " erased"
        print(result)
        return result

    def writefile(self, filename, text):
        """ This function is used to write the data in text file in
            the current working directory.If the User request this
            service for the first time, after login then the user
            specified filename is created and input data specified
            by user is updated in that file.

            If the User request this service to that file already exists,
            then whatever data given in the input it will append to that file.
            If we have any space inbetween character string it will take that
            character as it is. As we have split commands in the server,if 
            there is space it will split separately to that input data and
            pass text arguments as list to this function.This is the reason
            for using join command here to combine that user defined
            input data

            Parameters:
            ===========
            filename - name of the file that user specified.
                    
            Return:
            =======
            String which display message such that file is either created or updated.           
        
         """
        # Move to the user's current location
        os.chdir(self.current_path)
        input_data = ' '.join(text)

        # Open file to write to
        try:
            # Append to the file if it already exists
            if os.path.isfile(filename):
                file_to_append = open(filename, 'a')
                file_to_append.write(input_data + "\n")
                file_to_append.close()
                result = "File " + filename + " Updated"
                return result

            # Create the file if it doesn't exist
            file_to_write = open(filename, 'w')
            file_to_write.write(input_data + "\n")
            file_to_write.close()
            result = "File " + filename + " Created"
            return result

        except FileNotFoundError:
            result = "File not found"
            print(result)
            return result

    def create_dir(self, folder_name):
        """This function is used to create a new folder in the
            current working directory.If the folder already 
            exists then it will show FileExistsError.

            Parameters:
            ===========
            folder_name - name of the folder that user specified.
                    
            Return:
            =======
            String which display message such that folder is created.         
            
            """
        try:
            os.chdir(self.current_path)
            os.mkdir(folder_name)
            result = "Directory created " + folder_name
            print(result)
        except FileExistsError:
            result = "Directory already exists " + folder_name
            print(result)
        return result

    def changedir(self, dir_name):
        """ This function is used to move the current working directory
            to the specified folder.The User is not allowed to move back
            from home directory. They have ability to move inside their
            current directory.Admin is not allowed to move back from root directory.

            If the directory does not exists then it will display message
            such as directory not found.

            Parameters:
            ===========
            dir_name - name of the folder that user specified to move.
                    
            Return:
            =======
            String which display message such that folder is created.         
            
            """       
               
        print("Current Working Directory ", os.getcwd())
        try:
            if dir_name == '..':
                # Stop user from leaving their home folder
                if self.privilege == "user" and \
                        os.path.basename(self.current_path) == self.username:
                    result = "User is not allowed to leave the home folder"
                    print(result)
                    return result
                # Stop admin from leaving root
                if self.privilege == "admin" and os.path.basename(self.current_path) == "root":
                    result = "It's not allowed to leave the root directory"
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
        """This function is used to print all files and folders in the
            current working directory.If the folder is empty,
            then it will that message.

            Parameters:
            ===========
            list_of_files - list the files and folders in the
                            current working directory.
                    
            Return:
            =======
            String which display all files and folders in that
                directory with size and time.

            """
        os.chdir(self.current_path)
        list_of_files = os.listdir(os.getcwd())
        return_string = ""

        if list_of_files:
            for file_entry in list_of_files:
                f_name = os.path.basename(os.getcwd() + '\\' + file_entry)
                return_string += f_name + "\t"

                f_size = os.path.getsize(os.getcwd() + '\\' + file_entry)
                return_string += str(f_size) + "\t"

                f_time = time.ctime(os.path.getctime(
                    os.getcwd() + '\\' + file_entry))
                return_string += f_time + "\n"
        else:
            return_string = "(This folder is empty)"

        print(return_string)
        return return_string


class Admin(User):
    """This module is used to have class user with a privilage of Admin
       inherits attributes from the class user. Admin have the rights to
       delete the user with admin password.In case if user does not have
       admin privilege password and tries to delete user it will return
       error messages.

       After deleting the user, it will remove all directory for that user.

       Parameters:
       ===========
        username : string
        name of the user used for registration.

        password : string
        password for the user

        privileges : string
        privileges must be either user or admin.

        Method:
        =======
        delete - user with admin privilages have rights to delete user
                with admin password.if there is no user registered.
                It will throw error.First it will check password
                in pickle file, if it matches then it delete the
                user and remove home directory of that user and
                also updated pickle file.

    """
    def delete(self, username, password, root_path):
        """ Delete the user conforming currently logged in Admin's password.
            Parameters:
            ===========
                username : string
                name of the user used for registration.

                password : string
                password for the user

                privileges : string
                privileges must be either user or admin.
                    
            Return:
            =======
                String which display either user deleted or error message.
        """
        os.chdir(root_path)
        try:
            with open('reg.pickle', 'rb') as userlist_file:
                userlist = pickle.load(userlist_file)
        except FileNotFoundError:
            return "No users are registered yet/File not found"

        if self.privilege == "admin":
            if self.password == password:
                if username in [User.username for User in userlist]:
                    # Remove the user's home directory
                    try:
                        shutil.rmtree(os.path.join("Users", username))
                        
                    except FileNotFoundError:
                        shutil.rmtree(os.path.join("Admins", username))
                        
                    # Remove the user from the pickle file by overwriting it with an updated list
                    new_userlist = []
                    for user in userlist:
                        if user.username != username:
                            new_userlist.append(user)
                    userlist_file = open('reg.pickle', 'wb')
                    pickle.dump(new_userlist, userlist_file)
                    result = f"{username} has been deleted"
                    print(result)
                    return result
                # If no user object with that username exists, return error message
                result = f"{username} does not exist"
                print(result)
                return result
            # If the password is wrong, return error message
            result = f"Incorrect password for admin {self.username}"
            print(result)
            return result
        # If the user does not have admin privileges, actually it should not belong to
        # the Admin class and should not have any way of accessing this function...
        result = "Privilege must be Admin"
        print(result)
        return result
