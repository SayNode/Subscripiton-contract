from brownie import accounts, config,chain,  DataSetFactory,DataSet, DHN
import scripts.deploy as deployer

#Test all the functions in DataSet.sol

def testCreateDS():
    dec_fit = 10**18
    #Get the DataSetFactory.sol instance after deployment and the account used
    (DSF,DHN)=deployer.deploy()

    #Define accounts
    dohrnii_account = accounts[0] #mints the DHN tokens
    ds_creator_account1 = accounts[1] #creates a nem Data Set callled "Tetris"
    ds_creator_account2 = accounts[2] #creates a nem Data Set callled "Tetris"
    random_account1 = accounts[3]#just to call a DS by its name

    #Fund accounts
    DHN.transfer(ds_creator_account1, 30*dec_fit, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_creator_account2, 30*dec_fit, {"from": dohrnii_account}) #fund the creator  

    #Create a DS and instantiate it
    deployer.createDS(dec_fit, DHN, DSF, ds_creator_account1,"Tetris", "https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/Tetris.html",
                 "Games","Tetris statistics and data", 10*dec_fit, 3600, 2*dec_fit)

    DS_instance1 = deployer.getDSbyName(dec_fit, DSF, random_account1, "Tetris")
    
    #Create a DS and instantiate it
    deployer.createDS(dec_fit, DHN, DSF, ds_creator_account2,"Desserts", "https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/Dessert.html",
                 "Food","Some dessert recipes", 5*dec_fit, 3600, 2*dec_fit)
          
    DS_instance2 = deployer.getDSbyName(dec_fit, DSF, random_account1, "Desserts")

#Assertion: Owner Functions
    #URL
    assert DS_instance1.URL() == "https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/Tetris.html"
    DS_instance1.updateURL("https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/",{"from": ds_creator_account1})
    assert DS_instance1.URL() == "https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/"
    #Price
    assert DS_instance1.DSprice() == 10*dec_fit
    DS_instance1.changePrice(7*dec_fit,{"from": ds_creator_account1})
    assert DS_instance1.DSprice() == 7*dec_fit
    #Category
    assert DS_instance1.category() == "Games"
    DS_instance1.changeCategory("Websites",{"from": ds_creator_account1})
    assert DS_instance1.category() == "Websites"
    #Description
    assert DS_instance1.shortDesc() == "Tetris statistics and data"
    DS_instance1.changeDescription("Full wikipedia website",{"from": ds_creator_account1})
    assert DS_instance1.shortDesc() == "Full wikipedia website"

    #Withdraw funds (both subscribers sub period has ended)
    
    #DS_instance1.withdrawFunds({"from": ds_creator_account1})


    #DS_instance1.stakeMoreDHN(2*dec_fit)
    #deployer.deleteDS()

#Assertion: Subscriber Functions

#Assertion: Logistics functions