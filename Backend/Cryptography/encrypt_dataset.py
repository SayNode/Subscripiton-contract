#this imports the cryptography package
from cryptography.fernet import Fernet

def encryptData():
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()

    #this opens your json and reads its data into a new variable called 'data'
    with open('dataset.json','rb') as f:
        data = f.read()

    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #this writes your new, encrypted data into a new JSON file
    with open('dataset_encrypted.json','wb') as f:
        f.write(encrypted)

def decryptData():
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()
    
    #this opens your json and reads its data into a new variable called 'data'
    with open('dataset_encrypted.json','rb') as f:
        data = f.read()

    #this decrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    #this writes your new, encrypted data into a new JSON file
    with open('dataset_decrypted.json','wb') as f:
        f.write(encrypted)

encryptData()
decryptData()