//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";//For time calculations
import "@openzeppelin/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying problems
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";//To interact with DHN ERC20 Token
import "contracts/DataSetFactory.sol";//Access parent contract



contract DataSet is Ownable, ReentrancyGuard{

    //
    //DHN TOKEN CONTRACT TO INTERACT
    //
    IERC20 public DHN;

    //
    //DATASETFACTORY CONTRACT TO INTERACT
    //
    DataSetFactory public DSF;

    //
    //USER VARIABLES
    //
        struct Subscriber {
            uint256 price_paid;//how much did this sub pay?
            uint256 sub_time;//for how long is this sub subbed?
            uint256 sub_init_time;//when did he sub?
            bool subbed;//for an easy way to check if an address is subbed 
        }

        //array of subscribers addresses
        address[] public subscribers;
        //mapping of a subs address to his info
        mapping(address => Subscriber) public addressToSub;
    //
    //PAYMENT VARIABLES
    //
        struct Deposit {//keep track of when deposits are made (because the creator only gets this money after the sub period of the deposit is over)
            address subscriber_address;
            uint256 deposit_amount;//how much was the deposit
            uint256 time_of_deposit;//when did the deposit start
        }

        //array of deposits
        Deposit[] public deposits;

    //
    //DATASET VARIABLES - THESE COME FROM THE FRONT-END/CLIENT INTERACTION
    //
        string DSname;//Data set name
        string private URL;//IPFS URL
        string category;//Data set category
        string shortDesc;//Data set description
        uint256 subscriptionTime;//Possible sub periods from which the sub can choose (for now lets assume just one for simplicity)
        uint256 stakeAmount;//the amount a creator has to have staked in DHN to create this contract
        uint256 stakedAmount;//the amount a creator still has staked in DHN
        uint256 penalty;//how much staked DHN the creator looses for missing a deadline
        uint256 DSprice;//Data set price
        uint256 DSrating;//Data set rating
        uint256 creationTime;//Data set time of creation
        uint256 lastUpdated;//Keeps track of the time the DS was last updated
        uint256 updateFrequency;//How often if the DS updated?
        uint256 subCount = 0;//See how many people have subscribed to this DS since it was created;
        address creatorAddress;//Address of the creator

    //
    //SETTING INITIAL VARIABLES
    //
        constructor(
            address _DataSetFactoryAddress,
            address _DHNAddress,
            string memory _DSname,
            string memory _URL,
            string memory _category,
            string memory _shortDesc,
            address _creatorAddress,
            uint256 _DSprice,
            uint256 _updateFrequency,
            uint256 _stakeAmount,
            uint256 _penalty
        ) {
            DSF = DataSetFactory(_DataSetFactoryAddress);//Interact with parent contract
            DHN = IERC20(_DHNAddress);//Interact with DHN token contract
            DSname = _DSname;
            URL = _URL;
            category = _category;
            shortDesc = _shortDesc;
            subscriptionTime= 30 days;//WE ARE CONSIDERING THIS THE ONLY OPTION FOR THE TIME BEING
            DSprice = _DSprice;
            DSrating = 0;
            creationTime = block.timestamp;
            lastUpdated = block.timestamp;
            updateFrequency = _updateFrequency;
            creatorAddress = _creatorAddress;
            stakeAmount = _stakeAmount;
            penalty = _penalty;
        }

    //
    //MODIFIERS
    //
        modifier onlySubs(){ //give special permission to only those that are subbed
            require(addressToSub[msg.sender].subbed == true);
            _;
        }

    //
    //CREATOR FUNCTIONS
    //
        function updateURL(string memory _URL) public onlyOwner {
            URL = _URL;
        }

        function changePrice(uint _newPrice) public onlyOwner {
            DSprice = _newPrice;
        }

        function changeCategory(string memory _category) public onlyOwner {
            category = _category;
        }

        function changeDescription(string memory _shortDesc) public onlyOwner {
            shortDesc = _shortDesc;
        }

        function changeSubscriptionPeriods(uint[] memory _subTimes) public onlyOwner {
            //TO DO- ignore for now as we are assuming only one option for subcrition period
        }

        function withdrawFunds() public onlyOwner{//creator uses this to withdraw available funds
            uint withdrawable;
            for(uint i = 0; i<deposits.length; i++){//for every deposit, sees if the deposit was made more than a subcription time ago.
                                                    //if yes, then add it uo to the total of deposits amount the creator can withdraw
                if(block.timestamp - deposits[i].time_of_deposit> subscriptionTime){
                    withdrawable = withdrawable + deposits[i].deposit_amount;
                    deposits[i].deposit_amount=0;
                } 
            }
            //transfers the total withdrawble amount
            DHN.transferFrom(address(this),msg.sender, withdrawable);
            
        }

        function stakeMoreDHN(uint _amount) public payable{//need to see if we want this or not
            //require that currentBalance+_amount<stakeAmount aka his balance of DHN can't be bigger than the pre-established amount  
            require(stakedAmount+_amount<=stakeAmount, "Can't re-stake that much");
            //the creator can replenish his DHN stake if he has lost it by missed date updates
            DHN.transfer(address(this), _amount);
            stakedAmount = stakedAmount + _amount;

        }

        function deleteDS() public onlyOwner {
            
            //it should also activate if the staked DHN goes to zero, which means the creator has not updated in a long time
                //TO DO

            //Has to go into DataSetFactory.sol to delete the mapping of this SC before destroying this SC
            DSF.deleteChild(address.this);

            //Owner gets his money
            uint withdrawable;
            for(uint i = 0; i<deposits.length; i++){//for every deposit, sees if the deposit was made more than a subcription time ago.
                                                    //if yes, then add it uo to the total of deposits amount the creator can withdraw
                if(block.timestamp - deposits[i].time_of_deposit> subscriptionTime){
                    withdrawable = withdrawable + deposits[i].deposit_amount;
                    deposits[i].deposit_amount=0;
                } 
            }
            //transfers the total withdrawble amount
            DHN.transferFrom(address(this),msg.sender, withdrawable);

            //Has to give back to subs the money they paid for their current subscription because it want be finished
            for(uint i = 0; i<deposits.length; i++){
                if(deposits[i].deposit_amount>0){
                    DHN.transferFrom(address(this),payable(deposits[i].subscriber_address), deposits[i].deposit_amount);
                    deposits[i].deposit_amount=0;
                }
            }
            
            //selfdestructs
                selfdestruct(creatorAddress);
        }

    //
    //SUBSCRIBER FUNCTIONS
    //
        function subscribeToDS(uint _subPeriod) public payable nonReentrant{

            //require he is not subscribed already
            require(addressToSub[msg.sender].subbed != true, "You are already subbed to this data set.");
  
            //require that he pays the correct DHN price for the subscription
            require(DHN.balanceOf(msg.sender)>= stakeAmount, "You don't have enough DHN tokens for the staking requirment.");
            DHN.transferFrom(msg.sender, address(this), DSprice);
            deposits.push(Deposit(msg.sender,DSprice, block.timestamp));

            //if the user already has info in this DS
            if(addressToSub[msg.sender].sub_init_time!=0){
                addressToSub[msg.sender].subbed=true;//declare that he is subbed again
                addressToSub[msg.sender].sub_init_time=block.timestamp;//update the time he subbed
                addressToSub[msg.sender].sub_time=_subPeriod;//update his subbed time
                addressToSub[msg.sender].price_paid = DSprice;//update the price paid
            }else{//else
                subscribers.push(payable(msg.sender));//add new sub address to the record
                addressToSub[msg.sender] = Subscriber(DSprice, _subPeriod, block.timestamp, true);//create the new sub info
                                                                                                    //and map it to his address
                subCount++;//increment all time sub count
            }

        }

        function requestURL() public onlySubs returns(string memory) {
            //if the sub time hasn't expired yet
            if(checkIfStillSubbed()){
                return URL;//return the url link
            }
            //else 
            //this subscriber is no longer subscribed (but we keep his info in order to facilitate a possible re-sub)
            addressToSub[msg.sender].subbed=false;
            return "You are no longer subscribed to this data set";
        }


    //
    //LOGISTIC FUNCTIONS
    //
        function checkUpdateSchedule() public {
            //TO DO

            //if lastUpdated+block.timestamp>lastUpdated+updateFrequency the creator should lose some staked DHN coins
            //we will need to add the buffer later
            if(lastUpdated+block.timestamp>lastUpdated+updateFrequency){
                //do something
                stakeAmount = stakeAmount-penalty;
            }
        }

        function checkIfStillSubbed() public view returns(bool){//is the user still in its sub period?

            //if: now -  the initial sub time < the subscription time
            if((block.timestamp - addressToSub[msg.sender].sub_init_time)< addressToSub[msg.sender].sub_time){
                return true;
            }//else
            return false;
            
        }

        function numberOfCurrentlySubbed() public view returns(uint){//how many people are currently subbed?
            uint count = 0;
            for(uint i = 0; i<subscribers.length; i++){
                if(addressToSub[subscribers[i]].subbed == true)count++;
            }
            return count;
        }

        function getContractBalance() public view returns(uint){
            return DHN.balanceOf(address(this));
        }
    
}
