def readfile(filename):
    
    result = len(open(filename,'r').read())
    return result

result = readfile('Newtext.txt')
assert result != 0, "readfile is empty"
print("The result", result)

def writefile(filename):
    
    f = open(filename,'w')
    result = f.write('selvi')
    f.close()
    return result

result = writefile('old.txt')
assert result != 0, "write file is empty"
print("The result", result)