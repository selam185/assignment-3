
# change_folder and list
import os
import time

# name, size, date and time of creation, in an easy-to-read manner

print(os.listdir(os.getcwd()))
ls = os.listdir(os.getcwd())
for f in ls:
    f_name = os.path.basename(os.getcwd() + '\\' + f)
    print(f_name, end=(30 - len(f_name)) * ' ')

    f_size = os.path.getsize(os.getcwd() + '\\' + f)
    print(f_size, end=(10 - len(str(f_size))) * ' ')

    print(time.ctime(os.path.getctime(os.getcwd() + '\\' + f)), end='\n')


# print(os.getcwd())
# os.chdir("..")
# print(os.getcwd())
# os.chdir("..")
# print(os.getcwd())
# print(os.listdir(os.getcwd()))
