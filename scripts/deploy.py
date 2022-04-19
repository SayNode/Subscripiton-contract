from brownie import accounts, config,chain,  DataSetFactory,DataSet, DHN
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

#Testing createDS() from DataSetFactory.sol
def createDS(DHN, DSF, ds_creator_account, DS_name, DS_IPFS_link, ds_category, ds_desc, ds_sub_price, update_freq, penalty):
    print("------------------Creating a DS------------------")
    DHN.approve(DSF,300, {"from": ds_creator_account}) #creator approves that the DSF contract 
                                                       #can send tokens to the DS contract (amount = stakeAmount)

    DSF.createDS(DS_name, DS_IPFS_link, ds_category, ds_desc, ds_sub_price, update_freq, penalty, 
                {"from": ds_creator_account}) #DS created

def getDSinfo(DSF, ds_creator_account, ds_name):
    DS = getDSbyName(DSF, ds_creator_account, ds_name)
    print("DS info: ") # see info of sub1
    print("     Creator address: "+str(DS.creatorAddress())+" == "+str(ds_creator_account)) # see info of sub1
    print("     Dataset Sub Price: "+str(DS.DSprice())) # see info of sub1
    print("     Dataset Update freq: "+str(DS.updateFrequency())) # see info of sub1
    print("     Dataset Stake: "+str(DS.stakeAmount())) # see info of sub1
    print("     Dataset Penalty: "+str(DS.penalty())) # see info of sub1
    
#Accesing the creator DS contract
def getDSbyName(DSF, ds_subscriber_account, ds_name):
    print("------------------Get DataSet address by name------------------")
    DS_address = DSF.nameToSC(ds_name,{"from": ds_subscriber_account}) #get the address of DS according to its name
    DS = DataSet.at(DS_address) #instantiate the DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Staked amount(correct if it is 20): " + str(DS.stakeAmount())) #see if the creator staking in the DS worked
    return DS

#Subscribing to a DS
def subToDS(DHN,DSF, ds_subscriber_account, ds_name, sub_option):

    DS = getDSbyName(DSF, ds_subscriber_account, ds_name)

    print("------------------Subbing------------------")
    DHN.approve(DS,300, {"from": ds_subscriber_account}) #sub1 approves that the DSF contract 
                                                          #can send tokens to the DS contract (amount = stakeAmount)

    DS.subscribeToDS(sub_option, {"from": ds_subscriber_account}) #sub1 subscribes to the "Tetris" DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Subscriber info: ") # see info of sub1
    print("     Price paid: "+str(DS.addressToSub(ds_subscriber_account)[0])) # see info of sub1
    print("     Subscription Period: "+str(DS.addressToSub(ds_subscriber_account)[1])) # see info of sub1
    print("     Subscribed at blocktimestamp: "+str(DS.addressToSub(ds_subscriber_account)[2])) # see info of sub1

 #Withdraw funds Case1: booth subs have ended their sub time and the creator can withdraw
def withdrawFunds(DHN,DSF, ds_creator_account, ds_name):

    DS = getDSbyName(DSF, ds_creator_account, ds_name)

    print("------------------Withdraw Funds------------------")
    print("Creator Balance Before Withdraw: "+str(DHN.balanceOf(ds_creator_account)))#sould be 10 (starts with 30 and stakes 20)
    #print("Sub count Before Withdraw: "+str(DS.numberOfCurrentlySubbed()) )#should be 2
    print("Contract balance Before Withdraw: "+str(DS.getContractBalance()) )#should be 40 (20 staked by the creator+10 for each sub)

    DS.withdrawFunds({"from": ds_creator_account})

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Creator Balance After withdraw: " + str(DHN.balanceOf(ds_creator_account)))#should be 30 (10 he had + 10 from each sub)
    print("Contract balance After withdraw: "+str(DS.getContractBalance()))#should bonly be the staked 20

  
def main():

    #Get the DataSetFactory.sol instance after deployment and the account used
    (DSF,DHN)=deploy()

    #Define accounts
    dohrnii_account = accounts[0] #mints the DHN tokens
    ds_creator_account = accounts[1] #creates a nem Data Set callled "Tetris"
    ds_subscriber_account1 = accounts[2] #will subscribe to the "Tetris" dataset with a 1s sub time
    ds_subscriber_account2 = accounts[3] #will also subscribe to the "Tetris" dataset with a 1s sub time
    ds_subscriber_account3 = accounts[4] #will subscribe to the "Tetris" dataset with a 1day sub time
    ds_subscriber_account4 = accounts[5] #will also subscribe to the "Tetris" dataset with a 30 days sub time

    #Fund accounts
    DHN.transfer(ds_creator_account, 30, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_subscriber_account1, 30, {"from": dohrnii_account}) #fund sub1
    DHN.transfer(ds_subscriber_account2, 30, {"from": dohrnii_account}) #fund sub2  

    #Create a DS and instantiate it
    createDS(DHN, DSF, ds_creator_account,"Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10, 3600, 2)

    #Sub1
    subToDS(DHN, DSF, ds_subscriber_account1, "Tetris", 0)    
    #Sub2
    subToDS(DHN, DSF, ds_subscriber_account2, "Tetris", 0)

    #Simulating the passing of 10 seconds
    chain.sleep(10)

    #Withdraw funds
    withdrawFunds(DHN, DSF, ds_creator_account, "Tetris")

    #Get a DS info
    getDSinfo(DSF, ds_creator_account, "Tetris")