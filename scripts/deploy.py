from brownie import accounts, config, DataSetFactory,DataSet, DHN
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
    #Call existing contract:dohrnii_token_contrat = DHN.at("0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87")(dohrnii_account,{"from": dohrnii_account})
    dohrnii_token_contrat = DHN.deploy(dohrnii_account,{"from": dohrnii_account})
    time.sleep(1)#avoids known Brownie error "web3 is not connected"
    dataset_factory = DataSetFactory.deploy(dohrnii_token_contrat, {"from": dohrnii_account})
    time.sleep(1)#avoids known Brownie error "web3 is not connected"
    return dataset_factory, dohrnii_token_contrat

def main():

    #Get the DataSetFactory.sol instance after deployment and the account used
    (DSF,DHN)=deploy()

    #Define accounts
    dohrnii_account = accounts[0] #mints the DHN tokens
    ds_creator_account = accounts[1] #creates a nem Data Set callled "Tetris"
    ds_subscriber_account1 = accounts[2] #will subscribe to the "Tetris" dataset
    ds_subscriber_account2 = accounts[3] #will also subscribe to the "Tetris" dataset

    #Fund accounts
    DHN.transfer(ds_creator_account, 3000, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_subscriber_account1, 3000, {"from": dohrnii_account}) #fund sub1
    DHN.transfer(ds_subscriber_account2, 3000, {"from": dohrnii_account}) #fund sub2

#Testing createDS() from DataSetFactory.sol
    DHN.approve(DSF,300, {"from": ds_creator_account}) #creator approves that the DSF contract 
                                                       #can send tokens to the DS contract (amount = stakeAmount)

    DS = DSF.createDS("Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10, 20, 2, {"from": ds_creator_account}) #DS created
  
    
#Accesing the creator DS contract
    DS_address = DSF.nameToSC("Tetris",{"from": ds_subscriber_account1}) #get the address of DS according to its name
    DS = DataSet.at(DS_address) #instantiate the DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Staked amount(correct if it is 20): " + str(DS.stakeAmount())) #see if the creator staking in the DS worked

#Subscribing to a DS
    DHN.approve(DS,300, {"from": ds_subscriber_account1}) #sub1 approves that the DSF contract 
                                                          #can send tokens to the DS contract (amount = stakeAmount)

    DS.subscribeToDS(20,{"from": ds_subscriber_account1}) #sub1 subscribes to the "Tetris" DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Subscriber info: ") # see info of sub1
    print("     Price paid: "+str(DS.addressToSub(ds_subscriber_account1)[0])) # see info of sub1
    print("     Subscription Period: "+str(DS.addressToSub(ds_subscriber_account1)[1])) # see info of sub1
    print("     Subscribed at blocktimestamp: "+str(DS.addressToSub(ds_subscriber_account1)[2])) # see info of sub1

    ##
    

  
    