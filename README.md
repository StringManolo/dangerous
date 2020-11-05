# dangerous
Dangerous Malware. Educational purpouse only.  

Don't donwload to your PC if you don't know what are you doing.  
  
Don't execute on other computers, systems, etc.  
Just don't be dumb.  
  
I take no responsability for bad usage.  
  

### Examples:

Encrypt files in current folder:  
```
python smr.py -v -a txt -e -k 1337 -p ./
```
  
Decrypt files in current folder:  
```
python smr.py -v -a txt -d -k 1337 -p ./
```
  
### Arguments:  
Usage: python smr.py [-option1] [-option2] [...]  
 -a,  --adition  Add/Remove file extension to/from file.  
 -d,  --decrypt  Only decrypt. If a non encrypted file is in the path, will be encrypted.  
 -e,  --encrypt  Only encrypt. Uses weak Symmetric-key algorithm. Similar to Vernan or Affine encryption.  
 -h,  --help     Open this menu.  
 -i,  --interactive  Extra help to use the ransomware.  
 -k,  --key      Key/Password to encrypt files.  
 -p,  --path     Chose the path where the ransomware is goinf to run. All files in the path ans subpaths will be selected.  
 -v,  --verbose  Add more output to the console. Show more information about the running tasks.  

NOTICE: You can lose your files if the ranswomare crash, your pc shutdown or you can't remember your encryption key. I didn't made a bruteforce algorithm to decrypt the files. Since password is reused can be possible to recover the encrypted files. If you seriously need to, send me a message. https://twitter.com/XSStringManolo  
