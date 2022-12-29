import os
import threading
import sys

filesInUse = []
root = os.getcwd()
global datdict
datdict = {}
lock = threading.Lock()
global clientInfo
clientInfo = {
    'message': ''
}
global writer
writer = {'username': ''}

def thread_function(a, username):

    a = a.strip()
    a = a.split(' ')
    if a[0] == 'create':
        createFile(a[1])
    elif a[0] == 'delete':
        deleteFile(a[1])
    elif a[0] == 'makeDir':
        makeDirectory(a[1])
    elif a[0] == 'changeDir':
        changeDirectory(a[1])
    if a[0] == 'open':
        a[1] = a[1].replace("<", "")
        a[1] = a[1].replace(">", "")
        a[1] = a[1].replace("\n", "")
        args = a[1].split(',')
        openFile(args[0], args[1])
    elif a[0] == 'read_from_file':
        a[1] = a[1].replace("<", "")
        a[1] = a[1].replace(">", "")
        a[1] = a[1].replace(",", "")
        a[1] = a[1].replace("\n", "")
        a[2] = a[2].replace(",", "")
        a[3] = a[3].replace("\n", "")
        openFile(a[1], 'x', '', a[2], a[3])
    elif a[0] == 'close':
        a[1] = a[1].replace("<", "")
        a[1] = a[1].replace(">", "")
        a[1] = a[1].replace("\n", "")
        args = a[1].split(',')
        closeFile(args[0], username)
    elif a[0] == 'write_to_file':
        a[2] = ' '.join(a[2:])
        a[1] = a[1].replace("<", "")
        a[1] = a[1].replace(">", "")
        a[1] = a[1].replace("\n", "")
        a[1] = a[1].replace(",", "")
        a[2] = a[2].replace(",", "")
        a[2] = a[2].replace("\n", "")
        openFile(a[1], 'w', a[2], 0, 0, username)
    elif a[0] == 'write_at':
        a[1] = a[1].replace("<", "")
        a[1] = a[1].replace(">", "")
        a[1] = a[1].replace("\n", "")
        a[1] = a[1].replace(",", "")
        more_text = a[2:-1]
        a[3] = a[3].replace("\n", "")
        a[3] = a[3].replace(",", "")

        # a[4] = a[4].replace("\n", "")
        more_text = ' '.join(more_text)
        openFile(a[1], 'w', more_text, a[-1],0, username)
    elif a[0] == 'truncate_file':
        truncateFile(a[1], a[2])
    elif a[0] == 'mov':
        moveFile(a[1], a[2])
    elif a[0] == 'show':
        showDat()
    elif a[0] == 'exit':
        sys.exit(0)
    elif a[0] == 'mmap':
        memoryMap()     
    else:
        clientInfo


def showDat():
    readDat()
    clientInfo["message"] = ""
    for key in datdict:
        clientInfo["message"] += key + " " + datdict[key] + "\n"


def saveDat():
    file = open(root+"/" + "dat.dat", "w")
    for key in datdict:
        file.write(key + "#" + datdict[key] + "\n")
    file.close()


def writeDat(filename):
    readDat()
    file = open(filename, "r")
    content = file.read()
    datdict[filename] = content
    saveDat()


def readDat():

    if os.path.isfile(root+"/"+"dat.dat"):
        file = open(root+"/"+"dat.dat", "r")
        for line in file:
            if '#' in line:
                (key, val) = line.split('#', 1)
                datdict[key] = val

        file.close()

    else:
        file = open(root+"/"+"dat.dat", "w")
        file.close()


def createFile(filename):
    file = open(filename, "w")
    file.close()
    writeDat(filename)
    clientInfo["message"] = 'File ' + filename + ' created successfully!'


def deleteFile(filename):
    print(filesInUse)
    if filename not in filesInUse:
        datdict.pop(filename)
        print(filename)
        os.remove(filename)
        clientInfo["message"] = 'File ' + filename + ' deleted successfully!'
    else:
        clientInfo["message"] = 'File ' + filename + ' is in use!'


def makeDirectory(directory):
    if os.path.isdir(directory):
        print("Directory already exists!!!")
        clientInfo["message"] = "Directory already exists!!!"
    else:
        directoryName = root + "/" + directory
        print(directoryName)
        clientInfo["message"] = "Directory created successfully --> " + directoryName
        os.mkdir(directoryName)


def changeDirectory(directory):

    if directory == "..":
        directoryName = root
    else:
        directoryName = root + "/" + directory
        directoryName = directoryName.replace("\n", "")
    print(directoryName)
    clientInfo["message"] = "Directory changed successfully!"
    if os.path.isdir(directoryName):
        os.chdir(directoryName)
        clientInfo["message"] = "Directory changed successfully to " + directoryName
    else:
        print("Directory does not exist!")
        clientInfo["message"] = "Directory does not exist!"


def moveFile(filename, destination):
    lock.acquire()

    if os.path.exists(filename):
        if filename in filesInUse:
            print("File is in use, cannot be moved!")
            clientInfo["message"] = "File is in use, cannot be moved!"
        else:
            directoryName = root + "/" + destination
            if os.path.isdir(directoryName):
                os.rename(filename, directoryName + "/" + filename)
                clientInfo["message"] = "File moved successfully to " + \
                    directoryName
            else:
                print("Directory does not exist!")
                clientInfo["message"] = "Directory does not exist!"

    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"

    lock.release()


