"""Module for the User and Admin classes"""

import os
import time
import pickle


class User:
    """Class for user with a privilege User """

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
        """Reset the read function"""
        temp = self.filename
        self.filename = ""
        self.index = 0
        return temp + " has been closed"

    def readfile(self, filename):
        """Read data from the file <filename> in the current working directory"""
        # move to the user's current location
        os.chdir(self.current_path)

        # open file to read
        try:
            # File is in the middle of being read
            if self.filename:
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
        """Write a file with no content which will erase the file """
        # Move to the user's current location
        os.chdir(self.current_path)

        # Open file to erase the content
        file_to_erase = open(filename, 'w')
        file_to_erase.close()
        result = "File " + filename + " erased"
        print(result)
        return result

    def writefile(self, filename, text):
        """Write the data in the current working directory """
        # Move to the user's current location
        os.chdir(self.current_path)

        # Open file to write to
        try:
            # Append to the file if it already exists
            if os.path.isfile(filename):
                file_to_append = open(filename, 'a')
                file_to_append.write(text + "\n")
                file_to_append.close()
                result = "File " + filename + " Updated"
                return result

            # Create the file if it doesn't exist
            file_to_write = open(filename, 'w')
            file_to_write.write(text + "\n")
            file_to_write.close()
            result = "File " + filename + " Created"
            return result

        except FileNotFoundError:
            result = "File not found"
            print(result)
            return result

    def create_dir(self, folder_name):
        """Create a new folder in the current working directory"""
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
        """Move the current working directory to the specified folder."""
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
        """Print all files and folders in the current working directory"""
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
    """class for a user with a privillage of Admin
       inherits attributes from the class user
    """
    def delete(self, username, password, root_path):
        """Delete the user conforming currently logged in Admin's password"""
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
                        os.removedirs(os.path.join("Users", username))
                    except FileNotFoundError:
                        os.removedirs(os.path.join("Admins", username))
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
