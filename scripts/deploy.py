from brownie import accounts, config, DataSetFactory
import time
import os

def deploy():
    #A)For local ganache
    dohrnii_account = accounts[0] 

    #B)To import a wallet you need to do on the terminal:
        #1)brownie accounts new <name of the account>
        #2)Enter "0x"+ the private key you wish to import
        #3)Enter a password of your choosing to encrypt the account
        #To load account in this code: account = accounts.load("SAYNODE")

    #C)If we want to use .env
        #1)Create a .env file
        #2)Add "export PRIVATE_KEY = <wallet private key>" to it
        #3)Use the code bellow:
        #account = accounts.add(os.getenv("PRIVATE_KEY"))
    #D)Using "wallets" section in brownie-config.yaml:
        #1)Define the wallets in the brownie-config.yaml
        #2)Do the code bellow:
        #account = accounts.add(config["wallets"]["from_key"])
    
    #Deployment
    #dohrnii_token_contrat = DHN.deploy()=>we will probably import an existing DHN contract
    dataset_factory = DataSetFactory.deploy("0x2a90E736b550E3A7AF5cD7C18F74AADa08b7410F", {"from": dohrnii_account})
    time.sleep(1)#avoids known Brownie error "web3 is not connected"
    return dataset_factory

def main():

    #Get the DataSetFactory.sol instance after deployment and the account used
    DSF=deploy()
    dohrnii_account = accounts[0]
    ds_creator_account = accounts[1]
    ds_subscriber_account = accounts[2]

    #Testing a changeStakeAmount() from DataSetFactory.sol
    print(DSF.stakeAmount())
    DSF.changeStakeAmount(2, {"from": dohrnii_account})
    time.sleep(1)#avoids known Brownie error "web3 is not connected"
    print(DSF.stakeAmount())

    #Testing createDS() from DataSetFactory.sol
    DSF.createDS("Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10, 30, 2)