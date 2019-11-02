
import unittest
import threading
import asyncio
import time

import server
import client
import classfile


# c = client.Client()
# asyncio.run(c.client('127.0.0.1', 8080))
class ConnectionTest(unittest.TestCase):

    def test_repr(self):
        usr = classfile.User("name", "password", "user")

        expected_result = "name"
        result = ""

        result = str(usr)

        self.assertEqual(result, expected_result)

    def test_readfile(self):
        usr = classfile.User("name", "password", "user")
        usr.current_path = "C:\\Coding\\Python_New_projects\\Assignment_3"

        expected_result = "Content "
        result = ""

        result = usr.readfile("register.py")
        result = result[:8]

        self.assertEqual(result, expected_result)

    def test_writefile(self):
        usr = classfile.User("name", "password", "user")
        usr.current_path = "C:\\Coding\\Python_New_projects\\Assignment_3"

        expected_result = "File test.txt Created"
        result = ""

        result = usr.writefile("test.txt", "aaaaaaaaaaaa")

        self.assertEqual(result, expected_result)



if __name__ == "__main__":
    unittest.main()




