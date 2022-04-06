//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";//For time calculations
import "@openzeppelin/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying problems
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";//To interact with DHN ERC20 Token

contract DataSet is Ownable, ReentrancyGuard{

    //
    //DHN TOKEN CONTRACT TO INTERACT
    //
    IERC20 public DHN;

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
    //DATASET VARIABLES - THESE COME FROM THE FRONT-END/CLIENT INTERACTION
    //
        string DSname;//Data set name
        string private URL;//IPFS URL
        string category;//Data set category
        string shortDesc;//Data set description
        uint256[] public subscriptionTimes;//Possible sub periods from which the sub can choose
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
            address _DHNAddress,
            string memory _DSname,
            string memory _URL,
            string memory _category,
            string memory _shortDesc,
            address _creatorAddress,
            uint256 _DSprice,
            uint256 _updateFrequency
        ) {
            DHN = IERC20(_DHNAddress);
            DSname = _DSname;
            URL = _URL;
            category = _category;
            shortDesc = _shortDesc;
            DSprice = _DSprice;
            DSrating = 0;
            creationTime = block.timestamp;
            lastUpdated = block.timestamp;
            updateFrequency = _updateFrequency;
            creatorAddress = _creatorAddress;
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
            //TO DO
        }

        function deleteDS() public onlyOwner {
            //TO DO
            //it should also activate if the staked DHN goes to zero, which means the creator has not updated
            //in a long time
        }

    //
    //SUBSCRIBER FUNCTIONS
    //
        function subscribeToDS(uint _subPeriod) public payable nonReentrant{
            //require that he pays the correct DHN price for the subscription - TO DO

            //require he is not subscribed already
            require(addressToSub[msg.sender].subbed != true, "You are already subbed to this data set.");

            //if the user already has info in this DS
            if(addressToSub[msg.sender].sub_init_time!=0){
                addressToSub[msg.sender].subbed=true;//declare that he is subbed again
                addressToSub[msg.sender].sub_init_time=block.timestamp;//update the time he subbed
                addressToSub[msg.sender].sub_time=_subPeriod;//update his subbed time
            }else{//else
                subscribers.push(payable(msg.sender));//add new sub address to the record
                addressToSub[msg.sender] = Subscriber(msg.value, _subPeriod, block.timestamp, true);//create the new sub info
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
            }
        }

        function checkIfStillSubbed() public view returns(bool){//is the user still in its sub period?
            //sees if the user is still subed:
            //if now -  the initial sub time < the subscription time
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
    
}
