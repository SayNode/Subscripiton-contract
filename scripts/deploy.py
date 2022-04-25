from brownie import accounts, config, chain, Contract, DataSetFactory, DataSetFactoryV2, DataSet, DHN, TransparentUpgradeableProxy, ProxyAdmin
from scripts.helpful_scripts import get_account, encode_function_data
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

    dataset_factory = DataSetFactory.deploy({"from": dohrnii_account})

    #Proxy initializer
    DSF_encoded_initializer_function = encode_function_data(dataset_factory.initialize, dohrnii_token_contrat,20*10**18)

    #Proxy deployment
    proxy = TransparentUpgradeableProxy.deploy(
        dataset_factory.address,
        dohrnii_account.address,
        #proxy_admin.address,
        DSF_encoded_initializer_function,
        {"from": dohrnii_account, "gas_limit": 1000000},
    )
    #Establish initial link of proxy to DataSetFactory.sol
    dataset_factory = Contract.from_abi("DataSetFactory", proxy.address, DataSetFactory.abi)


    return dataset_factory, dohrnii_token_contrat

#Testing createDS() from DataSetFactory.sol
def createDS(dec_fit, DHN, DSF, ds_creator_account, DS_name, DS_IPFS_link, ds_category, ds_desc, ds_sub_price, update_freq, penalty):
    print("------------------Creating a DS------------------")
    DHN.approve(DSF,30*dec_fit, {"from": ds_creator_account}) #creator approves that the DSF contract 
                                                       #can send tokens to the DS contract (amount = stakeAmount)

    DSF.createDS(DS_name, DS_IPFS_link, ds_category, ds_desc, ds_sub_price, update_freq, penalty, 
                {"from": ds_creator_account}) #DS created

def getDSinfo(dec_fit, DSF, ds_creator_account, ds_name):
    DS = getDSbyName(dec_fit, DSF, ds_creator_account, ds_name)
    print("DS info: ") # see info of sub1
    print("     Creator address: "+str(DS.creatorAddress())+" == "+str(ds_creator_account)) #TEST:
    print("     Dataset Sub Price: "+str(DS.DSprice()/dec_fit)) #TEST:
    print("     Dataset Update freq: "+str(DS.updateFrequency())) #TEST:
    print("     Dataset Stake: "+str(DS.stakeAmount()/dec_fit)) #TEST:
    print("     Dataset Penalty: "+str(DS.penalty()/dec_fit)) #TEST:
    
#Accesing the creator DS contract
def getDSbyName(dec_fit, DSF, ds_subscriber_account, ds_name):
    print("------------------Get DataSet address by name------------------")
    DS_address = DSF.nameToSC(ds_name,{"from": ds_subscriber_account}) #get the address of DS according to its name
    DS = DataSet.at(DS_address) #instantiate the DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Staked amount(correct if it is 20): " + str(DS.stakeAmount()/dec_fit)) #TEST:see if the creator staking in the DS worked
    return DS

#Subscribing to a DS
def subToDS(dec_fit, DHN,DSF, ds_subscriber_account, ds_name, sub_option):

    DS = getDSbyName(dec_fit, DSF, ds_subscriber_account, ds_name)

    print("------------------Subbing------------------")
    DHN.approve(DS,30*dec_fit, {"from": ds_subscriber_account}) #sub1 approves that the DSF contract 
                                                          #can send tokens to the DS contract (amount = stakeAmount)

    DS.subscribeToDS(sub_option, {"from": ds_subscriber_account}) #sub1 subscribes to the "Tetris" DS

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Subscriber info: ") #TEST:see info of sub1
    print("     Price paid: "+str(DS.addressToSub(ds_subscriber_account)[0]/dec_fit)) #TEST:see info of sub1
    print("     Subscription Period: "+str(DS.addressToSub(ds_subscriber_account)[1])) #TEST:see info of sub1
    print("     Subscribed at blocktimestamp: "+str(DS.addressToSub(ds_subscriber_account)[2])) #TEST:see info of sub1

 #Withdraw funds Case1: booth subs have ended their sub time and the creator can withdraw
def withdrawFunds(dec_fit, DHN,DSF, ds_creator_account, ds_name):

    DS = getDSbyName(dec_fit, DSF, ds_creator_account, ds_name)

    print("------------------Withdraw Funds------------------")
    print("Creator Balance Before Withdraw: "+str(DHN.balanceOf(ds_creator_account)/dec_fit))#TEST:sould be 10 (starts with 30 and stakes 20)
    #print("Sub count Before Withdraw: "+str(DS.numberOfCurrentlySubbed()) )#TEST:should be 2
    print("Contract balance Before Withdraw: "+str(DS.getContractBalance()/dec_fit) )#TEST:should be 40 (20 staked by the creator+10 for each sub)

    DS.withdrawFunds({"from": ds_creator_account})

    time.sleep(1) #avoids known Brownie error "web3 is not connected"
    print("Creator Balance After withdraw: " + str(DHN.balanceOf(ds_creator_account)/dec_fit))#TEST:should be 30 (10 he had + 10 from each sub)
    print("Contract balance After withdraw: "+str(DS.getContractBalance()/dec_fit))#TEST:should bonly be the staked 20

def upgradeDSF(dec_fit, DHN,DSF, dohrnii_account, ds_name):
        dataset_factoryV2 = DataSetFactoryV2.deploy({"from": dohrnii_account})
        proxy = TransparentUpgradeableProxy[-1]
        proxy_admin = ProxyAdmin[-1]
        upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
        print("Proxy has been upgraded!")
        proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
  
def main():
    dec_fit = 10**18
    #Get the DataSetFactory.sol instance after deployment and the account used
    (DSF,DHN)=deploy()

    #Define accounts
    dohrnii_account = accounts[0] #mints the DHN tokens
    ds_creator_account1 = accounts[1] #creates a nem Data Set callled "Tetris"
    ds_creator_account2 = accounts[2] #creates a nem Data Set callled "Tetris"
    random_account1 = accounts[3]#just to call a DS by its name

    #Fund accounts
    DHN.transfer(ds_creator_account1, 30*dec_fit, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_creator_account2, 30*dec_fit, {"from": dohrnii_account}) #fund the creator  

    #Create a DS and instantiate it
    createDS(dec_fit,DHN, DSF, ds_creator_account1,"Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10*dec_fit, 3600, 2*dec_fit)

    DS_instance1 = getDSbyName(dec_fit, DSF, random_account1, "Tetris")
    