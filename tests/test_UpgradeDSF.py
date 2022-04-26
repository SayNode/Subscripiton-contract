from brownie import accounts, config,chain,  DataSetFactory,DataSet, DHN
import scripts.deploy as deployer

#Test the creation of a new DataSet

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
    deployer.createDS(dec_fit,DHN, DSF, ds_creator_account1,"Tetris", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games","Tetris statistics and data", 10*dec_fit, 3600, 2*dec_fit)

    DS_instance1 = deployer.getDSbyName(dec_fit, DSF, random_account1, "Tetris")

    #Upgrade DataSetFactory. sol to DataSetFactoryV2.sol
    DSF2= deployer.upgradeDSF(dec_fit, DHN,dohrnii_account)
    
    #Create a DS in the DataSetFactoryV2.sol and instantiate it
    deployer.createDS(dec_fit, DHN, DSF2, ds_creator_account2,"Desserts", "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Food","Some dessert recipes", 5*dec_fit, 3600, 2*dec_fit)
          
    DS_instance2 = deployer.getDSbyName(dec_fit, DSF2, random_account1, "Desserts")

    #Assertion: DS creation
    expected1 = ("Tetris", 
                "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Games",
                 "Tetris statistics and data",  
                 20*dec_fit,
                 20*dec_fit,
                 20*dec_fit,
                 2*dec_fit,
                 10*dec_fit,
                 0, 
                 3600,
                 0,
                 ds_creator_account1)
    
    assert expected1 == (DS_instance1.DSname(),
                        DS_instance1.URL(),
                        DS_instance1.category(),
                        DS_instance1.shortDesc(),
                        DS_instance1.stakeAmount(),
                        DS_instance1.stakedAmount(),
                        DHN.balanceOf(DS_instance1),
                        DS_instance1.penalty(),
                        DS_instance1.DSprice(),
                        DS_instance1.DSrating(),
                        DS_instance1.updateFrequency(),
                        DS_instance1.subCount(),
                        DS_instance1.creatorAddress())

    expected2 = ("Desserts", 
                "https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu",
                 "Food",
                 "Some dessert recipes",  
                 20*dec_fit,
                 20*dec_fit,
                 20*dec_fit,
                 2*dec_fit,
                 5*dec_fit,
                 0, 
                 3600,
                 0,
                 ds_creator_account2)
    
    assert expected2 == (DS_instance2.DSname(),
                        DS_instance2.URL(),
                        DS_instance2.category(),
                        DS_instance2.shortDesc(),
                        DS_instance2.stakeAmount(),
                        DS_instance2.stakedAmount(),
                        DHN.balanceOf(DS_instance2),
                        DS_instance2.penalty(),
                        DS_instance2.DSprice(),
                        DS_instance2.DSrating(),
                        DS_instance2.updateFrequency(),
                        DS_instance2.subCount(),
                        DS_instance2.creatorAddress())
    
    #Assertion: see if the upgradeFunction() function, that is only in DataSetFactoryV2.sol, is working
    assert DSF2.upgradeFunction({"from": random_account1}) == "The contract was upgraded"