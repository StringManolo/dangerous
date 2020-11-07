import secrets

def Myszkowski(string, key):
# Key to uppercase and key remove spaces
    i = 0
    aux = []
    while i < len(key):
        if key[i] != " ":
            aux.append(key[i].upper())
        i += 1
    key = aux[:]


# alfabetical position number :
    keyOrder = []
    i = 0
    while i < len(key):
        keyOrder.append(ord(key[i])-96)
        i += 1

#    print(keyOrder)
    

# bubble sorting :
    keyOcurr = keyOrder[:]
    i = 0
    while i < len(keyOrder):
        j = 0
        while j < (len(keyOrder) - 1):
            if keyOrder[j] > keyOrder[j+1]:
                keyOrder[j], keyOrder[j+1] = keyOrder[j+1], keyOrder[j]
            j += 1
        i += 1

#    print(keyOrder)


# find first ocurrence and change to char :
 #    print(f"""
 #
 #keyOrder:
 #{keyOrder}
 #
 #keyOcurr:
 #{keyOcurr}
 #
 #""")
    i = 0
    j = 0
    k = 97
    already = []
    while i < len(keyOrder):
        j = 0
        while j < (len(keyOrder) ):
#            print(f"Comparing keyOrder[i] ({keyOrder[i]}) and keyOcurr[j] ({keyOcurr[j]})")
            if keyOrder[i] == keyOcurr[j]:
#                print(f"\n\nKeyOrder ({keyOrder[i]}) found in position {i}")
#                print(f"Replacing ({keyOcurr[j]}) by {chr(k)}")
                l = 0
                while l < len(already):
#                    print(f"Testing if char(k) ({chr(k)}) is equal to already[l] ({already[l]})")
                    if keyOrder[i] == already[l]:
#                        print(f"This char ({chr(k)}) was already found.")
                        k -= 1
                        break
                    l += 1
            
                already.append(keyOrder[i])
                keyOcurr[j] = chr(k)
                k += 1
            j += 1
        i += 1

#    print(keyOcurr)
   
    i = 0
    while i < len(keyOcurr):
        keyOcurr[i] = ord(keyOcurr[i]) - 96
        i += 1

    print(f"""[{', '.join(map(str, list(key)))}]
{keyOcurr}
""")


# create table based on key length :
    i = 0
    j = 0
    table = []
    row = []
    while i < len(string):
        if j == len(key):
            table.append(row)
            j = 0
            row = []
        row.append(string[i])
        i += 1
        j += 1
    
# padding and pendding row
    if j < len(key):
        i = 0
        while i < (len(key) - j):
            # chosing randomly the padding from the charset
            row.append(secrets.choice(table[secrets.randbelow(len(table))]))
            # I feel this way is more secure. 
            i += 1
        table.append(row)


    prettyPrint = ']\n['.join(map(lambda x: ', '.join(map(str, x)), table))
    print(f"[{prettyPrint}]")



# End of cipher :
    


Myszkowski("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789Este es el texto a trasposicionar", "EstaEsLaKey")
#Myszkowski("", "abxdcazbeafgbmhai")