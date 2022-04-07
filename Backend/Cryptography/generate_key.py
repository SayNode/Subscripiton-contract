import base64
import os
#this imports the cryptography package
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#this generates a key and opens a file 'key.key' and writes the key there
def generateRandomKey():
    key = Fernet.generate_key()
    print(key)
    with open('key.key','wb') as file:
        file.write(key)

#this generates the salt which further protects our password generated key. The salt does not need to be private
#the salt is usefull if we want to change password in the future (which we should for security reasons)
#because it adds another non-deterministic layer to the encryption. Without it, two equal passwords would provide 
#the same encryption key
def generateSalt():
    salt  = os.urandom(16)#https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/
    return salt

#this generates a key from a password and opens a file 'key.key' and writes the key there
def generatePasswordKey(password, salt):
    password_provided = password #Input from us
    password = password_provided.encode() #Converts string to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print(key)

salt  = generateSalt()
generatePasswordKey("hello", salt)#EQUAL
generatePasswordKey("hel", salt)#DIFFERENT
generatePasswordKey("hello", salt)#EQUAL