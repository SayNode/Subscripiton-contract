//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";//For time calculations
import "@openzeppelin/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying problems

contract DataSet is Ownable, ReentrancyGuard{

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
    //DATASET VARIABLES
    //
        string DSname;
        string private URL;
        string category;
        string shortDesc;
        uint256[] public subscriptionTimes;
        uint256 DSprice;
        uint256 DSrating;
        uint256 creationTime;
        uint256 lastUpdated;
        uint256 updateFrequency;
        address creatorAddress;

    //
    //SETTING INITIAL VARIABLES
    //
        constructor(
            string memory _DSname,
            string memory _URL,
            string memory _category,
            string memory _shortDesc,
            address _creatorAddress,
            uint256 _DSprice,
            uint256 _updateFrequency
        ) {
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

        modifier checkIfStillSubbed(){//
            //to do
            //possibly a modifier or just a simple require() inside the requestURL() func
            //sees if the user is still subed (aka now - sub_init_time< sub_time)
            require((block.timestamp - addressToSub[msg.sender].sub_init_time)< addressToSub[msg.sender].sub_time, "You are not subscribed/Your subcription has ended.");
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
            //to do
        }

        function deleteDS() public onlyOwner {
            //to do
            //it should also activate if the staked DHN goes to zero, which means the creator has not updated
            //in a long time
        }

    //
    //SUBSCRIBER FUNCTIONS
    //
        function subscribeToDS(uint _subPeriod) public payable nonReentrant{
            //require that he pays the correct price for the subscription
            //require he is not subscribed already
            require(addressToSub[msg.sender].subbed != true);
            subscribers.push(payable(msg.sender));
            addressToSub[msg.sender] = Subscriber(msg.value, _subPeriod, block.timestamp, true);
        }

        function requestURL() public view onlySubs checkIfStillSubbed returns(string memory) {
            return URL;
        }


    //
    //LOGISTIC FUNCTIONS
    //
        function checkUpdateSchedule() public {
            //to do
            //if lastUpdated+updateTime>updateSchedule the creator should lose some staked DHN coins
        }
    
}
