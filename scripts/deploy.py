from brownie import accounts

def deploy():
    account = accounts[0]#for local ganache
    #To import a wallet you need to do on the terminal:
    #1)brownie accounts new <name of the account>
    #2)Enter "0x"+ the private key you wish to import
    #3)Enter a password of your choosing to encrypt the account
    print(account)

def main():
    deploy()