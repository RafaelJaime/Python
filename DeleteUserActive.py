"""
version 1.0.1
control if exist active user
"""

#you can delete active user
def deleteActiveUsers(user,file):
    f = open(file,"r")
    output = []
    for line in f:
        if not user in line:
            output.append(line)
    f.close()
    #open again the file and write all
    f = open(file, 'w')
    f.writelines(output)
    f.close()

    #del all items
    output.clean();

