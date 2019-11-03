"""
    This file contains the tests given for assignment3.
    The following unit tests are conducted on the class User.
"""
import unittest
import os
import server
import pickle
import classfile

ROOT_PATH = os.getcwd()
server.Server()

class ConnectionTest(unittest.TestCase):
    """ Handles test cases for all functions in class file """

    def test_repr(self):
        """ Sample test to print the usr name"""

        usr = classfile.User("name", "password", "user")
        expected_result = "name"
        result = str(usr)

        self.assertEqual(result, expected_result)

    def test_register_and_login(self):
        """ Testing to register the user successfully and then logging in.
         """

        os.chdir(ROOT_PATH)
        svr = server.Server()
        expected_result = ["User registered sucessfully", "Username already exists"]
        result = []

        result.append(svr.register('temp', 'pwd', 'user')[:27])
        result.append(svr.register('temp', 'pwd', 'user')[:27])
        
        expected_login_result = "temp: login successful"
        login_result = (svr.login('temp', 'pwd', 'tcp port')[:22])
        
        # remove the user before next test
        with open('reg.pickle', 'rb') as userlist_file:
            userlist = pickle.load(userlist_file)
        try:
            os.removedirs(os.path.join("Users", 'temp'))
        except FileNotFoundError:
            os.removedirs(os.path.join("Admins", 'temp'))
        # Remove the user from the pickle file by overwriting it with an updated list
        new_userlist = []
        for user in userlist:
            if user.username != 'temp':
                new_userlist.append(user)
        userlist_file = open('reg.pickle', 'wb')
        pickle.dump(new_userlist, userlist_file)
        userlist_file.close()

        self.assertEqual(login_result, expected_login_result)
        self.assertEqual(result, expected_result)

    def test_change_dir(self):
        """testing to change directory, root and Users directory should already exists
                in under root path if not run the server script """
        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root")
        expected_result = "Current working directory "+ usr.current_path+"\\Users"
        result = usr.changedir("Users")
        os.chdir(ROOT_PATH)
        self.assertEqual(result, expected_result)

    def test_writefile(self):
        """ testing to write text in the file, root and Users directory should already exists
                in under root path if not run the server script """

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        expected_result = ["File test.txt Created", "File test.txt Updated"]
        result = []
        test_input = ['test.txt', 'test.txt']

        result.append(usr.writefile(test_input[0], 'testing'))
        result.append(usr.writefile(test_input[1], 'testing'))

        self.assertEqual(result, expected_result)
        os.remove('test.txt')
        os.chdir(ROOT_PATH)



    def test_create_dir(self):
        """testing to create directory, root and Users directory should already exists
            in under root path if not run the server script"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        expected_result = ["Directory created testing", "Directory already exists testing"]
        result = []
        test_input = ['testing', 'testing']

        result.append(usr.create_dir(test_input[0]))
        result.append(usr.create_dir(test_input[1]))

        self.assertEqual(result, expected_result)

        os.rmdir('testing')
        os.chdir(ROOT_PATH)

    def test_list_function(self):
        """testing to list the content of empty directory, root and Users directory
           should already exists  in under root path if not run the server script
           and placed test_folder in that path"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        usr.create_dir("test_folder")
        usr.current_path = os.path.join(usr.current_path, "test_folder")
        expected_result = "(This folder is empty)"
        result = usr.list_function()
        self.assertEqual(result, expected_result)
        os.chdir(ROOT_PATH)

    def test_read_noinput(self):
        """testing to readfile function if that user passed without name of the file,
           root and Users directory should already exists in under root path
           if not create that folder"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        usr.filename = "some_file.extension"
        expected_result = "some_file.extension has been closed"
        result = usr.read_noinput()
        self.assertEqual(result, expected_result)
        os.chdir(ROOT_PATH)

    def test_write_notext(self):
        """testing to writefile function if that user passed without text,
           root and Users directory should already exists in under root path
           if not create that folder"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        expected_result = "File test1.txt erased"
        result = usr.write_notext('test1.txt')
        self.assertEqual(result, expected_result)
        os.chdir(ROOT_PATH)

    def test_create_write(self):
        """testing to check create folder and write function as mentioned in classfile,
           root and Users directory should already exists in under root path
           if not create that folder"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        exp_result_c_folder = ["Directory created test_all"]
        exp_result_write = ["File testall.txt Created"]

        for exp_fold, exp_write, in zip(exp_result_c_folder, exp_result_write):
            self.assertEqual(usr.create_dir('test_all'), exp_fold)
            self.assertEqual(usr.writefile('testall.txt', 'helloworld'), exp_write)

        os.rmdir('test_all')
        os.remove('testall.txt')
        os.chdir(ROOT_PATH)

    def test_read_write(self):
        """testing to check read and write function as mentioned in classfile,
           root and Users directory should already exists in under root path
           if not create that folder"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        expected_result_write = "File testread.txt Created"
        expected_result_read = "Content of line in reading file: \n\n" + "hello" + "\n\n"

        # for exp_write, exp_read in zip(expected_result_write, expected_result_read):
        self.assertEqual(usr.writefile('testread.txt', 'hello'), expected_result_write)
        self.assertEqual((usr.readfile('testread.txt')), expected_result_read)

        os.remove('testread.txt')
        os.chdir(ROOT_PATH)

    def test_emptyreadfile(self):
        """testing to check read function to read the empty file,it should denied request.
           root and Users directory should already exists in under root path
           if not create that folder"""

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users")
        expected_result = "Request denied"
        result = usr.readfile("invalid.txt")
        os.chdir(ROOT_PATH)
        self.assertEqual(result, expected_result)

    def test_change_prevdir(self):
        """testing to change directory to walk back previous folder, root and Users directory
             should already exists in under root path if not create that folder """

        usr = classfile.User("name", "password", "user")
        usr.current_path = os.path.join(ROOT_PATH, "root", "Users", "name")
        expected_result = "User is not allowed to leave the home folder"
        result = usr.changedir("..")
        os.chdir(ROOT_PATH)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
