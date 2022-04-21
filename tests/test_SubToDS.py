from brownie import accounts, config,chain,  DataSetFactory,DataSet, DHN
import scripts.deploy as deployer

#Test the subscription to two DataSets
#See the changes in:
                    # variables (subCount, contract balance, subBalance), 
                    # mappings(addressToSub), 
                    # arrays of structs (deposits, subscribres)

def testCreateDS():
    dec_fit = 10**18

    #Get the DataSetFactory.sol instance after deployment and the account used
    (DSF,DHN)=deployer.deploy()

    #Define accounts
    dohrnii_account = accounts[0] #mints the DHN tokens
    ds_creator_account1 = accounts[1] #creates a nem Data Set callled "Tetris"
    ds_creator_account2 = accounts[2] #creates a nem Data Set callled "Desserts"
    ds_subscriber_account1 = accounts[3] #will subscribe to the "Tetris" dataset with a 1s sub time
    ds_subscriber_account2 = accounts[4] #will also subscribe to the "Tetris" dataset with a 1s sub time
    ds_subscriber_account3 = accounts[5] #will subscribe to the "Desserts" dataset with a 1day sub time
    ds_subscriber_account4 = accounts[6] #will also subscribe to the "Desserts" dataset with a 30 days sub time

    #Fund accounts
    DHN.transfer(ds_creator_account1, 30*dec_fit, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_creator_account2, 30*dec_fit, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_subscriber_account1, 30*dec_fit, {"from": dohrnii_account}) #fund sub1
    DHN.transfer(ds_subscriber_account2, 30*dec_fit, {"from": dohrnii_account}) #fund sub2
    DHN.transfer(ds_subscriber_account3, 30*dec_fit, {"from": dohrnii_account}) #fund sub3
    DHN.transfer(ds_subscriber_account4, 30*dec_fit, {"from": dohrnii_account}) #fund sub4    

    #Create a DS and instantiate it
    deployer.createDS(dec_fit, DHN, DSF, ds_creator_account1,"Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10*dec_fit, 3600, 2*dec_fit)

    DS_instance1 = deployer.getDSbyName(dec_fit, DSF, ds_subscriber_account1, "Tetris")
    
    #Create a DS and instantiate it
    deployer.createDS(dec_fit, DHN, DSF, ds_creator_account2,"Desserts", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Food","Some dessert recipes", 5*dec_fit, 3600, 2*dec_fit)
          
    DS_instance2 = deployer.getDSbyName(dec_fit, DSF, ds_subscriber_account2, "Desserts")

    #Sub1
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account1, "Tetris", 0)    
    #Sub2
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account2, "Tetris", 0)
    #Sub3
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account3, "Desserts", 1)    
    #Sub4
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account4, "Desserts", 2)

#Assertion: DS creation alterations
    
    assert ((20+10*2)*dec_fit, 2) == (DHN.balanceOf(DS_instance1),#contract balance changes because of 2 subs
                            DS_instance1.subCount())#subcount increases by 2
    
    assert ((20+2*5)*dec_fit, 2) == (DHN.balanceOf(DS_instance2),#contract balance changes because of 2 subs
                        DS_instance2.subCount())#subcount increases by 2
    
#Assertion: Sub info

    #Subscribed to "Tetris"
    info1 = DS_instance1.addressToSub(ds_subscriber_account1)
    #Price paid, subscription time, Is this person currently subbed?
    assert (10*dec_fit, 1, True) == (info1[0], info1[1], info1[3])

    #Subscribed to "Tetris"
    info2 = DS_instance1.addressToSub(ds_subscriber_account2)
    #Price paid, subscription time, Is this person currently subbed?
    assert (10*dec_fit, 1, True) == (info2[0], info2[1], info2[3])

    #Not subscribed to "Tetris"
    info3 = DS_instance1.addressToSub(ds_subscriber_account3)
    #Price paid, subscription time, Is this person currently subbed?
    assert (0, 0, False) == (info3[0], info3[1], info3[3])

    #Subscribed to "Desserts"
    info4 = DS_instance2.addressToSub(ds_subscriber_account3)
    #Price paid, subscription time, Is this person currently subbed?
    assert (5*dec_fit, 24*3600, True) == (info4[0], info4[1], info4[3])

    #Subscribed to "Desserts"
    info5 = DS_instance2.addressToSub(ds_subscriber_account4)
    #Price paid, subscription time, Is this person currently subbed?
    assert (5*dec_fit, 30*24*3600, True) == (info5[0], info5[1], info5[3])

    #Not subscribed to "Desserts"
    info6 = DS_instance2.addressToSub(ds_subscriber_account1)
    #Price paid, subscription time, Is this person currently subbed?
    assert (0, 0, False) == (info6[0], info6[1], info6[3])

#Assertion: Deposits

    #Subscribed to "Tetris"
    info1 = DS_instance1.deposits(0)
    #Price paid, subscription time, Is this person currently subbed?
    assert (ds_subscriber_account1, 10*dec_fit) == (info1[0], info1[1])

#Assertion: Mappings

