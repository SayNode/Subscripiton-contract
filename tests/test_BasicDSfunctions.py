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
    ds_subscriber_account1 = accounts[4]
    ds_subscriber_account2 = accounts[5]

    #Fund accounts
    DHN.transfer(ds_creator_account1, 30*dec_fit, {"from": dohrnii_account}) #fund the creator
    DHN.transfer(ds_creator_account2, 30*dec_fit, {"from": dohrnii_account}) #fund the creator  
    DHN.transfer(ds_subscriber_account1, 30*dec_fit, {"from": dohrnii_account}) #fund sub1
    DHN.transfer(ds_subscriber_account2, 30*dec_fit, {"from": dohrnii_account}) #fund sub2

    #Create a DS and instantiate it
    deployer.createDS(dec_fit, DHN, DSF, ds_creator_account1,"Tetris", "https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/Tetris.html",
                 "Games","Tetris statistics and data", 10*dec_fit, 3600, 2*dec_fit)

    DS_instance1 = deployer.getDSbyName(dec_fit, DSF, random_account1, "Tetris")

    #Sub1
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account1, "Tetris", 0)#subbed for 1 second
    #Sub2
    deployer.subToDS(dec_fit, DHN, DSF, ds_subscriber_account2, "Tetris", 1)#subbed for 1 day

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


#Assertion: Subscriber Functions

    #Fails when subbing with option 0 (1 second sub) as it should,
    assert DS_instance1.requestURL.call({"from": ds_subscriber_account1})=="You are no longer subscribed to this data set"
    #Passes when subbing with option 2 (30 days) as it should
    assert DS_instance1.requestURL.call({"from": ds_subscriber_account2})=="https://ipfs.io/ipfs/bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/wiki/"

#Assertion: Logistics functions