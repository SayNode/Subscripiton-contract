//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";//For time calculations
import "@openzeppelin/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying problems

    contract DataSet is Ownable, ReentrancyGuard{
        //User Variables
        struct Subscriber {
            uint256 price_paid;
            uint256 sub_time;
            bool subbed;
        }

        Subscriber[] public subscriber;
        mapping(address => Subscriber) public addressToSub;

        //Data set Variables
        string DSname;
        string URL;
        string category;
        string shortDesc;
        uint256[] public subscriptionTimes;
        uint256 DSprice;
        uint256 DSrating;
        uint256 creationTime;
        uint256 lastUpdated;
        uint256 uploadFrequency;
        address ownerAddress;

        //Setting initial variables
        constructor(
            string memory _DSname,
            string memory _URL,
            string memory _category,
            string memory _shortDesc,
            uint256 _DSprice,
            uint256 _uploadFrequency
        ) {
            DSname = _DSname;
            URL = _URL;
            category = _category;
            shortDesc = _shortDesc;
            DSprice = _DSprice;
            DSrating = 0;
            creationTime = block.timestamp;
            lastUpdated = block.timestamp;
            uploadFrequency = _uploadFrequency;
        }

        //Modifiers
        modifier onlySubs(){
            require(addressToSub[msg.value].subbed == true);
            _;
        }

    //Creator functions
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

        function changeSubscriptionPeriods(uint[] _subTimes) public onlyOwner {
            //to do
        }

        function deleteDS() public onlyOwner {
            //to do
        }

    //Subscriber function
        function subscribeToDS(uint _subPeriod) public payable {
            //require that pays the correct price for the subscription
            //require he is not subscribed already
            subscriber.push(msg.sender);
            addressToSub[msg.sender] = Subscriber(msg.value, _subPeriod, true);
        }

        function requestURL() public view onlySubs returns(string memory) {
            return URL;
        }

        function checkUpdateSchedule() public {
            //to do
        }

        function checkIfStillSubbed() public {
            //to do
        }
    }
}