def openFile(filename, mode, content='', startingIndex=0, size=0, user=''):

    fileName = filename
    if os.path.exists(filename):
        match mode:

            case 'w':
                if filename not in filesInUse:
                    if writer['username'] == '':
                        writer["username"] = user
                        print(writer['username'])
                        file = open(filename, "r")
                        filesInUse.append(file)
                        contents = file.read()
                        filesInUse.remove(file)
                        file.close()
                        contents = str(contents)
                        if int(startingIndex) > len(contents):
                            startingIndex = len(contents)

                        contents = contents[:int(startingIndex)] + \
                            content + contents[int(startingIndex):]
                        file = open(filename, "w")
                        filesInUse.append(file)
                        if (startingIndex == 0):
                            file.write(content)
                        else:
                            file.write(contents)
                        if filename in filesInUse:
                            filesInUse.remove(filename)
                        file.close()
                        clientInfo["message"] = "File written to successfully!"
                    else:
                        clientInfo["message"] = "File is in use by " + writer["username"]
                        print("File is in use by " + writer["username"])    
                else:
                    print(filesInUse)
                    print("File is in use, cannot be written to!")
                    clientInfo["message"] = "File is in use, cannot be written to!"

            case 'r':
                if writer['username'] == '':
                    print(writer['username'])
                    filename = open(filename, "r")
                    filesInUse.append(fileName)
                    clientInfo["message"] =("Contents of " + fileName +
                        ": " + filename.read())
                    print(clientInfo["message"])
                    filename.close()
                else:
                    clientInfo["message"] = "File is in use by " + writer["username"]
            case 'x':
                file = open(filename, "r")
                filesInUse.append(file)
                index = startingIndex
                length = size
                contents = file.read()
                print(contents[int(index):int(index) + int(length)])
                clientInfo["message"] = contents[int(
                    index):int(index) + int(length)]
                file.close()

            case _:
                print("Invalid mode!")
                clientInfo["message"] = "Invalid mode!"

        writeDat(fileName)
    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"


# def moveWithinFile():
#     filename = input("Enter the name of the file you want to write to: ")
#     if os.path.exists(filename):
#         file = open(filename, "r")
#         filesInUse.append(file)
#         contents = file.read()
#         filesInUse.remove(file)
#         file.close()
#         contents = str(contents)
#         moveDataFrom = int(input("Enter starting index: "))
#         moveDataTo = int(input("Enter ending index: "))
#         lengthOfDataToMove = int(input("Enter length of data to move:"))
#         dataToMove = contents[moveDataFrom:moveDataFrom + lengthOfDataToMove]
#         contents = contents[:moveDataFrom] + \
#             contents[moveDataFrom + lengthOfDataToMove:]
#         contents = contents[:moveDataTo] + dataToMove + \
#             contents[moveDataTo:]

#         file = open(filename, "w")
#         filesInUse.append(file)
#         file.write(contents)
#         filesInUse.remove(file)
#         file.close()
#         writeDat(filename)

#     else:
#         print("File does not exist!!!")


def truncateFile(filename, size):
    if os.path.exists(filename):
        fileSize = os.path.getsize(filename)
        if int(size) < fileSize:
            file = open(filename, "r+")
            filesInUse.append(file)
            file.truncate(int(size))
            filesInUse.remove(file)
            clientInfo["message"] = "File truncated successfully!"
            file.close()
            writeDat(filename)
        else:
            print("File is already smaller than the size you want to truncate to!")
            clientInfo["message"] = "File is already smaller than the size you want to truncate to!"
    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"


def closeFile(filename, user):
    if filename in filesInUse:
        filesInUse.remove(filename)
        # writer[] = ''
        clientInfo["message"] = "File closed successfully!"
    elif user == writer["username"]:
        writer["username"] = ''
        clientInfo["message"] = "File closed successfully!"
    else:
        print("File is not opened!")
        clientInfo["message"] = "File is not opened!"


def memoryMap():
    arr = {}
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            file = open(os.path.join(root, name), "r")
            arr[os.path.join(root, name)] = hex(id(file))

        for name in dirs:
            if os.path.isdir(os.path.join(root, name)) == False:
                file = open(os.path.join(root, name), "r")
                arr[os.path.join(root, name)] = hex(id(file))

        clientInfo["message"] = ''
        for key, value in arr.items():
            print(key + ':\t' + value+'\n')
            clientInfo["message"] += key + ':\t' + value+'\n'


if __name__ == "__main__":
    filenames = ['input.txt', 'input2.txt', 'input3.txt', 'input4.txt']

    nThreads = int(sys.argv[1])
    print("Threads: " + str(nThreads))

    for i in range(nThreads):
        f = open(filenames[i], "r")
        lines = f.readlines()

        t = threading.Thread(target=thread_function, args=[i, lines])
        t.start()

# readDat()
# print("Welcome to the file system")
# while True:
#     print('Current working directory: ' + os.getcwd())
#     print('0. Exit')
#     print("1. Create a file")
#     print("2. Delete a file")
#     print("3. Close file")
#     print("4. Create a directory")
#     print("5. Change directory")
#     print("6. Move a file")
#     print("7. Open a file")
#     print("8. Move within a file")
#     print("9. Truncate a file")
#     print("10. Memory map")
#     print("11. List files")

#     mode = input("Enter the mode you want to run the file system in: ")
#     match mode:
#         case '0':
#             print("exiting")
#             break
#         case '1':
#             createFile()
#         case '2':
#             filename = input(
#                 "Enter the name of the file you want to delete: ")
#             deleteFile(filename)
#         case '3':
#             closeFile()
#         case '4':
#             makeDirectory()
#         case '5':
#             changeDirectory()
#         case '6':
#             moveFile()
#         case '7':
#             openFile()
#         case '8':
#             moveWithinFile()
#         case '9':
#             truncateFile()
#         case '10':
#             memoryMap()
#         case '11':
#             showDat()

#         case _:
#             print("Invalid mode!!!")
# saveDat()
# print("Thank you for using the file system")
